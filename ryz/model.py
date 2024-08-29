from pydantic import BaseModel


class Model(BaseModel):
    pass

class AbsModel(Model):
    class Config:
        arbitrary_types_allowed = True
