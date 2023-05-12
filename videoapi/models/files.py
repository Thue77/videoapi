import pydantic
from typing import Optional

class file(pydantic.BaseModel):
    name:   str
    url:    str
    size:   Optional[float]
    length: Optional[float]

    # def is_folder

# file().dict