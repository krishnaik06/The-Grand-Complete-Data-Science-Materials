
# Importing dependent modules
from pydantic import BaseModel, conlist, constr
from typing import Optional

# Zeroshot prediction endpoint input scheme
class Item_zeroshot(BaseModel):
    title: str
    summary: constr(min_length=20)
    labels: Optional[conlist(str, min_items=2, max_items=10)] = None
    model: str
    
