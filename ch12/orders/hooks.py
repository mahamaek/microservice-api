import json
import dredd_hooks

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
