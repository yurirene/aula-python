from operator import gt, lt
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from models import Curso
from fastapi import APIRouter
from fastapi import Path

router = APIRouter()

cursos = {
    1: {
        "titulo" : "Programação para Leigos",
        "aulas" : 112,
        "horas" : 58
    },

    2: {
        "titulo" : "Lógica de Programação",
        "aulas" : 87,
        "horas" : 67
    }
}

@router.get('/api/v1/cursos')
async def get_cursos() : 
    return cursos

@router.get('/api/v1/cursos/{curso_id}')
async def get_curso_by_id(curso_id : int = Path(default=None, title='ID do Curso', description = 'Deve ser entre 1 e 2', gt=0, lt=3)) : 
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')


@router.post('/api/v1/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso):
    next_id: int  = len(cursos) + 1
    cursos[next_id] = curso
    del curso.id
    return curso
    
@router.put('/api/v1/cursos/{curso_id}', status_code=status.HTTP_200_OK)
async def put_curso(curso_id: int, curso: Curso) : 
    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id
        return curso
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'não existe esse id {curso_id}')

@router.delete('/api/v1/cursos/{curso_id}')
async def delete_curso(curso_id: int):
    if curso_id in cursos:
        del cursos[curso_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id não encontrado')
