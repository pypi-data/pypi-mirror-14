__version__ = '0.2.1'
__version_info__ = '.'.split(__version__)
for i in range(len(__version_info__)):
    if __version_info__[i].isdigit():
        __version_info__[i] = int(__version_info__[i])
