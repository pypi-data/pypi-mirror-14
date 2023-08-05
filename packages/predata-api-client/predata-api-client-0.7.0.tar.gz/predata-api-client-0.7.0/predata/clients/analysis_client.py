from predata.clients.generic_client import PredataGenericClient


class PredataAnalysisClient(PredataGenericClient):

    """
    Client for requesting Predata analysis information.
    """

    def list_country_drivers(self, country_code, date=None, n=None):
        """
        List top signal drivers for country overview signal.
        """
        endpoint = "analysis/drivers/countries/%s/" % country_code
        query_dict = {
            "n": n,
            "date": date.isoformat() if date else None,
        }
        return {
            "iso3": country_code,
            "date": date.isoformat() if date else None,
            "n": n if n else 3,
            "result": self.make_request(endpoint, query_dict=query_dict)
        }

    def list_topic_drivers(self, topic_id, date=None, n=None):
        """
        List top signal drivers for topic overview signal.
        """
        endpoint = "analysis/drivers/topics/%s/" % topic_id
        query_dict = {
            "n": n,
            "date": date.isoformat() if date else None,
        }
        return {
            "topic_id": topic_id,
            "date": date.isoformat() if date else None,
            "n": n if n else 3,
            "result": self.make_request(endpoint, query_dict=query_dict)
        }

    def list_country_predictions(self, country_code=None, date=None, maximum=False, prediction_type=None,
                                 prediction_window=None):
        """
        List country predictions.
        """
        endpoint = "analysis/predictions/countries/"
        query_dict = {
            "iso3": country_code,
            "date": date.isoformat() if date else None,
            "max": maximum,
            "heatmap_type": prediction_type,
            "prediction_window": prediction_window
        }
        return {
            "iso3": country_code,
            "date": date.isoformat() if date else None,
            "max": maximum,
            "prediction_type": prediction_type,
            "prediction_window": prediction_window,
            "result": self.make_request(endpoint, query_dict=query_dict, process_rpc=True)
        }

    def get_country_predictions(self, country_code, tag_id=None, tag_category_id=None, prediction_window=None,
                                start_date=None, end_date=None):
        """
        Retrieve a country and tag / tag_category prediction.
        """
        endpoint = "analysis/predictions_over_time/countries/"
        query_dict = {
            "iso3": country_code,
            "tag_id": tag_id,
            "tag_category_id": tag_category_id if tag_category_id and not tag_id else None,
            "heatmap_type": "strategic" if tag_category_id and not tag_id else None,
            "prediction_window": prediction_window,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None
        }
        return {
            "iso3": country_code,
            "tag_id": tag_id,
            "tag_category_id": tag_category_id,
            "heatmap_type": "strategic" if tag_category_id and not tag_id else None,
            "prediction_window": prediction_window,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "result": self.make_request(endpoint, query_dict=query_dict, process_rpc=True)
        }

    def list_topic_predictions(self, topic_id=None, date=None, maximum=False, prediction_type=None,
                               prediction_window=None):
        """
        List topic predictions.
        """
        endpoint = "analysis/predictions/topics/"
        query_dict = {
            "topic_id": topic_id,
            "max": maximum,
            "date": date.isoformat() if date else None,
            "heatmap_type": prediction_type,
            "prediction_window": prediction_window
        }
        return {
            "topic_id": topic_id,
            "date": date.isoformat() if date else None,
            "max": maximum,
            "prediction_type": prediction_type,
            "prediction_window": prediction_window,
            "result": self.make_request(endpoint, query_dict=query_dict, process_rpc=True)
        }

    def get_topic_predictions(self, topic_id, tag_id=None, tag_category_id=None, prediction_window=None,
                              start_date=None, end_date=None):
        """
        Retrieve a topic and tag / tag_category prediction.
        """
        endpoint = "analysis/predictions_over_time/topics/"
        query_dict = {
            "topic_id": topic_id,
            "tag_id": tag_id,
            "tag_category_id": tag_category_id if tag_category_id and not tag_id else None,
            "heatmap_type": "strategic" if tag_category_id and not tag_id else None,
            "prediction_window": prediction_window,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None
        }
        return {
            "topic_id": topic_id,
            "tag_id": tag_id,
            "tag_category_id": tag_category_id,
            "heatmap_type": "strategic" if tag_category_id and not tag_id else None,
            "prediction_window": prediction_window,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "result": self.make_request(endpoint, query_dict=query_dict, process_rpc=True)
        }

    def get_custom_predictions(self, event_set_ids, signal_set_ids, heatmap_type=None, prediction_window=None,
                               start_date=None, end_date=None):
        """
        Retrieve a custom prediction as defined by event sets and signal sets.
        """
        endpoint = "analysis/predictions_over_time/custom/"
        query_dict = {
            "event_set_ids": event_set_ids,
            "series_ids": signal_set_ids,
            "heatmap_type": heatmap_type,
            "prediction_window": prediction_window,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None
        }
        return {
            "event_set_ids": event_set_ids,
            "signal_set_ids": signal_set_ids,
            "heatmap_type": heatmap_type,
            "prediction_window": prediction_window,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "result": self.make_request(endpoint, query_dict=query_dict, encoding=True, process_rpc=True)
        }
