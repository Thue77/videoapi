import pydantic


class Token(pydantic.BaseModel):
    token_type:     str
    scope:          str
    expires_in:     int
    ext_expires_in: int
    access_token:   str