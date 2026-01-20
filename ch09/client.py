import requests

URL = "http://localhost:9002/graphql"

query_document = """
{
    allIngredients {
        name
    }
}
"""

results = requests.get(URL, params={'query': query_document})

print(results.json())
