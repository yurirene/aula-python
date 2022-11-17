from typing import List
from unittest import result
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.curso_model import CursoModel
from schemas.curso_schema import CursoSchema
from core.dependency import get_session

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoSchema)
async def post_curso(curso: CursoSchema, db:AsyncSession = Depends(get_session)) :
    novo_curso = CursoModel(titulo=curso.titulo, aulas = curso.aulas, horas = curso.horas)
    
    db.add(novo_curso)
    await db.commit()

    return novo_curso

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[CursoSchema])
async def get_cursos(db: AsyncSession = Depends(get_session)) :
    async with db as session:    
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()

        return cursos

@router.get('/{curso_id}', response_model=CursoSchema, status_code=status.HTTP_200_OK)
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_session)) :
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso = result.scalar_one_or_none()
        if not curso:
            raise HTTPException(detail='Curso não Encontrado', status_code=status.HTTP_404_NOT_FOUND)
        return curso            

@router.put('/{curso_id}', response_model=CursoSchema, status_code=status.HTTP_200_OK)
async def put_curso(curso_id: int, curso: CursoSchema, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_up = result.scalar_one_or_none()
        if not curso:
            raise HTTPException(detail='Curso não encontrado', status_code=status.HTTP_404_NOT_FOUND)

        curso_up.titulo = curso.titulo
        curso_up.aulas = curso.aulas
        curso_up.horas = curso.horas

        await session.commit()
        return curso_up

@router.delete('/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)) :
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso = result.scalar_one_or_none()
        if not curso:
            raise HTTPException(detail='Curso não Encontrado', status_code=status.HTTP_404_NOT_FOUND)

        await session.delete(curso)
        await session.commit()
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)