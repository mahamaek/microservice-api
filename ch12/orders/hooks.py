import json
import dredd_hooks
import requests

response_stash = {}


@dredd_hooks.after('/orders > Creates an order > 200 > application/json')
def save_created_order(transaction):
    response_payload = transaction['real']['body']
    order_id = json.loads(response_payload)
    response_stash['created_order_id'] = order_id


@dredd_hooks.before('/orders/{order_id} > Returns the details of a specific order > 200 > application/json')
def before_get_order(transaction):
    transaction["fullPath"] = f"orders/{response_stash['created_order_id']}"
    transaction["request"]["uri"] = f"orders/{response_stash['created_order_id']}"


@dredd_hooks.before("/orders/{order_id} > Replaces an existing order > 200 > " "application/json")
def before_put_order(transaction):
    transaction["fullPath"] = f"orders/{response_stash['created_order_id']}"
    transaction["request"]["uri"] = f"orders/{response_stash['created_order_id']}"


@dredd_hooks.before("/orders/{order_id} > Deletes an existing order > 204")
def before_delete_order(transaction):
    transaction["fullPath"] = f"orders/{response_stash['created_order_id']}"
    transaction["request"]["uri"] = f"orders/{response_stash['created_order_id']}"


@dredd_hooks.before(
    "/orders/{order_id}/pay > Processes payment for an order > 200 > "
    "application/json"
)
def before_pay_order(transaction):
    # using dredd to create resource befor test
    response = requests.post(
        "http://127.0.0.1:8000/orders",
        json={"order": [{"product": "string",
                         "size": "small", "quantity": 1}]},
    )

    id = response.json()['id']
    transaction["fullPath"] = f"orders/{id}/pay"
    transaction["request"]["uri"] = f"orders/{id}/pay"


@dredd_hooks.before(
    "/orders/{order_id}/cancel > Cancels an order > 200 > application/json"
)
def before_cancel_order(transaction):
    response = requests.post(
        "http://127.0.0.1:8000/orders",
        json={"order": [{"product": "string",
                         "size": "small", "quantity": 1}]},
    )

    id = response.json()['id']
    transaction["fullPath"] = f"orders/{id}/cancel"
    transaction["request"]["uri"] = f"orders/{id}/cancel"
