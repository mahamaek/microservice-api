from ariadne import make_executable_schema, gql, QueryType
from ariadne.asgi import GraphQL
import random
import string

schema = """
    type Query {
        hello: String
}
"""

query = QueryType()


@query.field('hello')
def resolve_hello(*_):
    return ''.join(random.choice(string.ascii_letters) for _ in range(10))


server = GraphQL(make_executable_schema(schema, [query]), debug=True)
