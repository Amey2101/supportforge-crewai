
# SupportForge

**SupportForge** is an AI-powered customer support workflow built with **CrewAI**.

The project simulates how a SaaS company could use multiple specialized AI agents to investigate and resolve customer support tickets. Instead of building a simple chatbot, SupportForge focuses on **agent orchestration, task execution, context passing, tool calling, and interaction with external systems**.

The system uses a simulated SaaS backend called **NexaCloud** to provide customer, payment, and subscription data and to execute state-changing support actions.

---

## Overview

A customer support ticket passes through a sequence of specialized agents:


Customer Ticket
       │
       ▼
┌──────────────────────┐
│   Triage Agent       │
│                      │
│ Category + Severity  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Investigation Agent  │
│                      │
│ Examine account data │
│ using custom tools   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Resolution Agent     │
│                      │
│ Determine and        │
│ execute resolution   │
└──────────┬───────────┘
           │
           ▼
      CrewAI Tools
           │
           ▼
┌──────────────────────┐
│  NexaCloud API       │
│    (FastAPI)         │
│                      │
│ Customer / Payments  │
│ Subscription State   │
└──────────────────────┘

---

## Example Scenario

A customer submits:

"I was charged twice for my subscription and I still can't access the premium features."

SupportForge processes the ticket through multiple stages:

Triage — determines the ticket category and severity.
Investigation — retrieves customer, payment, and subscription information.
Resolution — determines the appropriate action based on the investigation.
Tool execution — performs authorized actions through the NexaCloud API.

Example tools available to the agents:

get_customer()
get_payment_history()
get_subscription()

issue_refund()
activate_subscription()

This allows the agents to interact with an external system rather than simply generating text.

---

## CrewAI Concepts Demonstrated

Agents

Specialized agents are responsible for different stages of the support workflow:

Support Triage Specialist
Customer Support Investigator
Customer Support Resolution Specialist
Tasks

Each agent receives a specific task containing:

Task description
Expected output
Context from previous tasks
Sequential Crew

The workflow uses CrewAI's sequential process:

Triage
  ↓
Investigation
  ↓
Resolution

The output of earlier tasks is passed into later stages as context.

Custom Tools

The agents interact with the NexaCloud backend through custom CrewAI tools.

Read Operations
get_customer()
get_payment_history()
get_subscription()
Write Operations
issue_refund()
activate_subscription()
External API Integration

The tools communicate with the FastAPI backend over HTTP:

CrewAI Agent
     ↓
CrewAI Tool
     ↓
HTTP Request
     ↓
FastAPI Backend
     ↓
JSON Response
     ↓
Agent
Agentic Tool Calling

The Resolution Agent has access to authorized tools and can decide when a backend action is required.

For example:

Resolution Agent
       ↓
"I need to activate the subscription"
       ↓
activate_subscription()
       ↓
POST /customers/{id}/subscription/activate
       ↓
Backend state changes

---

## Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Application development |
| **CrewAI** | Multi-agent orchestration |
| **OpenRouter** | LLM provider |
| **FastAPI** | Simulated NexaCloud backend |
| **Requests** | HTTP communication between tools and backend |

---

## Project Structure

supportforge-crewai/
│
├── main.py
│   └── CrewAI agents, tasks and crew
│
├── tools.py
│   └── Custom CrewAI tools for backend interaction
│
├── mock_backend/
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
│
├── .gitignore
└── README.md
Simulated NexaCloud Backend

The backend represents a fictional SaaS platform.

It exposes endpoints for:

Customer information
Payment history
Subscription information
Payment refunds
Subscription activation
Ticket management

Example customer state:

Customer
CUST-1001

Payments
PAY-501 → ₹999 → succeeded
PAY-502 → ₹999 → succeeded

Subscription
SUB-2001 → Pro → provisioning_error

The backend is intentionally simple and deterministic. Its purpose is to provide an external system that the CrewAI agents can interact with while learning agentic workflows.

Running the Project
1. Clone the Repository
git clone https://github.com/Amey2101/supportforge-crewai.git
cd supportforge-crewai
2. Create and Activate a Virtual Environment
python -m venv .venv

On Windows:

.venv\Scripts\activate
3. Install Dependencies

Install the required Python packages for CrewAI and the backend.

4. Configure Environment Variables

Create a .env file in the project root:

OPENROUTER_API_KEY=your_api_key_here

Never commit your .env file.

5. Start the NexaCloud Backend

From the project directory:

cd mock_backend
uvicorn main:app --reload

The API will be available at:

http://localhost:8000

Interactive API documentation:

http://localhost:8000/docs
6. Run SupportForge

Open another terminal:

cd supportforge-crewai
python main.py
What This Project Demonstrates

The primary goal of SupportForge is understanding the transition from a basic LLM application to an agentic system capable of interacting with external systems.

LLM
 ↓
Agent
 ↓
Tool
 ↓
External System
 ↓
State Change

The project demonstrates how an agentic application can combine:

Specialized agents
Task orchestration
Sequential execution
Context propagation
Tool calling
API integration
Read operations
Write operations
External state changes

The project is intentionally focused on the CrewAI orchestration layer, while the NexaCloud backend remains a lightweight simulated service.

Future Exploration

Potential extensions include:

Structured outputs
Guardrails
Human-in-the-loop approval
CrewAI memory
RAG / knowledge sources
CrewAI Flows
Parallel task execution
Error handling and retries
Persistence and resumability
Observability
MCP integration
A2A communication
FastAPI application layer
Automated testing
Disclaimer

SupportForge is an educational project built to explore CrewAI and agentic application architecture.

The NexaCloud backend is a simulated SaaS API and does not process real customer accounts, payments, or subscriptions.
