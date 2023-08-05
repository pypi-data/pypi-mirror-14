from predata.clients.generic_client import PredataGenericClient


class PredataUserClient(PredataGenericClient):

    """
    Client for requesting Predata user information.
    """

    def list_user(self, group_id=None, full=True):
        """
        Return list of users.
        """
        endpoint = "users/"
        query_dict = {
            "group_id": group_id,
            "full": full
        }
        return {
            "group_id": group_id,
            "result": self.make_request(endpoint, query_dict=query_dict)
        }

    def get_user(self, user_id, full=True):
        """
        Get user information.
        """
        endpoint = "users/%s/" % user_id
        query_dict = {
            "full": full
        }
        return {
            "user_id": user_id,
            "result": self.make_request(endpoint, query_dict=query_dict)
        }

    def list_group(self):
        """
        Return list of groups.
        """
        endpoint = "groups/"
        return {
            "result": self.make_request(endpoint)
        }

    def get_group(self, group_id):
        """
        Get group information.
        """
        endpoint = "groups/%s/" % group_id
        return {
            "group_id": group_id,
            "result": self.make_request(endpoint)
        }

    def list_subscriptions(self):
        """
        Return a list of all subscriptions.
        """
        endpoint = "subscriptions/"
        return {
            "result": self.make_request(endpoint)
        }
