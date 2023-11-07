import asyncio
import dataclasses

from whoispyside6_clone.utils.async_http import AsyncHTTP


@dataclasses.dataclass
class GeolocationGetter:
    origin_query: str
    country: str
    country_code: str
    isp: str
    organization: str
    latitude: str
    longitude: str
    timezone: str

    def __init__(self, ip):
        self.ip = ip
        self.ip_base_url = (f"http://ip-api.com/json/{self.ip}"
                            f"?fields=status,country,countryCode,lat,lon,timezone,isp,org,query")

        data = asyncio.get_event_loop().run_until_complete(AsyncHTTP(url=self.ip_base_url).get_json_contents())
        if data["status"] == "success":
            self.origin_query = data["query"]
            self.country = data["country"]
            self.country_code = data["countryCode"]
            self.isp = data["isp"]
            self.organization = data["org"]
            self.latitude = data["lat"]
            self.longitude = data["lon"]
            self.timezone = data["timezone"]


if __name__ == '__main__':
    SAMPLE = GeolocationGetter(ip="google.com")
    print(SAMPLE)
