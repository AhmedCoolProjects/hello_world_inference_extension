import requests
from time import time
from yapsy.IMultiprocessPlugin import IMultiprocessPlugin
from sonic_engine.model.log import Logger
from sonic_engine.core.database import __db__
from .config_types.extensions import InferenceModelPipeline


class HelloWorldInferenceExtension(IMultiprocessPlugin):
    def __init__(self, p):
        IMultiprocessPlugin.__init__(self, p)

        data = p.recv()
        self.config = data["config"]
        message = data["message"]

        __db__.register_extension(self.config)

        print(f"{message}")

    def run(self):
        for model in self.config.models:
            my_model = InferenceModelPipeline(**model)
            self._get_input(my_model)

    def _get_input(self, model: InferenceModelPipeline):
        logger = Logger(self.config.log, __name__.split(".")[-1])

        for data in __db__.get_message():
            i = 0
            t = time()
            url = model.url
            if data["type"] == "message":
                if True:
                    logger.debug(f"{i} items processed")
                    t = time()
                    self._get_prediction_and_publish(data["data"], url, i)
                    i += 1

    def _get_prediction_and_publish(self, data, url, id):
        ip_data = __db__.retrieve("ip_data", data)
        url = f"{url}/{ip_data['src_ip']}"

        headers = {
            "accept": "application/json",
            "x-apikey": "705ff1ea0b1e1a8df9e7526cf8dc21a5787089df8529e1baba684d9b0dbc894f",
        }

        response = requests.get(url, headers=headers)
        response_json = response.json()
        log = {
            "id": id,
            "timestamp": int(time()),
            "data": data.decode(),
            "result": response_json,
            "url": url,
        }

        __db__.store("inference", id, log)

        for ch in self.config.channels.publish:
            __db__.publish(ch, id)
