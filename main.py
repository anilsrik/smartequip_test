import random
from fastapi import FastAPI, HTTPException, Query, Depends, Request
from fastapi_health import health
from pydantic import BaseModel
from typing import List
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware import Middleware
from starlette_context import context, plugins
from starlette_context.middleware import ContextMiddleware

#we cna use addtional logger if we want to override uvicorn logging
#from loguru import logger


#middleware to supprot requist ids. This will be helpful to track requests and thier corresponding reponse if needed
middleware = [Middleware(
    ContextMiddleware,
        plugins=(plugins.RequestIdPlugin(), plugins.CorrelationIdPlugin())
    )
]

app = FastAPI(middleware=middleware)

def is_service_healthy():
    return True

class ChallengeQueryParams:
    def __init__(
        self,
        count: int = Query(2, description="List count for the sum challenge"),
        min_val: int = Query(0, description="Minimum value allowed for the sum challenge"),
        max_val: int = Query(100, description="Maximum value allowed for the sum challenge"),
        floats: bool = Query(False, description="Do you need floating points for the sum challenge? Floating points are restricted to 2 decismals")
    ):
        self.count = count
        self.min_val = min_val
        self.max_val = max_val
        self.floats = floats

        if not 2 <= count <= 100:
            raise HTTPException(status_code=400, detail="Count Value must be within range (2,100) both included")

class ChallengeAns(BaseModel):
    input: List[float]
    ans: int


def getRandomNumbers(count,start,stop, is_int=True):
    randomList = []
    for _ in range(0,count):
        if is_int:
            randomList.append(random.randint(start,stop))
        else:    
            randomList.append(round(random.uniform(start,stop),2))
    return randomList

@app.get("/sumchallenge")
async def sumchallenge(params : ChallengeQueryParams = Depends()):
    randomList = getRandomNumbers(count=params.count, start = params.min_val, stop = params.max_val, is_int = not params.floats)
    return { "challenge" : "Please sum numbers " + ",".join(map(str, randomList)) }



@app.post("/validatesum")
async def validatesum(data : ChallengeAns):
    input_list = data.input
    sum_input = sum(input_list)
    if abs(sum_input - data.ans) < 10e-5:
        return {"message": "Good"}
    else:
        raise HTTPException(400, detail="Bad request. Answer incorrect")



app.add_api_route("/health", health([is_service_healthy]))