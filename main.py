import requests
from time import time
from yapsy.IMultiprocessPlugin import IMultiprocessPlugin
from sonic_engine.util.functions import loadConfig, relative
from sonic_engine.model.log import LogOptions, Logger
from sonic_engine.core.database import __db__
from .config_types.extensions import InferenceCustomConfig, InferenceModelPipeline


class HelloWorldInferenceExtension(IMultiprocessPlugin):
    def __init__(self, p):
        IMultiprocessPlugin.__init__(self, p)

        # TODO: to be added as a simple function in the sonic engine
        self.config = loadConfig(InferenceCustomConfig, relative(
            __file__, './config.yaml'))

        __db__.register_extension(self.config)

        print("--> Hello World Inference Extension Loaded")

    def run(self):
        for model in self.config.models:
            print("Start")
            my_model = InferenceModelPipeline(**model)
            self._get_input(my_model)

    def _get_input(self, model: InferenceModelPipeline):

        for data in __db__.get_message():
            logger = Logger(self.config.log, __name__.split('.')[-1])
            i = 0
            t = time()
            url = model.url
            if data['type'] == 'message':
                if time() - t > 3:
                    logger.debug(f'{i} items processed')
                    t = time()
                    self._get_prediction_and_publish(
                        data['data'], url, i)
                    i += 1

    def _get_prediction_and_publish(self, data, url, id):

        ip_data = __db__.retrieve('ip_data', data)
        src_city = requests.get(f'{url}/{ip_data["src_ip"]}/city/').content
        dst_city = requests.get(f'{url}/{ip_data["dst_ip"]}/city/').content

        log = {
            'id': id,
            'timestamp': int(time()),
            'data': data.decode(),
            'prediction': {
                'src_city': src_city,
                'dst_city': dst_city
            },
            'url': url
        }

        print("--> Prediction: ", log)
        print("--> Data: ", data.decode())
        __db__.store('inference', id, log)

        for ch in self.config.channels.publish:
            __db__.publish(ch, id)
