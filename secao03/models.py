from typing import Optional
from pydantic import BaseModel, validator

class Curso(BaseModel) :
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

    @validator('titulo')
    def validar_titulo(csl,value):
        palavras = value.split(' ')
        if (len(palavras) < 3):
            raise ValueError('O Titulo de Palavras deve ter 3 palavras')

