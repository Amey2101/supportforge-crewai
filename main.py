import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from tools import (get_customer,get_payment_history,get_subscription,issue_refund,activate_subscription,)

load_dotenv()

# --- LLM config, isolated so we can swap models later ---
llm = LLM(
    model="openrouter/nex-agi/nex-n2.5-mini:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.2,
    max_tokens=1024,
)

# --- Agents ---
triage_agent = Agent(
    role="Support Triage Specialist",
    goal="Accurately classify incoming NexaCloud support tickets by category and severity",
    backstory=(
        "You are an experienced support triage specialist at NexaCloud, a SaaS company. "
        "You've read thousands of tickets and are excellent at quickly identifying what "
        "kind of problem a customer actually has, even when they describe multiple issues "
        "at once or use vague language."
    ),
    llm=llm,
    verbose=True,
)

investigation_agent = Agent(
    role="Customer Support Investigator",
    goal="Investigate the customer's issue using the information provided by the triage specialist and identify the likely cause.",
    backstory=(
        "You are an experienced customer support investigator at NexaCloud. "
        "You specialize in analyzing support cases after they have been triaged. "
        "You examine the reported symptoms, connect related issues, and determine "
        "what is most likely happening before a resolution is proposed."
    ),
    tools=[get_customer, get_payment_history, get_subscription],
    llm=llm,
    verbose=True,
)

resolution_agent = Agent(
    role="Customer Support Resolution Specialist",
    goal="Determine an appropriate resolution for the customer's issue based on the triage and investigation results.",
    backstory=(
        "You are a senior customer support resolution specialist at NexaCloud. "
        "You review investigated support cases and determine what should happen next. "
        "You consider the customer's reported problem, the investigation findings, "
        "and operational constraints when proposing a resolution."
    ),
    tools=[issue_refund,activate_subscription],
    llm=llm,
    verbose=True,
)

# --- Tasks ---
classify_ticket = Task(
    description=(
        "A customer submitted the following support ticket:\n\n"
        '"{ticket_text}"\n\n'
        "Identify the primary category (Billing, Refunds, Subscription, Account, "
        "Login/Auth, Technical, Feature Question, or Security), the severity "
        "(Low, Medium, High, Critical), and briefly explain your reasoning."
    ),
    expected_output=(
        "A short classification report with: Category, Severity, and a 1-2 sentence justification."
    ),
    agent=triage_agent,
)

investigate_ticket = Task(
    description=(
        "Investigate the customer's support issue using the original ticket "
        "and the available NexaCloud support tools.\n\n"
        "Customer ticket:\n"
        "{ticket_text}\n\n"
        "First determine what information must be verified. "
        "Use the available tools to retrieve relevant customer data, "
        "especially payment history when the issue involves billing. "
        "Base your conclusions on the data returned by the tools rather "
        "than assumptions.\n\n"
        "Identify the likely cause and explain how the verified data "
        "relates to the customer's reported problem."
    ),
    expected_output=(
        "A concise investigation report containing: "
        "Verified Facts, Likely Cause, and Relationship Between Issues."
    ),
    agent=investigation_agent,
    context=[classify_ticket],
)

resolve_ticket = Task(
    description=(
        "Resolve the customer's support ticket using the verified findings "
        "from the triage and investigation stages.\n\n"
        "If the investigation establishes that a refund is required, use "
        "the refund tool to process the appropriate duplicate payment. "
        "If the investigation establishes that the subscription needs "
        "activation, use the subscription activation tool.\n\n"
        "Only perform actions supported by the verified investigation findings. "
        "After attempting the necessary actions, report what was successfully "
        "executed and what, if anything, failed."
    ),
    expected_output=(
        "A resolution execution report containing: "
        "Actions Attempted, Actions Successfully Executed, "
        "Actions That Failed, and Final Case Status."
    ),
    agent=resolution_agent,
    context=[classify_ticket, investigate_ticket],
)

# --- Crew ---
support_crew = Crew(
    agents=[
        triage_agent,
        investigation_agent,
        resolution_agent,
    ],
    tasks=[
        classify_ticket,
        investigate_ticket,
        resolve_ticket,
    ],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    ticket = "Customer ID: CUST-1001\n""I was charged twice for my subscription and I still can't access the premium features."
    result = support_crew.kickoff(inputs={"ticket_text": ticket})
    print("\n\n=== FINAL OUTPUT ===")
    print(result)