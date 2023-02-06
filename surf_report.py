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
    data_json = json.loads(data)["data"][context]
    return (data, data_json)

def parse_ratings(ratings):
    result = []
    for rating in ratings:
        date = time.strftime('%m/%d@%H:%M', time.localtime(rating["timestamp"]))
        grade = rating["rating"]["key"]
        result.append("%s %s" % (date, grade))
    return result
def parse_waves(waves_data):
    result = []
    for wave_data in waves_data:
        date = time.strftime('%m/%d@%H:%M', time.localtime(wave_data["timestamp"]))
        surf_min = wave_data["surf"]["min"]
        surf_max = wave_data["surf"]["max"]
        primary_swell = wave_data["swells"][0]
        primary_swell_height = primary_swell["height"]
        primary_swell_direction = primary_swell["direction"]
        if primary_swell_direction == 0 and primary_swell_height == 0:
            primary_swell = wave_data["swells"][1]
            primary_swell_height = round(primary_swell["height"], 1)
            primary_swell_direction = primary_swell["direction"]
        result.append("\theight: %s-%sft\tprimary swell: %sft @ %s" %
                      (surf_min, surf_max, primary_swell_height, primary_swell_direction))
        # print(f"{date}\theight: {surf_min}-{surf_max}ft\tprimary swell: {primary_swell_height}ft @ {primary_swell_direction}deg")
    return result

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

def get_report_for_location(location):
    if location not in surfline:
        return "Location %s not available" % location
    contexts = [
            "rating",
            "wave",
            "wind",
            "tides"
            ]
    results = {}
    for context in contexts:
        (data, data_json) = get_data(location, context)
        results[context] = data_json

    ratings = parse_ratings(results["rating"])
    waves = parse_waves(results["wave"])

    reply = "%s (%s)\n" % (surfline[location]["name"], surfline[location]["link"])
    for i in range(len(ratings)):
        reply += "%s\n%s\n" % (ratings[i],  waves[i])
    return reply

def get_locations():
    return surfline.keys()
