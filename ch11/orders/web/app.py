from orders.web.middlewares.authorization_middleware import AuthorizeRequestMiddleware
from pathlib import Path
import yaml
from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware


from orders.web.api.auth import decode_and_validate_token

app = FastAPI(debug=True, openapi_url="/openapi/orders.json",
              docs_url="/docs/orders")

oas_doc = yaml.safe_load(
    (Path(__file__).parent / "../../oas.yaml").read_text())

app.openapi = lambda: oas_doc

app.add_middleware(AuthorizeRequestMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from orders.web.api import api  # isort:skip  # noqa: E402
