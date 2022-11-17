from unittest import result
from fastapi import APIRouter, status, Depends, HTTPException, Response
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.curso_model import CursoModel
from core.dependency import get_session

#Bypass warning SQLModel select
# from sqlmodel.sql.expression import Select, SelectOfScalar
# SelectOfScalar.inherit_cache = True
# Select.inherit_cache = True

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoModel)
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)
    db.add(novo_curso)
    await db.commit()
    return novo_curso

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[CursoModel])
async def get_cursos(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()
        return cursos

@router.get('/{curso_id}', status_code= status.HTTP_200_OK, response_model=CursoModel)
async def get_curso(curso_id: int, db:AsyncSession = Depends(get_session)) :
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso: CursoModel = result.scalar_one_or_none()
        if not curso:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')
        
        return curso

@router.put('/{curso_id}', status_code=status.HTTP_200_OK, response_model=CursoModel)
async def put_curso(curso_id: int, curso: CursoModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_update: CursoModel = result.scalar_one_or_none()
        if not curso:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não Encontrado')
        
        curso_update.titulo = curso.titulo
        curso_update.aulas = curso.aulas
        curso_update.horas = curso.horas

        await session.commit()
        return curso_update

@router.delete('/{curso_id}', status_code=204)
async def delete_curso(curso_id: int, db:AsyncSession = Depends(get_session)) :
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso: CursoModel = result.scalar_one_or_none()
        if not curso:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')
        
        await session.delete(curso)
        await session.commit()