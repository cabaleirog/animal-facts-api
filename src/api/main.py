"""
The root APP to be extracted in our tests!
"""
from fastapi import FastAPI

from src.api.routers import \
    animal_router  # birds_router,; cats_router,; dogs_router,; foxes_router,; kangaroos_router,

app = FastAPI(version="1.0.0")

app.include_router(router=animal_router)
# app.include_router(router=birds_router)
# app.include_router(router=cats_router)
# app.include_router(router=dogs_router)
# app.include_router(router=foxes_router)
# app.include_router(router=kangaroos_router)


@app.get(path="/", status_code=200)
def root():
    """
    This is the root path
    """
    return {"msg": "Hello World!"}
