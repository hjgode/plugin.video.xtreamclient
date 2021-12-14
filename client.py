import requests
from requests.models import Response

from connection import Connection
from url_api_builder import EndpointEnum, Url_api_builder


class Client:
    def __init__(self, url: str):
        self._url = url
        self.last_error="None"
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
        r = Response
        r.status_code=200
        self.last_error="None"
        try:
            r = requests.get(Url_api_builder.build(ep, self._connection, *args))
            if r.status_code==200:
                self.last_error="None"
                return r.json()
#            return r.json() if r.status_code == 200 else None
        except requests.exceptions.HTTPError as e:
            print('HTTP Error')
            self.last_error='HTTP Error'
            print(e)
        except requests.exceptions.ConnectionError as e:
            print("ConnectionError")
            self.last_error='ConnectionError'
            print(e)
        except requests.exceptions.RequestException as e:
            print("RequestException")
            self.last_error="RequestException"
            print(e)
        except Exception as e:
            self.last_error=e.__doc__
        return None
#        if r.status_code ==200:
#            return r.json()
#        else:
#            return None
#        return r.json() if r.status_code == 200 else None

    def get_last_error(self):
        if self.last_error==None:
            self.last_error="unknown, see log"
        return self.last_error