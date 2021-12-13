from enum import Enum, unique
from connection import Connection


@unique
class EndpointEnum(Enum):
    AUTH = 0
    USER_PANEL = 1
    LIVE_STREAMS = 2
    VODS = 3
    LIVE_CATEGORIES = 4
    LIVE_STREAMS_BY_CATEGORY = 5
    SERIES = 6
    XMLTV = 7
    ALL_EPG = 8
    SHORT_EPG = 9
    CATCHUP = 10
    VOD_CATEGORIES = 11
    VOD_STREAMS_BY_CATEGORY = 12
    SERIES_CATEGORIES = 13
    SERIES_STREAMS_BY_CATEGORY = 15
    SERIES_INFO = 16

class Url_api_builder:
    endpoints = {
        "auth": "{}://{}:{}/player_api.php?username={}&password={}",
        "user_panel": "{}://{}:{}/panel_api.php?username={}&password={}",
        "live_streams": "{}://{}:{}/player_api.php?username={}&password={}&action=get_live_streams",
        "vods": "{}://{}:{}/player_api.php?username={}&password={}&action=get_vod_streams",
        "live_categories": "{}://{}:{}/player_api.php?username={}&password={}&action=get_live_categories",
        "live_streams_by_category": "{}://{}:{}/player_api.php?username={}&password={}&action=get_live_streams&category_id={}",
        "series_all": "{}://{}:{}/player_api.php?username={}&password={}&action=get_series",
        "xmltv": "{}://{}:{}/xmltv.php?username={}&password={}",
        "all_epg": "{}://{}:{}/xmltv.php?username={}&password={}&action=get_simple_data_table&stream_id={}",
        "short_epg": "{}://{}:{}/xmltv.php?username={}&password={}&action=get_short_epg&stream_id={}&limit={}",
        "catchup": "{}://{}:{}/streaming/timeshift.php?username={}&password={}&stream=2&start=2019-04-19:16-00&duration=120",
        "vod_categories": "{}://{}:{}/player_api.php?username={}&password={}&action=get_vod_categories",
        "vod_streams_by_category": "{}://{}:{}/player_api.php?username={}&password={}&action=get_vod_streams&category_id={}",
        "series_categories": "{}://{}:{}/player_api.php?username={}&password={}&action=get_series_categories",
        "series_streams_by_category": "{}://{}:{}/player_api.php?username={}&password={}&action=get_series&category_id={}",
        "series_info": "{}://{}:{}/player_api.php?username={}&password={}&action=get_series_info&series_id={}",
        
    }

    @staticmethod
    def build(ep: EndpointEnum, cnx: Connection, *args):
        return Url_api_builder.endpoints[str.lower(ep.name)].format(
            cnx.scheme, cnx.server, cnx.port, cnx.username, cnx.password, *args
        )
