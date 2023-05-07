import pydantic


class User(pydantic.BaseModel):
    # user_name:      str
    access_token:   str