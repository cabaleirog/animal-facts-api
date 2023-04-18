"""
ANIMALSSSSSSSSSSSSSSSSSSSSss
"""

import re
from typing import List

from fastapi import APIRouter, HTTPException, Path, Query

from src.api.models.animal import AnimalEnum, FactModel
from src.api.models.http.body import AbstractRequestModel, RequestModel
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


@router.post(
    path="/",
    response_model=FactModel,
    status_code=201,
    name="Create a new fact",
    description="Create a new fact based on a animal type",
)
async def create_fact(request: RequestModel):
    """
    Create a new fact about an animal
    """
    # Sanity Check...
    if re.match("^[0-9]+$", request.fact):
        # Checks if the fact is all numerical or if it's actually text.
        # Does almost the same check as "".isdigit()
        raise HTTPException(
            status_code=406, detail="The fact provided, is not acceptable"
        )

    result = Operator.create(request_body=request)

    if result.get("ERROR"):
        raise HTTPException(status_code=403, detail=result.get("ERROR"))

    return FactModel(**result)


@router.delete(
    path="/{id}",
    status_code=204,
    response_model=None,
    name="Remove a fact about an animal.",
    description="Remove a fact.",
)
async def remove_fact_by_id(xid: int = Path(alias="id", ge=1)):
    """
    Remove a fact based on a given ID
    """
    result = Operator.remove_one(_id=xid)

    if result.get("ERROR"):
        raise HTTPException(status_code=404, detail="Did not find any fact")

    return None


@router.patch(
    path="/{id}",
    status_code=200,
    response_model=FactModel,
    name="Update a fact about an animal.",
    description="Update a fact, based on a specific ID.",
)
async def update_by_id(
    request: AbstractRequestModel, xid: int = Path(alias="id", ge=1)
):
    """
    Update a fact based on a given ID
    """
    # Sanity Check...
    if re.match("^[0-9]+$", request.fact):
        # Checks if the fact is all numerical or if it's actually text.
        # Does almost the same check as "".isdigit()
        raise HTTPException(
            status_code=406, detail="The fact provided, is not acceptable"
        )

    result = Operator.update_one(_id=xid, request=request)

    if result.get("ERROR"):
        raise HTTPException(status_code=404, detail=result.get("ERROR"))

    return FactModel(**result)
