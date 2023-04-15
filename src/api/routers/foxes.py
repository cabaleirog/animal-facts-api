# """
# Foxes module
# """
#
# from fastapi import APIRouter, HTTPException, Response
#
# from src.api.models.fox import Fox
# from src.api.models.http.body import RequestBody
# from src.api.models.http.headers import HeadRequestHeaders
# from src.api.utils.operations import Operator
#
# router = APIRouter(prefix="/fox", tags=["Fox"])
#
# __ANIMAL_NAME = "fox"
#
#
# @router.get(
#    path="/count",
#    status_code=200,
#    name="Get the count of fox facts",
# )
# async def foxs_count():
#    """
#    Count of foxs.
#    """
#    return {"count": len(Operator.all_facts(fact_file_name=__ANIMAL_NAME))}
#
#
# @router.get(
#    path="/",
#    response_model=list[Fox],
#    status_code=200,
#    description="Get all foxs!",
#    name="Get all foxs!",
# )
# async def foxs():
#    """
#    Retrieve facts about foxs
#    """
#    return Operator.all_facts(fact_file_name=__ANIMAL_NAME)
#
#
# @router.get(
#    path="/fact",
#    response_model=Fox,
#    description="Get a random fact about a fox",
#    name="Get a random fact about a fox",
# )
# async def fox_fact():
#    """
#    Retrieve facts about foxs
#    """
#    return Operator.random_fact(fact_file_name=__ANIMAL_NAME)
#
#
# @router.get(
#    path="/{id}",
#    response_model=Fox,
#    description="Get one of the foxs based on an ID",
#    name="Get one fox",
# )
# async def fox_fact_id(id: int):  # pylint:disable=invalid-name, redefined-builtin
#    """
#    Retrieve facts about foxs
#    """
#    return Operator.fact_id(fact_file_name=__ANIMAL_NAME, fact_id=id)
#
#
# @router.post(
#    path="/",
#    response_model=Fox,
#    description="Create a new fox fact",
#    name="Create a new fox fact",
# )
# async def fox_add_fact(request: RequestBody):
#    """
#    Add a new fact for foxs!
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
#    name="Delete a fox",
# )
# async def fox_delete(id: int):  # pylint:disable=invalid-name, redefined-builtin
#    """
#    Delete a fox, given a ID
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
#    name="Update a fox",
# )
# async def fox_update(
#    id: int, request: RequestBody
# ):  # pylint:disable=invalid-name, redefined-builtin
#    """
#    Delete a fox, given a ID
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
