# This route is currently a mock for a landing page of the app
# It is most likely going to be featuring some statistics and summaries
# As well maybe with changelog

from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def get_root():
    return {"message": "Hello World!"}
