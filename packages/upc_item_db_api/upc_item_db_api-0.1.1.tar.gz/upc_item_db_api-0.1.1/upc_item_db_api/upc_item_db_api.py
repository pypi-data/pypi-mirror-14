import requests
import urllib


class UPCItemDBError(Exception):
    def __init__(self, code, message):
        self.message = str(code) + " " + message


class Connection(object):
    """
    A class for establishing a connection with the UPCItemDB API
    http://www.upcitemdb.com/api/explorer

    Every response in JSON with the following format
    {
        "code": string,
        "total": int,
        "offset": int,
        "items": [{
            "ean": string,
            "title": string,
            "upc": string,
            "description": string,
            "brand": string,
            "model": string,
            "dimension": string,
            "weight": string,
            "currency": string,
            "lowest_recorded_price": int,
            "images": [string],
            "offers": [
                {
                    "merchant": string,
                    "domain": string,
                    "title": string,
                    "currency": string,
                    "list_price": int,
                    "price": int,
                    "shipping": string,
                    "condition": string,
                    "availability": string,
                    "link": string,
                    "updated_t": integer
                }
            ]
        }]
    }
    """

    def __init__(self, api_key=None):
        """
        @parameter api_key (required): your api key -- string
        """
        self.api_key = api_key
        self.base_url = "https://api.upcitemdb.com/prod/trial"

    def post_lookup(self, params={}):
        """
        Lookup products by structured search parameters via HTTP POST

        @parameter params: the parameters to lookup the item with -- dictionary

        currently supported keys:
            - params["upc"] -- string
        """
        url = '{}/lookup'.format(self.base_url)
        return self._post_request(url, params)

    def lookup(self, upc=None):
        """
        Lookup products by upc via HTTP GET

        @parameter upc (required): the upc/isb/ean of the item -- string
        """
        url = "{}/lookup?upc={}".format(self.base_url, upc)
        return self._get_request(url)

    def search(self, s=None, brand=None, category=None, offset=None,
            item_type='product'):
        """
        Search for products by keyword and other filters via HTTP GET

        @parameter s (required): keywords to search with -- string
        @parameter brand: brand name                     -- string
        @parameter category: product category keyword    -- string
        @parameter offset: offset for results paging     -- int
        @parameter type: 'book' or 'product'             -- string default: 'product'
        """
        args = {}
        if not s:
            raise ArgumentError
        args["s"] = s
        if brand: args["brand"] = brand
        if category: args["category"] = category
        if brand: args["brand"] = brand
        if offset: args["offset"] = offset
        args["type"] = item_type
        url = "{}/search?{}".format(self.base_url, urllib.urlencode(args))
        return self._get_request(url)

    def post_search(self, params={}):
        """
        Search for products with structured search parameters via HTTP POST

        @parameter params: the parameters to search the items with -- dictionary

        currently supported keys:
            - params["s"]                  -- string
            - params["type"]               -- string
            - params["offset"]             -- int
            - params["filter"]["brand"]    -- string
            - params["filter"]["category"] -- string
        """
        url = "{}/search".format(self.base_url)
        return self._post_request(url, params)

    def _raise_error_if_any(self, data):
        """Raises an error if the passed response data is an error code"""
        if data["code"] != "OK":
            raise UPCItemDBError(data["code"], data["message"])

    def _get_request(self, url):
        response = requests.get(url)

        try:
            data = response.json()
            self._raise_error_if_any(data)
        except ValueError:
            raise UPCItemDBError(0, "no response from server")

        return data

    def _post_request(self, url, data={}):
        response = requests.post(url, json=data)

        try:
            data = response.json()
            self._raise_error_if_any(data)
        except ValueError:
            raise UPCItemDBError(0, "no response from server")

        return data
