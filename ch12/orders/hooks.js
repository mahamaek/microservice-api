const hooks = require('hooks');
const http = require('http');

let responseStash = {};

// Helper function to create an order synchronously (mimicking 'requests.post')
function createOrderSync(callback) {
    const data = JSON.stringify({
        order: [{ product: "espresso", size: "small", quantity: 1 }]
    });

    const options = {
        hostname: '127.0.0.1',
        port: 8000,
        path: '/orders',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': data.length
        }
    };

    const req = http.request(options, (res) => {
        let body = '';
        res.on('data', (chunk) => body += chunk);
        res.on('end', () => {
            const parsed = JSON.parse(body);
            callback(parsed.id);
        });
    });

    req.write(data);
    req.end();
}

// --- 201 Save ID ---
hooks.after('/orders > Creates an order > 201 > application/json', (transaction) => {
    const body = JSON.parse(transaction.real.body);
    responseStash['created_order_id'] = body.id;
});

// --- 200/204 Success Path Hooks ---
const successHooks = [
    '/orders/{order_id} > Returns the details of a specific order > 200 > application/json',
    '/orders/{order_id} > Replaces an existing order > 200 > application/json',
    '/orders/{order_id} > Deletes an existing order > 204'
];

successHooks.forEach((name) => {
    hooks.before(name, (transaction) => {
        const id = responseStash['created_order_id'];
        transaction.fullPath = `/orders/${id}`;
        transaction.request.uri = `/orders/${id}`;
    });
});

// --- Actions (Pay/Cancel) - Create Fresh Resource ---
['pay', 'cancel'].forEach((action) => {
    const name = action === 'pay' 
        ? '/orders/{order_id}/pay > Processes payment for an order > 200 > application/json'
        : '/orders/{order_id}/cancel > Cancels an order > 200 > application/json';

    hooks.before(name, (transaction, done) => {
        createOrderSync((id) => {
            transaction.fullPath = `/orders/${id}/${action}`;
            transaction.request.uri = `/orders/${id}/${action}`;
            done();
        });
    });
});

// --- 422 Failure Path Hooks ---

// NEW: GET Orders 422 (Invalid Query Param)
hooks.before('/orders > Returns a list of orders > 422 > application/json', (transaction) => {
    transaction.fullPath += "?limit=not-a-number";
    transaction.request.uri += "?limit=not-a-number";
});

// POST Create 422 (Invalid Body)
hooks.before('/orders > Creates an order > 422 > application/json', (transaction) => {
    transaction.request.body = JSON.stringify({
        order: [{ product: "espresso", size: "invalid-size" }]
    });
});

// Specific Resource 422 (Invalid UUID Format)
const failSpecificHooks = [
    '/orders/{order_id} > Returns the details of a specific order > 422 > application/json',
    '/orders/{order_id}/cancel > Cancels an order > 422 > application/json',
    '/orders/{order_id}/pay > Processes payment for an order > 422 > application/json',
    '/orders/{order_id} > Replaces an existing order > 422 > application/json',
    '/orders/{order_id} > Deletes an existing order > 422 > application/json'
];

failSpecificHooks.forEach((name) => {
    hooks.before(name, (transaction) => {
        const placeholder = "d222e7a3-6afb-463a-9709-38eb70cc670d";
        transaction.fullPath = transaction.fullPath.replace(placeholder, "invalid-uuid");
        transaction.request.uri = transaction.request.uri.replace(placeholder, "invalid-uuid");
    });
});