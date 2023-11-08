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

    def __init__(self, data: dict[str]):
        if data["status"] == "success":
            self.origin_query = data["query"]
            self.country = data["country"]
            self.country_code = data["countryCode"]
            self.isp = data["isp"]
            self.organization = data["org"]
            self.latitude = data["lat"]
            self.longitude = data["lon"]
            self.timezone = data["timezone"]


async def create_geolocationgetter(ip: str) -> GeolocationGetter:
    ip_base_url = (
        f"http://ip-api.com/json/{ip}"
        f"?fields=status,country,countryCode,lat,lon,timezone,isp,org,query"
    )
    data = await AsyncHTTP(ip_base_url).get_json_contents()
    return GeolocationGetter(data)
