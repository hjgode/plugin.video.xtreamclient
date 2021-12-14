import requests

from connection import Connection
from url_api_builder import EndpointEnum, Url_api_builder


class Client:
    def __init__(self, url: str):
        self._url = url
        self.matched, self._connection = Connection.from_url(url)

    def user_panel(self):
        return self._get(EndpointEnum.USER_PANEL)

    def auth(self):
        return self._get(EndpointEnum.AUTH)

    def live_streams(self):
        return self._get(EndpointEnum.LIVE_STREAMS)

    def vods(self):
        return self._get(EndpointEnum.VODS)

    def vod_categories(self):
        return self._get(EndpointEnum.VOD_CATEGORIES)
    def vod_streams_by_category(self, category: str):
        return self._get(EndpointEnum.VOD_STREAMS_BY_CATEGORY, category)

    def live_categories(self):
        return self._get(EndpointEnum.LIVE_CATEGORIES)

    def live_streams_by_category(self, category: str):
        return self._get(EndpointEnum.LIVE_STREAMS_BY_CATEGORY, category)

    def series_categories(self):
        return self._get(EndpointEnum.SERIES_CATEGORIES)
    def series_streams_by_category(self, category: str):
        return self._get(EndpointEnum.SERIES_STREAMS_BY_CATEGORY, category)
    def series_info_by_id(self, id: str):
        return self._get(EndpointEnum.SERIES_INFO, id)
    def series(self): #get all series
        return self._get(EndpointEnum.SERIES)

    def xmltv(self):
        return self._get(EndpointEnum.XMLTV)

    def all_epg(self, stream_id: int):
        return self._get(EndpointEnum.ALL_EPG, stream_id)

    def short_epg(self, stream_id: int, limit: int = 5):
        return self._get(EndpointEnum.SHORT_EPG, stream_id, limit)

    def catchup(self):
        return self._get(EndpointEnum.CATCHUP)

    def _get(self, ep: EndpointEnum, *args):
        try:
            r = requests.get(Url_api_builder.build(ep, self._connection, *args))
        except requests.exceptions.RequestException as e:
            print(e.strerror)
        return r.json() if r.status_code == 200 else None
