"""
ANIMALSSSSSSSSSSSSSSSSSSSSss
"""

from typing import List

from fastapi import APIRouter, HTTPException, Path, Query

from src.api.models.animal import AnimalEnum, FactModel
from src.api.utils.operations import Operator

router = APIRouter(prefix="/facts", tags=["Animal Facts"])


@router.get(
    path="/",
    status_code=200,
    response_model=List[FactModel],
    name="Retrieve all facts from the database",
    description="Get all facts",
)
async def get_all_facts(
    animal: AnimalEnum | None = Query(default=None),
) -> list[FactModel]:
    """
    Get a random fact of an animal
    """

    result = (
        Operator.get_all_for_animal(animal=animal.value)
        if animal
        else Operator.get_all()
    )

    if result[0].get("ERROR"):
        raise HTTPException(status_code=404, detail="Did not find any fact")

    return [FactModel(**x) for x in result]


@router.get(
    path="/random",
    status_code=200,
    response_model=FactModel,
    name="Retrieve a random animal fact",
    description="Get a random fact about an animal!",
)
async def random_fact(animal: AnimalEnum | None = Query(default=None)):
    """
    Get a random fact of an animal
    """
    result = (
        Operator.get_random_by_animal(animal=animal.value)
        if animal
        else Operator.get_random()
    )

    if result.get("ERROR"):
        raise HTTPException(status_code=404, detail="Did not find any fact")

    return FactModel(**result)


@router.get(
    path="/{id}",
    status_code=200,
    response_model=FactModel,
    name="Retrieve a fact about based on a given ID",
    description="Get a specific fact",
)
async def get_fact_by_id(xid: int = Path(alias="id", ge=1)):
    """
    Get a random fact of an animal that you specify in the PATH
    """
    result = Operator.get_one(_id=xid)

    if result.get("ERROR"):
        raise HTTPException(status_code=404, detail="Did not find any fact")

    return FactModel(**result)


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
