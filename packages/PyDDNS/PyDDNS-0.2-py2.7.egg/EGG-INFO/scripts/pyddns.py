import boto.route53
import urllib2
import logging
import ConfigParser
import os
import sys

DEBUG = True
conf = None
logger = logging.getLogger("pyddns")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# sh = logging.handlers.SysLogHandler(('172.16.3.254',logging.handlers.SYSLOG_UDP_PORT ), logging.handlers.SysLogHandler.LOG_USER)
sh = logging.handlers.SysLogHandler(address = '/dev/log')
sh.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)
ch.setFormatter(formatter)

sh_formatter = logging.Formatter('%(name)s[%(process)d]: %(levelname)s: %(message)s')

sh.setFormatter(sh_formatter)

logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(sh)


class NotConfiguredException(Exception):
    pass

def get_configuration():
    # first, try to get a config file in the current directory, then under
    # the ~/.config/pyddns directory, and finally under /etc/pyddns/
    base_dir =  os.path.dirname(os.path.realpath(__file__))
    path_list = [os.path.expanduser(i) for i in (base_dir, '~/.config/pyddns/', '/etc/pyddns/')
    ]
    config = ConfigParser.ConfigParser()
    for path in path_list:
        config_path = os.path.join(path, 'pyddns.conf')
        if os.path.exists(config_path):
            config.readfp(open(config_path))
            return config
    raise NotConfiguredException

def get_my_ip():
    # returns current IP address from ident.me
    res = urllib2.urlopen('https://ident.me').read()
    return res

def get_zone_configuration(conf, zone_name):
    res = None
    update = False
    for z in [zone_name, zone_name[:-1]]:
        try:
            update = conf.get(z, 'set_main').lower() == 'true'
            break
        except ConfigParser.NoSectionError:
            continue
    return update

def main():
    logger.debug("Starting pyddns")
    cur_ip = get_my_ip()
    conf = get_configuration()
    conn = boto.route53.connection.Route53Connection(
        aws_access_key_id = conf.get('aws', 'access_key_id'),
        aws_secret_access_key = conf.get('aws', 'secret_access_key')
    )
    zones = conn.get_zones()

    for zone in zones:

        change_set = boto.route53.record.ResourceRecordSets(conn, zone.id)
        # check if it's configured
        zone_name = zone.name
        update_zone = get_zone_configuration(conf, zone_name)
        if update_zone:
            logger.debug( "Processing %s" % zone.name)
            old_ip = zone.get_a(zone.name).resource_records[0]
            # print dir(old_ip)
            if old_ip != cur_ip:
                logger.info("Changing IP for %s from %s to %s" % (zone.name, old_ip, cur_ip))
                changes = change_set.add_change("UPSERT", zone.name, type="A")
                changes.add_value(cur_ip)
                res = change_set.commit()
            else:
                logger.debug("Skipping %s: Already current" % zone.name)
        else:
            logger.debug("Skipping %s" % zone.name)





if __name__=='__main__':
    main()



# conn = route53.connect('')
