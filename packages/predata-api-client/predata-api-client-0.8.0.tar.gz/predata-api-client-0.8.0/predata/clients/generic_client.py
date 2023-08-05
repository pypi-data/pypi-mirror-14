import time
import urllib

import requests

from predata.config.exceptions import PredataPythonClientExeception
from predata.config.logger import logger


class PredataGenericClient(object):

    def __init__(self, session, hostname, api_base, max_retries):
        self.session = session
        self.HOSTNAME = hostname
        self.API_BASE = api_base
        self.MAX_RETRIES = max_retries

    def _build_endpoint(self, endpoint, query_dict, encoding=False):
        params = urllib.urlencode({k: query_dict[k] for k in query_dict.keys() if query_dict[k]}, encoding)
        if params:
            endpoint += "?%s" % params
        return endpoint

    def make_request(self, endpoint, method="GET", query_dict=None, encoding=False, process_rpc=False, data=None):
        """
        Make and paginate through results if necessary.
        """
        total_response = []
        MAX_RETRIES = self.MAX_RETRIES
        retries = 0

        if query_dict:
            endpoint = self._build_endpoint(endpoint, query_dict, encoding=encoding)
        current_endpoint = self.HOSTNAME + self.API_BASE + endpoint

        while current_endpoint and retries < MAX_RETRIES:
            logger.info("[%s]: Making request to %s" % (method, current_endpoint))

            try:
                if method == "GET":
                    resp = self.session.get(current_endpoint)
                elif method == "PUT":
                    resp = self.session.put(current_endpoint, data=data)
                else:
                    raise PredataPythonClientExeception("%s: Invalid method", method)
            except requests.exceptions.ConnectionError:
                logger.debug("Request to %s failed on ConnectionError" % current_endpoint)
                retries += 1
                continue

            if resp.status_code == 404:
                logger.debug("Request to %s failed on HTTP 404 response code" % current_endpoint)
                # a 404 / not found should just return empty
                break
            elif resp.status_code == 403 or (resp.status_code != 200 and method == "PUT"):
                # permission denied or a bad put request should just return error message
                return resp.json()
            elif resp.status_code != 200:
                # if it is anything other than 200 and not above, log error and retry
                logger.debug("Request to %s failed on HTTP %s response code" %
                             (current_endpoint, resp.status_code))
                retries += 1
                continue

            retries = 0

            response_content = resp.json()

            # if it is an RPC call and progress
            if process_rpc and ("callback" in response_content or "progress" in response_content):
                logger.debug("Processing RPC to %s" % current_endpoint)
                if "callback" in response_content:
                    current_endpoint = self.HOSTNAME + response_content["callback"]
                time.sleep(1.0)
                continue

            if "results" in response_content and response_content["results"] != "processing":
                total_response += response_content["results"]
                if "next" in response_content:
                    current_endpoint = response_content["next"]
                else:
                    current_endpoint = None
            else:
                total_response = response_content
                current_endpoint = None

        if retries >= MAX_RETRIES:
            raise PredataPythonClientExeception("Exceeded maximum number of retries to the server.")

        return total_response
