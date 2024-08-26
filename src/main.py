from fastapi import FastAPI
from library.views import router as library_router

app = FastAPI()
app.include_router(library_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
