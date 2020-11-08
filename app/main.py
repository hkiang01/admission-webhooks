import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/validate/deployments")
async def validate_deployments(request: Request):
    # print(f"request: {str(request)}")
    print(f"headers: {request.headers}")
    body = await request.body()
    print(f"body: {body.decode()}")
    return JSONResponse(
        {"allowed": True, "status": {"message": "test admission webhook"}}
    )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8443,
        ssl_keyfile=os.environ["SSL_KEYFILE"],
        ssl_certfile=os.environ["SSL_CERTFILE"],
    )
