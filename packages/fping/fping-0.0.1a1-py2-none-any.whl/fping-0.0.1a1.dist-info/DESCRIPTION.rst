# fping.py
Python library that uses the fping executable as its ping engine.

### Requirements
* Python 2.7 on Linux or Mac OS X (Python 3.5 compatibility is in the works,
 but not there yet.)
* netaddr library (e.g. pip install netaddr)
* Custom, forked build of fping (see Installation).

### Installation
This library requires a forked version of fping, that has an added option to
output the basic alive, unreachable and unresolvable hosts in CSV format.

* Go to https://github.com/NetworkEng/fping and follow the installation
instructions there to compile and install the custom version. Since you will
be downloading the files directly from github, DO NOT skip step 1.
* If you have issues running autogen.sh, please make sure that you have 
installed the automake package that is appropriate for your Linux distribution.
* For Mac OS X you will need:
    * Xcode installed from the app store (launch it via gui at least once 
    after install)
    * Xcode command line developer tools via 'xcode-select --install'
    * Accept the command line license agreement via
    'sudo xcodebuild -license accept'
    * Install homebrew, and then use 'brew install automake'

### Usage
Though this is a work in progress, in its current state, this script is 
intended to be a library that is called and executed either in the (i)python 
interpreter / shell, or imported and used by another python script.

    Examples:
        >>> from fping import FastPing
        >>> fp = FastPing()
        >>> fp.ping(filename='testing')
        # cmd =  ['/usr/local/sbin/fping', '-nV', '8.8.8.8',
                  'www.google.com', '206.190.36.45', 'localhost',
                  'host.cannotresolve.com']
        {'host.cannotresolve.com': 'unresolvable',
        'pa-in-f99.1e100.net': 'alive',
        'google-public-dns-a.google.com': 'alive',
        'localhost': 'unreachable',
        'ir1.fp.vip.gq1.yahoo.com': 'alive'}
        >>> fp.hosts(filename='testing', status='alive')
        'pa-in-f99.1e100.net': 'alive',
        'google-public-dns-a.google.com': 'alive',
        'ir1.fp.vip.gq1.yahoo.com': 'alive'}
        >>> fp.alive
        ['pa-in-f99.1e100.net',
        'google-public-dns-a.google.com',
        'ir1.fp.vip.gq1.yahoo.com']
        >>> fp.dead
        ['localhost']
        >>> fp.noip
        ['host.cannotresolve.com']
        >>>


