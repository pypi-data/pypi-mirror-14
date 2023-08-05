version_major = 1
version_minor = 0
version_micro = 2
version_extra = ''

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
__version__ = '%s.%s.%s%s' % (version_major,
                              version_minor,
                              version_micro,
                              version_extra)
# Main setup parameters
NAME = 'catidb_api'
DESCRIPTION = 'Client API for CATI data management servers'
PROJECT = 'catidb'
ORGANISATION = 'CATI'
AUTHOR = 'CATI'
AUTHOR_EMAIL = 'support@cati-neuroimaging.com'
URL = 'https://cati.cea.fr'
LICENSE = 'CeCILL-B'
VERSION = __version__
REQUIRES = ['requests[security]', 'soma-base[crypto]', ]
