from fastapi import FastAPI

from database import engine
from library.views import router as library_router

app = FastAPI()
app.include_router(library_router)


if __name__ == "__main__":
    import uvicorn
    from library import db_models

    db_models.Base.metadata.create_all(bind=engine)
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
