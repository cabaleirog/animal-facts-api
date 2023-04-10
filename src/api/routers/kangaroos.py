"""
Kangaroos module
"""

from fastapi import APIRouter, HTTPException, Response

from src.api.models.http.body import RequestBody
from src.api.models.http.headers import HeadRequestHeaders
from src.api.models.kangaroo import Kangaroo
from src.api.utils.operations import Operator

router = APIRouter(prefix="/kangaroos", tags=["Kangaroo"])

__ANIMAL_NAME = "kangaroos"


@router.get(
    path="/count",
    status_code=200,
    name="Get the count of kangaroo facts",
)
async def kangaroos_count():
    """
    Count of kangaroos.
    """
    return {"count": len(Operator.all_facts(fact_file_name=__ANIMAL_NAME))}


@router.get(
    path="/",
    response_model=list[Kangaroo],
    status_code=200,
    description="Get all kangaroos!",
    name="Get all kangaroos!",
)
async def kangaroos():
    """
    Retrieve facts about kangaroos
    """
    return Operator.all_facts(fact_file_name=__ANIMAL_NAME)


@router.get(
    path="/fact",
    response_model=Kangaroo,
    description="Get a random fact about a kangaroo",
    name="Get a random fact about a kangaroo",
)
async def kangaroo_fact():
    """
    Retrieve facts about kangaroos
    """
    return Operator.random_fact(fact_file_name=__ANIMAL_NAME)


@router.get(
    path="/{id}",
    response_model=Kangaroo,
    description="Get one of the kangaroos based on an ID",
    name="Get one kangaroo",
)
async def kangaroo_fact_id(id: int):  # pylint:disable=invalid-name, redefined-builtin
    """
    Retrieve facts about kangaroos
    """
    return Operator.fact_id(fact_file_name=__ANIMAL_NAME, fact_id=id)


@router.post(
    path="/",
    response_model=Kangaroo,
    description="Create a new kangaroo fact",
    name="Create a new kangaroo fact",
)
async def kangaroo_add_fact(request: RequestBody):
    """
    Add a new fact for kangaroos!
    """
    added_fact = Operator.add(file_name=__ANIMAL_NAME, request_body=request)
    return added_fact


@router.delete(
    path="/{id}",
    responses={
        204: {"Success": "The fact has been deleted"},
        404: {"Not Found": "ID could not be found"},
    },
    name="Delete a kangaroo",
)
async def kangaroo_delete(id: int):  # pylint:disable=invalid-name, redefined-builtin
    """
    Delete a kangaroo, given a ID
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
    name="Update a kangaroo",
)
async def kangaroo_update(
    id: int, request: RequestBody
):  # pylint:disable=invalid-name, redefined-builtin
    """
    Delete a kangaroo, given a ID
    """
    result = Operator.update(
        file_name=__ANIMAL_NAME, animal_id=id, request_body=request
    )

    if result == "404":
        raise HTTPException(
            status_code=404, detail="You can only delete facts that have an id!"
        )

    return {"id": id, "fact": request.fact}
