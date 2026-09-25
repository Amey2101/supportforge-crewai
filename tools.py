import requests
from crewai.tools import tool


@tool("get_payment_history")
def get_payment_history(customer_id: str) -> str:
    """Retrieve payment history for a NexaCloud customer."""

    response = requests.get(
        f"http://localhost:8000/customers/{customer_id}/payments"
    )

    response.raise_for_status()

    return response.text


@tool("get_customer")
def get_customer(customer_id: str) -> str:
    """Retrieve customer information from NexaCloud."""

    response = requests.get(
        f"http://localhost:8000/customers/{customer_id}"
    )

    response.raise_for_status()

    return response.text

@tool("get_subscription")
def get_subscription(customer_id: str) -> str:
    """Retrieve subscription information from NexaCloud."""

    response = requests.get(
        f"http://localhost:8000/customers/{customer_id}/subscription"
    )

    response.raise_for_status()

    return response.text

@tool("issue_refund")
def issue_refund(payment_id: str) -> str:
    """Issue a refund for a NexaCloud payment."""

    response = requests.post(
        f"http://localhost:8000/payments/{payment_id}/refund"
    )

    if response.status_code == 409:
        return f"Refund failed: payment {payment_id} has already been refunded."

    if response.status_code == 404:
        return f"Refund failed: payment {payment_id} was not found."

    response.raise_for_status()

    return response.text


@tool("activate_subscription")
def activate_subscription(customer_id: str) -> str:
    """Activate a NexaCloud customer's subscription."""

    response = requests.post(
        f"http://localhost:8000/customers/{customer_id}/subscription/activate"
    )

    if response.status_code == 404:
        return f"Activation failed: customer {customer_id} was not found."

    response.raise_for_status()

    return response.text


if __name__ == "__main__":
    result = activate_subscription.run("CUST-1001")
    print(result)

    