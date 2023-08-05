import base64
import requests

from predata.clients.signal_client import PredataSignalClient
from predata.clients.data_client import PredataDataClient
from predata.clients.analysis_client import PredataAnalysisClient
from predata.clients.user_client import PredataUserClient

from predata.config.constants import (
    PRODUCTION_HOSTNAME,
    DEVELOPMENT_HOSTNAME,
    API_BASE_VERSION_1,
    MAX_NUMBER_OF_RETRIES
)
from predata.config.exceptions import PredataPythonClientExeception


class PredataClient():

    """
    Predata Python API Client.
    """

    data_client = None
    signal_client = None
    analysis_client = None
    user_client = None

    def __init__(self, token=None, username=None, password=None, version=1, hostname="prod"):
        """
        Supports token authentication or basic authentication.
        """
        if version == 1:
            self.API_BASE = API_BASE_VERSION_1
        else:
            raise PredataPythonClientExeception("Unsupported API version")

        if hostname == "prod":
            self.HOSTNAME = PRODUCTION_HOSTNAME
        elif hostname == "dev":
            self.HOSTNAME = DEVELOPMENT_HOSTNAME  # note: only Predata staff users will be able to access
        else:
            raise PredataPythonClientExeception("Unsupported Host: %s" % hostname)

        if not token and not (username and password):
            raise PredataPythonClientExeception("No authentication credentials provided")

        self.session = requests.Session()

        if token:
            self._token_auth(token)
        elif (username and password):
            self._basic_auth(username, password)

        self.MAX_NUMBER_OF_RETRIES = MAX_NUMBER_OF_RETRIES

    def _token_auth(self, token):
        """
        Add token authentication to session
        """
        self.session.headers.update({"Authorization": "Token %s" % token})

    def _basic_auth(self, username, password):
        """
        Add basic authentication cookies to session
        """
        encoded_string = base64.b64encode("%s:%s" % (username, password))
        self.session.headers.update({"Authorization": "Basic %s" % encoded_string})

    def signals(self):
        """
        Access signals client.
        """
        if not self.signal_client:
            self.signal_client = PredataSignalClient(self.session, self.HOSTNAME, self.API_BASE,
                                                     self.MAX_NUMBER_OF_RETRIES)
        return self.signal_client

    def data(self):
        """
        Access data client.
        """
        if not self.data_client:
            self.data_client = PredataDataClient(self.session, self.HOSTNAME, self.API_BASE,
                                                 self.MAX_NUMBER_OF_RETRIES)
        return self.data_client

    def analysis(self):
        """
        Access analysis client.
        """
        if not self.analysis_client:
            self.analysis_client = PredataAnalysisClient(self.session, self.HOSTNAME, self.API_BASE,
                                                         self.MAX_NUMBER_OF_RETRIES)
        return self.analysis_client

    def users(self):
        """
        Access user client.
        """
        if not self.user_client:
            self.user_client = PredataUserClient(self.session, self.HOSTNAME, self.API_BASE, self.MAX_NUMBER_OF_RETRIES)
        return self.user_client
