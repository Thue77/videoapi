import pydantic
from typing import Optional

class file(pydantic.BaseModel):
    name:   str
    url:    str
    size:   float
    length: Optional[float]

# file().dict