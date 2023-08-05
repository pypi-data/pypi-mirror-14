# Copyright (C) Bouvet ASA - All Rights Reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
import json
import requests
import urllib.parse

from .exceptions import PipeAlreadyExists, SystemAlreadyExists
from .dataset import Dataset
from .system import System
from .pipe import Pipe
from .log import Log
from . import utils


def quote_id_for_url(item_id):
    return urllib.parse.quote(urllib.parse.quote(item_id, safe=""), safe="")


class Connection:
    """This class represents a connection to a Sesam installation. This is the starting point of all interactions
    with the Sesam installation.
    """
    def __init__(self, sesamapi_base_url,
                 username=None, password=None,
                 client_certificate=None,
                 timeout=30):
        if not sesamapi_base_url.endswith("/"):
            sesamapi_base_url += "/"
        self.sesamapi_base_url = sesamapi_base_url
        self.username = username
        self.password = password
        self.timeout = timeout

        if self.username:
            auth = (self.username, self.password)
        else:
            auth = None

        headers = {
            "ACCEPT": "application/json,*/*"
        }

        self.session = session = requests.Session()
        if auth is not None:
            session.auth = auth
        if client_certificate is not None:
            session.cert = client_certificate
        session.headers = headers

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def _get_requests_kwargs(self):
        kwargs = {}
        if self.timeout:
            kwargs["timeout"] = self.timeout
        return kwargs

    def do_put_request(self, url, data=None, **kwargs):
        assert url is not None
        session_put_kwargs = self._get_requests_kwargs()
        session_put_kwargs.update(kwargs)
        return self.session.put(url, data=data, **session_put_kwargs)

    def do_get_request(self, url, allowable_response_status_codes=(200, 404), **kwargs):
        assert url is not None
        session_get_kwargs = self._get_requests_kwargs()
        session_get_kwargs.update(kwargs)
        response = self.session.get(url, **session_get_kwargs)
        utils.validate_response_is_ok(response, allowable_response_status_codes)
        return response

    def do_post_request(self, url, **kwargs):
        assert url is not None
        session_post_kwargs = self._get_requests_kwargs()
        session_post_kwargs.update(kwargs)
        return self.session.post(url, **session_post_kwargs)

    def do_delete_request(self, url, **kwargs):
        assert url is not None
        session_delete_kwargs = self._get_requests_kwargs()
        session_delete_kwargs.update(kwargs)
        return self.session.delete(url, **session_delete_kwargs)

    @property
    def pipes_url(self):
        return self.sesamapi_base_url + "pipes"

    def get_pipe_url(self, pipe_id):
        return self.pipes_url + "/" + quote_id_for_url(pipe_id)

    def get_pipe_config_url(self, pipe_id):
        return self.get_pipe_url(pipe_id) + "/config"

    @property
    def logs_url(self):
        return self.sesamapi_base_url + "logs"

    def get_log_url(self, log_id):
        return self.logs_url + "/" + quote_id_for_url(log_id)

    def get_pipe_pump_url(self, pipe_id):
        return self.get_pipe_url(pipe_id) + "/pump"

    def get_pipe_entities_url(self, pipe_id):
        return self.get_pipe_url(pipe_id) + "/entities"

    @property
    def systems_url(self):
        return self.sesamapi_base_url + "systems"

    def get_system_url(self, system_id):
        return self.systems_url + "/" + quote_id_for_url(system_id)

    def get_system_config_url(self, system_id):
        return self.get_system_url(system_id) + "/config"

    @property
    def stats_url(self):
        return self.sesamapi_base_url + "stats"

    @property
    def status_url(self):
        return self.sesamapi_base_url + "status"

    @property
    def datasets_url(self):
        return self.sesamapi_base_url + "datasets"

    def get_dataset_url(self, dataset_id):
        return self.datasets_url + "/" + quote_id_for_url(dataset_id)

    def get_dataset_entities_url(self, dataset_id):
        return self.get_dataset_url(dataset_id) + "/entities"

    def get_systems(self):
        systems = []

        # TODO: wrap in a utility-method and add error-detection
        response = self.do_get_request(self.systems_url, allowable_response_status_codes=[200])
        parsed_response = json.loads(response.text)

        for system_json in parsed_response:
            systems.append(System(self, system_json))

        return systems

    def get_system(self, system_id):
        response = self.do_get_request(self.get_system_url(system_id))
        if response.status_code == 404:
            return None
        system_json = json.loads(response.text)
        return System(self, system_json)

    def get_stats(self):
        """
        :return: A nested dict with metrics.
        """
        stats_response = self.do_get_request(self.stats_url, allowable_response_status_codes=[200])
        return stats_response.json()

    def get_status(self):
        """
        :return: A dict with various status-information (disk-usage, etc.)
        """
        status_response = self.do_get_request(self.status_url)
        return status_response.json()

    def get_datasets(self):
        datasets = []
        response = self.do_get_request(self.datasets_url, allowable_response_status_codes=[200])
        parsed_response = json.loads(response.text)
        for dataset_json in parsed_response:
            datasets.append(Dataset(self, dataset_json))
        return datasets

    def get_dataset(self, dataset_id):
        response = self.do_get_request(self.get_dataset_url(dataset_id), )
        if response.status_code == 404:
            return None
        dataset_json = json.loads(response.text)
        return Dataset(self, dataset_json)

    def get_pipes(self):
        pipes = []

        # TODO: wrap in a utility-method and add error-detection
        response = self.do_get_request(self.pipes_url, allowable_response_status_codes=[200])

        parsed_response = json.loads(response.text)

        for pipe_json in parsed_response:
            pipes.append(Pipe(self, pipe_json))
        return pipes

    def get_pipe(self, pipe_id):
        # TODO: wrap in a utility-method and add error-detection
        response = self.do_get_request(self.get_pipe_url(pipe_id))
        if response.status_code == 404:
            return None
        pipe_json = json.loads(response.text)
        return Pipe(self, pipe_json)

    def add_pipes(self, pipe_configs):
        response = self.do_post_request(self.pipes_url, json=pipe_configs)
        utils.validate_response_is_ok(response, allowable_response_status_codes=[201, 409])
        if response.status_code == 409:
            raise PipeAlreadyExists(response.text)

        pipe_json_list = json.loads(response.text)
        pipes = [Pipe(self, pipe_json) for pipe_json in pipe_json_list]
        return pipes

    def add_systems(self, system_configs):
        response = self.do_post_request(self.systems_url, json=system_configs)
        utils.validate_response_is_ok(response, allowable_response_status_codes=[201, 409])
        if response.status_code == 409:
            raise SystemAlreadyExists(response.text)

        system_json_list = json.loads(response.text)
        systems = [System(self, system_json) for system_json in system_json_list]
        return systems

    def get_logs(self):
        logs = []

        # TODO: wrap in a utility-method and add error-detection
        response = self.do_get_request(self.logs_url, allowable_response_status_codes=[200])
        parsed_response = json.loads(response.text)

        for log_json in parsed_response:
            logs.append(Log(self, log_json))
        return logs

    def get_log_content(self, log_id):
        """This returns a stream with the content of the specified logfile"""
        # TODO: wrap in a utility-method and add error-detection
        response = self.do_get_request(self.get_log_url(log_id), stream=True)
        if response.status_code == 404:
            return None
        return response.raw
