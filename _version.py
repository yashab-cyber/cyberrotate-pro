"""
Version information for CyberRotate Pro
"""

__version__ = "2.1.0"
__author__ = "Yashab Alam"
__email__ = "yashabalam707@gmail.com"
__company__ = "ZehraSec"
__website__ = "https://www.zehrasec.com"
__github__ = "https://github.com/yashab-cyber/cyberrotate-pro"

VERSION_INFO = {
    "major": 1,
    "minor": 0,
    "patch": 0,
    "pre_release": None,
    "build": None
}

def get_version():
    """Return the version string"""
    return __version__

def get_version_info():
    """Return version information as a dictionary"""
    return {
        "version": __version__,
        "author": __author__,
        "email": __email__,
        "company": __company__,
        "website": __website__,
        "github": __github__,
        "version_info": VERSION_INFO
    }
