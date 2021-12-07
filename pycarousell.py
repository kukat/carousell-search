import requests
import json

import myconfigurations as config


class CarousellSearch(object):
    def __init__(self, query_string=None, results=30):
        self.base_url = ("https://www.carousell.sg/api-service/filter/cf/4.0/search/")
        self.fields = {
            "bestMatchEnabled": True,
            "canChangeKeyword": False,
            "ccid": "5729",
            "count": 20,
            "countryCode": "SG",
            "countryId": "1880251",
            "filters": [
                {
                "rangedFloat": { "start": { "value": "600" }, "end": { "value": "800" } },
                "fieldName": "price"
                }
            ],
            "includeSuggestions": False,
            "locale": "en",
            "prefill": {
                "prefill_sort_by": "3",
                "prefill_price_start": "600",
                "prefill_price_end": "800"
            },
            "query": "xbox series x",
            "sortParam": { "fieldName": "3" }
        }

        self.query_fields = json.dumps(self.fields)
        self.query_url = self.base_url

    def send_request(self):
        # print(self.query_url)
        # print(self.query_fields)
        r = requests.post(self.query_url, json=self.fields)
        data = json.loads(r.text)
        return data['data']['results']
