import json

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/validate/deployments")
async def validate_deployments(request: Request) -> JSONResponse:
    """Admission webhook to validate deployments

    Parameters
    ----------
    request : Request
        See https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#request

    Returns
    -------
    JSONResponse
        See https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#response
    """  # noqa: E501
    body_raw = await request.body()
    print(f"body_raw: {body_raw}\n")
    body = json.loads(body_raw)
    uid = body["request"]["uid"]
    template_spec = body["request"]["object"]["spec"]["template"]["spec"]
    if (
        "securityContext" not in template_spec.keys()
        or "runAsNonRoot" not in template_spec["securityContext"]
        or template_spec["securityContext"]["runAsNonRoot"] is not True
    ):
        response_body = {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "uid": uid,
                "allowed": False,
                "status": {
                    "code": 403,
                    "message": "You must specify a securityContext "
                    "with runAsNonRoot set to `true`",
                },
            },
        }
    else:
        response_body = {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {"uid": uid, "allowed": True},
        }

    return JSONResponse(response_body, status_code=200)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
    )
