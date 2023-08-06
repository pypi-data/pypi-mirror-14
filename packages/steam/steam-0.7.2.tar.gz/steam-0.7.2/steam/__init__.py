__version__ = "0.7.2"
__author__ = "Rossen Georgiev"

version_info = (0, 7, 2)

from steam.steamid import SteamID
from steam.webapi import WebAPI


# proxy object
# avoids importing steam.enums.emsg unless it's needed
class SteamClient(object):
    def __new__(cls, *args, **kwargs):
        from steam.client import SteamClient as SC
        return SC(*args, **kwargs)
