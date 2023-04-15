# """
# Birds module
# """
# import random
# from typing import List
#
# from fastapi import APIRouter, HTTPException, Response
# from fastapi.responses import JSONResponse
#
## from src.api.models.bird import Bird
# from src.api.models.http.body import RequestBody
# from src.api.models.http.headers import HeadRequestHeaders
# from src.api.utils.messages import Message
# from src.api.utils.operations import Operator
#
#
# router = APIRouter(prefix="/birds", tags=["Birds"])
#
#
# @router.head(
#    path="/",
#    name="Get the amount of bird facts",
#    response_model=HeadRequestHeaders,
# )
# async def birds_head():
#    """
#    Amount of Bird facts.
#    """
#
#    count = Operator.get_count(table=Operator.BIRDS_TABLE)
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
#    response_model=List[Bird],
#    name="Get a list of all bird facts",
#    description="Get a list of all bird facts",
# )
# async def birds_get_all():
#    """
#    Get all bird facts dasdasdasdas
#    """
#    rows = Operator.get_all(table=Operator.BIRDS_TABLE)
#
#    return [Bird(id=_id, fact=fact) for _id, fact in rows]
#
#
# @router.get(
#    path="/fact",
#    response_model=Bird,
#    description="Get a random fact about a bird",
#    name="Get a random fact about a bird",
# )
# async def bird_fact():
#    """
#    Selects one random fact out of all facts.
#    """
#
#    rows = Operator.get_all(table=Operator.BIRDS_TABLE)
#    _id, fact = random.choice(rows)
#    return Bird(id=_id, fact=fact)
#
#
# @router.get(
#    path="/{id}",
#    response_model=Bird,
#    description="Get one of the birds based on an ID",
#    name="Get one bird",
#    responses={404: {"model": Message}},
# )
# async def bird_fact_id(id: int):  # pylint:disable=invalid-name, redefined-builtin
#    """
#    Target a specific row in the Database.
#    Return the fact object if the ID exists.
#
#    If it doesnt, return 404
#    """
#    result = Operator.get_one(table=Operator.BIRDS_TABLE, _id=id)
#    if result is None:
#        return JSONResponse(
#            status_code=404, content=Message(message="Item not found").dict()
#        )
#    _id, fact = result
#    return Bird(id=_id, fact=fact)
#
#
# @router.post(
#    path="/",
#    response_model=Bird,
#    description="Create a new Bird fact",
#    name="Create a new Bird fact",
# )
# async def bird_add_fact(request: RequestBody):
#    """
#    Add a new fact for birds!
#    """
#    result = Operator.create(table=Operator.BIRDS_TABLE, request_body=request)
#    print(result)
#    return Bird(id=1, fact="w")
#

# @router.delete(
#     path="/{id}",
#     responses={
#         204: {"Success": "The fact has been deleted"},
#         404: {"Not Found": "ID could not be found"},
#     },
#     name="Delete a bird",
# )
# async def bird_delete(id: int):  # pylint:disable=invalid-name, redefined-builtin
#     """
#     Delete a bird, given a ID
#     """
#     result = Operator.delete(file_name=__ANIMAL_NAME, animal_id=id)

#     if result == "404":
#         raise HTTPException(
#             status_code=404, detail="You can only delete facts that have an id!"
#         )

#     return Response(content="Fact deleted", status_code=204)


# @router.patch(
#     path="/{id}",
#     responses={
#         200: {"Success": "The fact has been updated"},
#         404: {"Not Found": "ID could not be found"},
#     },
#     name="Update a bird",
# )
# async def bird_update(
#     id: int, request: RequestBody
# ):  # pylint:disable=invalid-name, redefined-builtin
#     """
#     Delete a bird, given a ID
#     """
#     result = Operator.update(
#         file_name=__ANIMAL_NAME, animal_id=id, request_body=request
#     )

#     if result == "404":
#         raise HTTPException(
#             status_code=404, detail="You can only delete facts that have an id!"
#         )

#     return {"id": id, "fact": request.fact}
