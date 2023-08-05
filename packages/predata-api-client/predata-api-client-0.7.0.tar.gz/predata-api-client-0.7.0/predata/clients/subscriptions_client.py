from predata.clients.generic_client import PredataGenericClient


class PredataUserClient(PredataGenericClient):

    """
    Client for requesting Predata user information.
    """
    ROUTE = "subscriptions/"

    def list_subscriptions(self):
        """
        Return a list of all subscriptions.
        """
        endpoint = ""
        return {
            "result": self.make_request(endpoint)
        }
