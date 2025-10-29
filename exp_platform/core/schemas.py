from typing import Dict
from pydantic import BaseModel

class ExperimentConfig(BaseModel):
    model_id: str
    dataset_id: str
    params: Dict[str, object]
    run_dir: str
