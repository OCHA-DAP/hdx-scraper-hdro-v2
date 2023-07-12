import requests

from hdx.location.country import Country


_API_URL = "https://api.hdrdata.org/CountryIndicators/{country_iso3}"


def get_country_data() -> dict:
    """Get the HDRO API data for every country. Takes a few minutes to run.
    Returns a dictionary with ISO3 keys, and values that are each a dictionary
    of the JSON returned from the API."""
    country_data = dict()
    for country_iso3 in Country.countriesdata()["countries"].keys():
        response = requests.get(_API_URL.format(country_iso3=country_iso3.lower()))
        data_json = response.json()
        if not data_json:
            continue
        country_data[country_iso3] = data_json
        # TODO: remove this after testing
        break
    return country_data

    # with open('tmp.csv', 'w') as f:
    #    writer = csv.DictWriter(f, fieldnames=data_json[0])
    #    writer.writeheader()
    #    writer.writerows(data_json)
