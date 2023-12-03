import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

from utils import *


class QueryBody(BaseModel):
    query: str
    temperature: float
    max_output_tokens: int
