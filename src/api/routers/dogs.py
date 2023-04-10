"""
Dogs module
"""

from fastapi import APIRouter, HTTPException, Response

from src.api.models.dog import Dog
from src.api.models.http.body import RequestBody
from src.api.models.http.headers import HeadRequestHeaders
from src.api.utils.operations import Operator

router = APIRouter(prefix="/dogs", tags=["Dogs"])

__ANIMAL_NAME = "dogs"


@router.get(
    path="/count",
    status_code=200,
    name="Get the count of dog facts",
)
async def dogs_count():
    """
    Count of dogs.
    """
    return {"count": len(Operator.all_facts(fact_file_name=__ANIMAL_NAME))}


@router.get(
    path="/",
    response_model=list[Dog],
    status_code=200,
    description="Get all dogs!",
    name="Get all dogs!",
)
async def dogs():
    """
    Retrieve facts about dogs
    """
    return Operator.all_facts(fact_file_name=__ANIMAL_NAME)


@router.get(
    path="/fact",
    response_model=Dog,
    description="Get a random fact about a dog",
    name="Get a random fact about a dog",
)
async def dog_fact():
    """
    Retrieve facts about dogs
    """
    return Operator.random_fact(fact_file_name=__ANIMAL_NAME)


@router.get(
    path="/{id}",
    response_model=Dog,
    description="Get one of the dogs based on an ID",
    name="Get one dog",
)
async def dog_fact_id(id: int):  # pylint:disable=invalid-name, redefined-builtin
    """
    Retrieve facts about dogs
    """
    return Operator.fact_id(fact_file_name=__ANIMAL_NAME, fact_id=id)


@router.post(
    path="/",
    response_model=Dog,
    description="Create a new dog fact",
    name="Create a new dog fact",
)
async def dog_add_fact(request: RequestBody):
    """
    Add a new fact for dogs!
    """
    added_fact = Operator.add(file_name=__ANIMAL_NAME, request_body=request)
    return added_fact


@router.delete(
    path="/{id}",
    responses={
        204: {"Success": "The fact has been deleted"},
        404: {"Not Found": "ID could not be found"},
    },
    name="Delete a dog",
)
async def dog_delete(id: int):  # pylint:disable=invalid-name, redefined-builtin
    """
    Delete a dog, given a ID
    """
    result = Operator.delete(file_name=__ANIMAL_NAME, animal_id=id)

    if result == "404":
        raise HTTPException(
            status_code=404, detail="You can only delete facts that have an id!"
        )

    return Response(content="Fact deleted", status_code=204)


@router.patch(
    path="/{id}",
    responses={
        204: {"Success": "The fact has been updated"},
        404: {"Not Found": "ID could not be found"},
    },
    name="Update a dog",
)
async def dog_update(
    id: int, request: RequestBody
):  # pylint:disable=invalid-name, redefined-builtin
    """
    Delete a dog, given a ID
    """
    result = Operator.update(
        file_name=__ANIMAL_NAME, animal_id=id, request_body=request
    )

    if result == "404":
        raise HTTPException(
            status_code=404, detail="You can only delete facts that have an id!"
        )

    return {"id": id, "fact": request.fact}
