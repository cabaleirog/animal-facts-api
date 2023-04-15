"""
ANIMALSSSSSSSSSSSSSSSSSSSSss
"""
import random
from typing import List

from fastapi import APIRouter

from src.api.models.animal import FactModel

from src.api.utils.operations import Operator
from src.api.models.http.body import RequestBody
from src.api.models.animal import FactModel

router = APIRouter(prefix="/fact", tags=["Animal"])


@router.get(
    path="/",
    status_code=200,
    response_model=FactModel,
    name="Get a list of all bird facts",
    description="Get a list of all bird facts",
)
async def get_random(animal: str | None):
    """
    Get a random fact of an animal
    """
    if animal is None:
        return FactModel(**Operator.get_random())

    return FactModel(**Operator.get_random_by_animal(animal=animal))


# @router.get(
#    path="/",
#    response_model=FactModel,
#    description="Get a specific fact based on an id",
#    name="Get a specific fact",
# )
# async def specific_fact(id: int):  # pylint: disable=redefined-builtin, invalid-name
#    """
#    Returns the fact of a specific animal with the requested id.
#    """
#    row = Operator.get_one(_id=id)
#    _id, fact, animal = row
#    return FactModel(id=_id, fact=fact, animal=animal)
#
#
# @router.get(
#    path="/",
#    response_model=FactModel,
#    description="Get a random fact about an animal",
#    name="Get random fact",
# )
# async def random_fact(animal: str):  # pylint: disable=redefined-builtin, invalid-name
#    """
#    Returns the fact of a specific animal with the requested id.
#    """
#    row = Operator.get_one(_id=id)
#    _id, fact, animal = row
#    return FactModel(id=_id, fact=fact, animal=animal)
#
#
# @router.post(
#    path="/",
#    response_model=FactModel,
#    description="Create a new Bird fact",
#    name="Create a new Bird fact",
# )
# async def bird_add_fact(request: RequestBody):
#    """
#    Add a new fact for birds!
#    """
#    result = Operator.create(table=Operator.BIRDS_TABLE, request_body=request)
#    print(result)
#    return FactModel(id=1, fact="w")
#

# API -> DB

# API - return facts about animals
# GET /fact -> [....] | GET ALL
# GET /fact?id=1 -> 1 fact | GET ONE
# GET /fact?animal=dog -> 1 RANDOM dog fact | GET RANDOM


# CRUD

# API tests

# DEVOPS

# AUTOMATE tests..
