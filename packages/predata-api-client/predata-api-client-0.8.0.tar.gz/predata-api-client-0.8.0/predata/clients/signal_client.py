from predata.clients.generic_client import PredataGenericClient


class PredataSignalClient(PredataGenericClient):

    """
    Client for requesting Predata signals.
    """

    def _handle_special_endpoints(self, endpoint, maximum, normalized):
        if maximum:
            endpoint += "max/"
        elif normalized:
            endpoint += "norm/"
        return endpoint

    def get_source_signal(self, source_id, signal_type="aggregate", date=None, maximum=False, normalized=False):
        """
        Get source signal by source id.

        Accepts difference signal type ("aggregate", "chatter", "contestation", "users")
        """
        endpoint = "signals/source/%s/" % signal_type
        endpoint = self._handle_special_endpoints(endpoint, maximum, normalized) + "?source_id=%s" % (source_id)
        query_dict = {
            "date": date.isoformat() if date else date
        }
        return {
            "source": source_id,
            "signal_type": signal_type,
            "max": maximum,
            "normalized": normalized,
            "date": date,
            "result": self.make_request(endpoint, query_dict=query_dict)
        }

    def list_source_signals(self, source_id):
        """
        Return all signals associated with source
        """
        endpoint = "data/sources/%s/" % source_id
        return {
            "source_id": source_id,
            "result": self.make_request(endpoint)["signal_types"]
        }

    def get_country_signal(self, country_code, signal_type="aggregate", date=None, maximum=False, normalized=False):
        """
        Get country signal by country code.
        """
        endpoint = "signals/country/%s/" % signal_type
        endpoint = self._handle_special_endpoints(endpoint, maximum, normalized) + "?iso3=%s" % country_code
        query_dict = {
            "date": date.isoformat() if date else date
        }
        return {
            "country": country_code,
            "max": maximum,
            "normalized": normalized,
            "date": date,
            "result": self.make_request(endpoint, query_dict=query_dict)
        }

    def list_country_signals(self, country_code):
        """
        Return all signal types associated with country
        """
        endpoint = "data/countries/%s/" % country_code
        return {
            "country_code": country_code,
            "result": self.make_request(endpoint)["signal_types"]
        }

    def get_topic_signal(self, topic_id, signal_type="aggregate", date=None, maximum=False, normalized=False):
        """
        Get topic signal by topic_id.
        """
        endpoint = "signals/topic/%s/" % signal_type
        endpoint = self._handle_special_endpoints(endpoint, maximum, normalized) + "?topic_id=%s" % topic_id
        query_dict = {
            "date": date.isoformat() if date else date
        }
        return {
            "topic": topic_id,
            "max": maximum,
            "normalized": normalized,
            "date": date,
            "result": self.make_request(endpoint, query_dict=query_dict)
        }

    def list_topic_signals(self, topic_id):
        """
        Return all signal types associated with topic
        """
        endpoint = "data/topics/%s/" % topic_id
        return {
            "topic_id": topic_id,
            "result": self.make_request(endpoint)["signal_types"]
        }

    def get_asset_prices(self, asset_id):
        """
        Get asset signal / prices.
        """
        endpoint = "data/assets/prices/?asset_id=%s" % asset_id
        return {
            "asset_id": asset_id,
            "result": self.make_request(endpoint)
        }
