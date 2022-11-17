from operator import gt, lt
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from models import Curso
from fastapi import APIRouter
from fastapi import Path

router = APIRouter()


@router.get('/api/v1/usuarios')
async def get_usuarios() : 
    return {"info": "Todos os Usuários"}
