import versioneer
from setuptools import find_packages, setup

setup(
    name='Methanal',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    maintainer='Methanal developers',
    description='A web forms library for Mantissa',
    url='https://github.com/fusionapp/methanal',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Twisted',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    packages=find_packages() + ['nevow.plugins', 'xmantissa.plugins'],
    include_package_data=True,
    install_requires=['Twisted >= 2.5.0',
                      'Epsilon >= 0.5.0',
                      'Axiom >= 0.5.20',
                      'Nevow >= 0.12.0',
                      'Mantissa >= 0.6.1',
                      'fusion_util >= 1.1.1'])
