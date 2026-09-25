from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="NexaCloud Mock Backend")


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"


class Customer(BaseModel):
    customer_id: str
    name: str
    email: str


class Subscription(BaseModel):
    subscription_id: str
    customer_id: str
    plan: str
    status: Literal["provisioning_error", "active"]
    monthly_price: int
    currency: str


class Payment(BaseModel):
    payment_id: str
    customer_id: str
    amount: int
    currency: str
    status: Literal["succeeded", "refunded"]
    description: str


TicketStatus = Literal["open", "in_progress", "resolved", "closed"]


class Ticket(BaseModel):
    ticket_id: str
    customer_id: str
    status: TicketStatus


class TicketUpdate(BaseModel):
    status: TicketStatus


customers = {
    "CUST-1001": Customer(
        customer_id="CUST-1001",
        name="Alex Morgan",
        email="alex.morgan@example.com",
    )
}

subscriptions = {
    "CUST-1001": Subscription(
        subscription_id="SUB-2001",
        customer_id="CUST-1001",
        plan="Pro",
        status="provisioning_error",
        monthly_price=999,
        currency="INR",
    )
}

payments = {
    "PAY-501": Payment(
        payment_id="PAY-501",
        customer_id="CUST-1001",
        amount=999,
        currency="INR",
        status="succeeded",
        description="Pro subscription",
    ),
    "PAY-502": Payment(
        payment_id="PAY-502",
        customer_id="CUST-1001",
        amount=999,
        currency="INR",
        status="succeeded",
        description="Pro subscription",
    ),
}

tickets = {
    "TICKET-1001": Ticket(
        ticket_id="TICKET-1001",
        customer_id="CUST-1001",
        status="open",
    )
}


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse()


@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str) -> Customer:
    customer = customers.get(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.get("/customers/{customer_id}/payments", response_model=list[Payment])
async def get_payments(customer_id: str) -> list[Payment]:
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail="Customer not found")
    return [payment for payment in payments.values() if payment.customer_id == customer_id]


@app.get("/customers/{customer_id}/subscription", response_model=Subscription)
async def get_subscription(customer_id: str) -> Subscription:
    subscription = subscriptions.get(customer_id)
    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription


@app.post("/payments/{payment_id}/refund", response_model=Payment)
async def refund_payment(payment_id: str) -> Payment:
    payment = payments.get(payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment.status == "refunded":
        raise HTTPException(status_code=409, detail="Payment is already refunded")
    payment.status = "refunded"
    return payment


@app.post("/customers/{customer_id}/subscription/activate", response_model=Subscription)
async def activate_subscription(customer_id: str) -> Subscription:
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail="Customer not found")
    subscription = subscriptions.get(customer_id)
    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    subscription.status = "active"
    return subscription


@app.get("/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: str) -> Ticket:
    ticket = tickets.get(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@app.patch("/tickets/{ticket_id}", response_model=Ticket)
async def update_ticket(ticket_id: str, update: TicketUpdate) -> Ticket:
    ticket = tickets.get(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket.status = update.status
    return ticket
