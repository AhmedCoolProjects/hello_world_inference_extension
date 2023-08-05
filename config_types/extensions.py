from typing import List
from sonic_engine.util.dataclass import nested_dataclass
from sonic_engine.model.extension import ModelsPipeline, InferenceConfig


@nested_dataclass
class InferenceModelPipeline(ModelsPipeline):
    "Model extension configs"

    url: str = None


@nested_dataclass
class InferenceCustomConfig(InferenceConfig):
    "Custom Inference extension configs"

    models: List[InferenceModelPipeline]
