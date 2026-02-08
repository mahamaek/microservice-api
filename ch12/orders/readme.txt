# Running dredd to test orders api

./node_modules/.bin/dredd oas.yaml http://127.0.0.1:8000 --server "uvicorn orders.app:app"

./node_modules/.bin/dredd oas.yaml http://127.0.0.1:8000 --server "python -m uvicorn orders.app:app"