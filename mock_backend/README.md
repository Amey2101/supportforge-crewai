# NexaCloud Mock Backend

A small, deterministic FastAPI service with in-memory demo data. Data resets whenever the server restarts.

## Install dependencies

From the `supportforge` directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r mock_backend/requirements.txt
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`.

## Start the server

```bash
python -m uvicorn mock_backend.main:app --reload --host 127.0.0.1 --port 8000
```

The API is available at `http://localhost:8000`. Interactive API documentation is available at `http://localhost:8000/docs`.

## Test the endpoints

Check server health:

```bash
curl http://localhost:8000/health
```

Read the demo customer, payments, and subscription:

```bash
curl http://localhost:8000/customers/CUST-1001
curl http://localhost:8000/customers/CUST-1001/payments
curl http://localhost:8000/customers/CUST-1001/subscription
```

Refund a payment and activate the subscription:

```bash
curl -X POST http://localhost:8000/payments/PAY-501/refund
curl -X POST http://localhost:8000/customers/CUST-1001/subscription/activate
```

Refund requests are stateful. Repeating the `PAY-501` refund while the server is running returns HTTP `409`.

Read and update the demo ticket:

```bash
curl http://localhost:8000/tickets/TICKET-1001
curl -X PATCH http://localhost:8000/tickets/TICKET-1001 \
  -H "Content-Type: application/json" \
  -d '{"status":"resolved"}'
```

Restart the server to restore the initial demo state.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Check server health |
| `GET` | `/customers/{customer_id}` | Get a customer |
| `GET` | `/customers/{customer_id}/payments` | List a customer's payments |
| `GET` | `/customers/{customer_id}/subscription` | Get a customer's subscription |
| `POST` | `/payments/{payment_id}/refund` | Refund a succeeded payment |
| `POST` | `/customers/{customer_id}/subscription/activate` | Activate a customer's subscription |
| `GET` | `/tickets/{ticket_id}` | Get a ticket |
| `PATCH` | `/tickets/{ticket_id}` | Update a ticket status |

Unknown resources return HTTP `404`, repeated refunds return HTTP `409`, and invalid request data returns HTTP `422`.

## Demo IDs

- Customer: `CUST-1001` (Alex Morgan)
- Subscription: `SUB-2001`
- Payments: `PAY-501`, `PAY-502`
- Ticket: `TICKET-1001`
