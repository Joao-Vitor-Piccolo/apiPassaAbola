from pydantic import BaseModel

class SchemaMessage(BaseModel):
    message: str
