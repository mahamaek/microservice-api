# Running dredd to test orders api

./node_modules/.bin/dredd oas.yaml http://127.0.0.1:8000 --server "uvicorn orders.app:app"

./node_modules/.bin/dredd oas.yaml http://127.0.0.1:8000 --server "uvicorn orders.app:app" --hookfile=./hooks.py --language=python

./node_modules/.bin/dredd oas.yaml http://127.0.0.1:8000 --server "python -m uvicorn orders.app:app"

# It is better to have the hooks in .js and use below command to run. the python was failing

./node_modules/.bin/dredd oas.yaml http://127.0.0.1:8000 --server "uvicorn orders.app:app" --hookfiles=./hooks.js