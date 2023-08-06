from setuptools import setup, find_packages
from distutils.command.install import INSTALL_SCHEMES

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setup(
    name = "PyDDNS",
    version = "0.2",
    packages = find_packages(),
    scripts = ['pyddns/pyddns.py'],
    install_requires = ['boto'],
    package_data = {
        '':['*.dist', '*.md', '*.txt'],
    },
    data_files=[('', ['LICENSE.txt', 'pyddns/pyddns.conf.dist'])],
    include_package_data = True,
    author = 'Eric Williams',
    author_email = 'eric@ehw.io',
    description="PyDDNS uses Amazon's Route53 as a Dynamic DNS provider for sites with "
                "dynamic IP addresses",
    license = "MIT",
    keywords = "AWS EC2 DDNS DynDNS boto",
    url = "http://bitbucket.org/rubeon/pyddns/",
    identifiers = [
        'Development Status :: 4 - Beta',
        'Topic :: System :: Networking',
        'Topic :: Internet :: Name Service (DNS)'
        ]
)
