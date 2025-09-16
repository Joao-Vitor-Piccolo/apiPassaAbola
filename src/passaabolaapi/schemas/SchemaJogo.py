from pydantic import BaseModel

class SchemaJogo(BaseModel):
    id: int
    time_1_id: int
    time_2_id: int
    gols_1: int
    gols_2: int
