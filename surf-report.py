from urllib.request import urlopen
from urllib.parse import urlencode, urljoin
import json
import time
# https://services.surfline.com/kbyg/spots/forecasts/weather?spotId=5cbf8d85e7b15800014909e8&days=2&intervalHours=3

def get_data(location, context):
    url = urljoin(surfline_api_base_url, context)
    days = 2
    interval_hours = 3
    params = urlencode({
        'spotId': surfline[location]["id"],
        'days': days,
        'intervalHours': interval_hours
        })
    url = "%s?%s" % (url, params)
    print(f"requesting url: {url}")

    response = urlopen(url)
    data = response.read()
    data_json = json.loads(data)
    return (data, data_json)

surfline_api_base_url = "https://services.surfline.com/kbyg/spots/forecasts/"
surfline = {
        "north-ocean-beach": {
            "link": "https://www.surfline.com/surf-report/north-ocean-beach/5d9b68deab58860001c7359e",
            "id": "5d9b68deab58860001c7359e",
            "name": "North Ocean Beach"
            },
        "central-ocean-beach": {
            "link": "https://www.surfline.com/surf-report/central-ocean-beach/638e32a4f052ba4ed06d0e3e",
            "id": "638e32a4f052ba4ed06d0e3e",
            "name": "Central Ocean Beach"
            },
        "south-ocean-beach": {
            "link": "https://www.surfline.com/surf-report/south-ocean-beach/5842041f4e65fad6a77087f9",
            "id": "5842041f4e65fad6a77087f9",
            "name": "South Ocean Beach"
            },
        "rockaway": {
            "link": "https://www.surfline.com/surf-report/rockaway/5842041f4e65fad6a7708979",
            "id": "5842041f4e65fad6a7708979",
            "name": "Rockaway"
            },
        "pacifica": {
            "link": "https://www.surfline.com/surf-report/pacifica/5cbf8d85e7b15800014909e8",
            "id": "5cbf8d85e7b15800014909e8",
            "name": "Pacifica"
            },
        "pacifica-linda-mar": {
            "link": "https://www.surfline.com/surf-report/pacifica-linda-mar/5842041f4e65fad6a7708976",
            "id": "5842041f4e65fad6a7708976",
            "name": "Pacifica / Linda Mar"
            },
        "montara": {
            "link": "https://www.surfline.com/surf-report/montara/5842041f4e65fad6a7708974",
            "id": "5842041f4e65fad6a7708974",
            "name": "Montara"
            },
        "maverick-s": {
            "link": "https://www.surfline.com/surf-report/maverick-s/5842041f4e65fad6a7708801",
            "id": "5842041f4e65fad6a7708801",
            "name": "Maverick's"
            },
        "princeton-jetty": {
            "link": "https://www.surfline.com/surf-report/princeton-jetty/5842041f4e65fad6a7708970",
            "id": "5842041f4e65fad6a7708970",
            "name": "Princeton Jetty"
            }
        }

context = "rating"
location = "pacifica-linda-mar"

(data, data_json) = get_data(location, context)

for rating in data_json["data"]["rating"]:
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rating["timestamp"]))
    grade = rating["rating"]
    print(f"{date}: {grade}")
