from pydantic import BaseModel

class SchemaPostGol(BaseModel):
    jogo_id: int
    jogadora_id: int
