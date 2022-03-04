class Cache:
    def __init__(self):
        """
        Below cache are NOT part of configuration (therefore states) because they;
            1) are so expensive to save!
            2) have to be independent of pickles
        """
        self._cache_data_table = {}
        self._cache_audit_results = None
        self._cache_response_model_for_presenter_connection = None
        self._connections_filtered = None

    @property
    def cache_data_table(self):
        return self._cache_data_table

    def set_cache_data_table(self, data_table):
        self._cache_data_table = data_table

    def clear_cache_data_table(self):
        self._cache_data_table = {}

    @property
    def cache_audit_results(self):
        return self._cache_audit_results

    @property
    def audit_results_are_cached(self) -> bool:
        return self._cache_audit_results is not None

    def clear_audit_results(self):
        self._cache_audit_results = None

    def set_cache_audit_results(self, audit_results):
        self._cache_audit_results = audit_results

    @property
    def cache_response_model_for_presenter_connection(self):
        return self._cache_response_model_for_presenter_connection

    @property
    def connection_model_is_cached(self) -> bool:
        return self._cache_response_model_for_presenter_connection is not None

    def set_connection_model(self, response_model_connection):
        self._cache_response_model_for_presenter_connection = response_model_connection

    def clear_connection_model(self):
        self._cache_response_model_for_presenter_connection = None

    @property
    def connections_filtered(self):
        return self._connections_filtered

    def set_connections_filtered(self, connections_filtered):
        self._connections_filtered = connections_filtered

    def clear_connections_filtered(self):
        self._connections_filtered = None

    @property
    def connections_filtered_are_cached(self) -> bool:
        return self._connections_filtered is not None
