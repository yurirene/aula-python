from fastapi import FastAPI
from routes import cursos_router
from routes import usuarios_router

app = FastAPI()
app.include_router(cursos_router.router, tags=['cursos'])
app.include_router(usuarios_router.router, tags=['usuarios'])



if __name__ == '__main__' :
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)