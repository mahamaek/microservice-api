from ariadne import make_executable_schema, gql, QueryType
from ariadne.asgi import GraphQL
import random
import string
from web.schema import schema

server = GraphQL(schema,debug=True)
