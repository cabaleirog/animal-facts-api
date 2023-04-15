# """
# Dogs module
# """
#
# from fastapi import APIRouter, HTTPException, Response
# from fastapi.responses import JSONResponse
# from src.api.models.dog import Dog
# from src.api.models.http.body import RequestBody
# from src.api.models.http.headers import HeadRequestHeaders
# from src.api.utils.operations import Operator
# import random
#
# router = APIRouter(prefix="/dogs", tags=["Dogs"])
#
# __ANIMAL_NAME = "dogs"
#
#
# @router.head(
#    path="/",
#    name="Get the amount of dogs facts",
#    response_model=HeadRequestHeaders,
# )
# async def dog_head():
#    """
#    Amount of dog facts.
#    """
#
#    count = Operator.get_count(table=Operator.DOGS_TABLE)
#
#    return JSONResponse(
#        content={"content-length": "0"},
#        headers={"count": f"{count[0] or 0}"},
#    )
#
#
# @router.get(
#    path="/",
#    status_code=200,
#    response_model=list[Dog],
#    name="Get a list of all dog facts",
#    description="Get a list of all dog facts",
# )
# async def dogs_get_all():
#    """
#    Get all dog facts
#    """
#    rows = Operator.get_all(table=Operator.DOGS_TABLE)
#
#    return [Dog(id=_id, fact=fact) for _id, fact in rows]
#
#
# @router.get(
#    path="/fact",
#    response_model=Dog,
#    description="Get a random fact about a dog",
#    name="Get a random fact about a dog",
# )
# async def dog_fact():
#    """
#    Selects one random fact about DOGS out of all facts.
#    """
#    rows = Operator.get_all(table=Operator.DOGS_TABLE)
#    _id, fact = random.choice(rows)
#    return Dog(id=_id, fact=fact)
#
#
# @router.get(
#    path="/{id}",
#    response_model=Dog,
#    description="Get one of the dogs based on an ID",
#    name="Get one dog",
# )
# async def dog_fact_id(id: int):  # pylint:disable=invalid-name, redefined-builtin
#    """
#    Retrieve facts about dogs
#    """
#    return Operator.fact_id(fact_file_name=__ANIMAL_NAME, fact_id=id)
#
#
# @router.post(
#    path="/",
#    response_model=Dog,
#    description="Create a new dog fact",
#    name="Create a new dog fact",
# )
# async def dog_add_fact(request: RequestBody):
#    """
#    Add a new fact for dogs!
#    """
#    added_fact = Operator.add(file_name=__ANIMAL_NAME, request_body=request)
#    return added_fact
#
#
# @router.delete(
#    path="/{id}",
#    responses={
#        204: {"Success": "The fact has been deleted"},
#        404: {"Not Found": "ID could not be found"},
#    },
#    name="Delete a dog",
# )
# async def dog_delete(id: int):  # pylint:disable=invalid-name, redefined-builtin
#    """
#    Delete a dog, given a ID
#    """
#    result = Operator.delete(file_name=__ANIMAL_NAME, animal_id=id)
#
#    if result == "404":
#        raise HTTPException(
#            status_code=404, detail="You can only delete facts that have an id!"
#        )
#
#    return Response(content="Fact deleted", status_code=204)
#
#
# @router.patch(
#    path="/{id}",
#    responses={
#        204: {"Success": "The fact has been updated"},
#        404: {"Not Found": "ID could not be found"},
#    },
#    name="Update a dog",
# )
# async def dog_update(
#    id: int, request: RequestBody
# ):  # pylint:disable=invalid-name, redefined-builtin
#    """
#    Delete a dog, given a ID
#    """
#    result = Operator.update(
#        file_name=__ANIMAL_NAME, animal_id=id, request_body=request
#    )
#
#    if result == "404":
#        raise HTTPException(
#            status_code=404, detail="You can only delete facts that have an id!"
#        )
#
#    return {"id": id, "fact": request.fact}
#
