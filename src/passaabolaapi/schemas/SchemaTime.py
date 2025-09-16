from pydantic import BaseModel

class SchemaTime(BaseModel):
    id: int
    nome: str

class SchemaGetTime(BaseModel):
    nome: str
