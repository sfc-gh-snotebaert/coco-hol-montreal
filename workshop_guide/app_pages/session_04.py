import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(4, "Cortex Agents", "10:35 - 11:00 AM", "25 min", "Cortex Agent with Analyst + Search + custom tools")

render_technologies_used([
    {"name": "Cortex Agent (CREATE AGENT)", "description": "An orchestrating AI that plans tasks, selects tools (Analyst, Search, custom), executes them, reflects on results, and generates responses. Created as a first-class Snowflake object.", "icon": "smart_toy"},
    {"name": "Tool Orchestration", "description": "The Agent automatically routes questions to the right tool: Cortex Analyst for structured data, Cortex Search for unstructured documents, custom UDFs for business logic.", "icon": "route"},
    {"name": "Custom Tools (UDFs)", "description": "User-defined functions that extend Agent capabilities. The Agent can call any SQL UDF as a tool, enabling custom business logic and calculations.", "icon": "build"},
])


PROMPT_4_1 = """In PORT_MTL_AI.PORT_OPS, create a Cortex Agent called PORT_OPS_AGENT that port operations staff can use to ask questions about both structured data and unstructured documents.

It should:
- Use claude-sonnet-4-6 as the orchestration model
- Have two tools: the PORT_OPERATIONS_VIEW semantic view (for structured data queries) and the port_knowledge_search Cortex Search service (for safety docs and inspection reports)
- Include instructions that define it as the Port of Montreal Operations Assistant, guiding it to use the right tool for the question type — structured data tool for numbers/volumes/metrics, search tool for incidents/reports/documents
- Mention key domain context in the instructions: Canada's second-largest port on the St. Lawrence River, $100B annual trade, key terminals (Maisonneuve, Cast, Viau, Bickerdike, Racine), Seaway winter closure Dec-Mar, and support for English and French
- Include 3-4 sample questions that span both tools (e.g. TEU volumes, incident reports, CBSA inspections)

Execute and show confirmation."""

render_prompt("Prompt 4.1", "Create the Cortex Agent", PROMPT_4_1)

render_explanation("What this prompt does", """
Creates a **Cortex Agent** — an AI orchestrator that combines multiple data tools:

**CREATE AGENT anatomy**:

- **MODEL**: The LLM used for orchestration (planning, reflection, response generation). `claude-sonnet-4-6` is recommended for strong reasoning.

- **TOOLS**: The capabilities the agent can use:
  - **Cortex Search service** (`port_knowledge_search`): For searching unstructured documents
  - **Semantic view** (`PORT_OPERATIONS_VIEW`): For generating SQL queries from natural language

- **INSTRUCTIONS**: System prompt that shapes behavior, tone, and priorities:
  - Role definition ("You are the Port of Montreal Operations Assistant")
  - Tool routing guidance ("use structured data tool for numbers")
  - Behavioral guidelines (cite sources, emphasize safety)
  - Bilingual support (English + French)

- **SAMPLE_QUESTIONS**: Seed questions shown to users in the UI.

**How the Agent orchestrates**:
1. **Planning**: Receives user question, decides which tool(s) to use
2. **Tool execution**: Calls Analyst (generates + runs SQL) or Search (retrieves documents)
3. **Reflection**: Evaluates tool results — are they sufficient? Need another tool?
4. **Response**: Synthesizes a natural language answer from tool outputs
""")


PROMPT_4_2 = """Test our PORT_OPS_AGENT by running queries through SNOWFLAKE.CORTEX.AGENT(). Run these four queries one at a time:

1. Structured data query: "What are the busiest terminals by TEU count and which shipping lines dominate each terminal?"
2. Unstructured search query: "Have there been any environmental incidents or pollution events at the port? What was done about them?"
3. Mixed query (should use both tools): "Which terminals have had both the highest cargo volume AND the most safety incidents? Is there a correlation?"
4. Bilingual query: "Quels sont les principaux problemes de securite signales au port cette annee?"

For each, show the full response including which tools the agent chose to use."""

render_prompt("Prompt 4.2", "Test the Agent", PROMPT_4_2)

render_explanation("What this prompt does", """
Tests the Agent with four question types that exercise different tool routing:

1. **Pure structured** — routes to Cortex Analyst, generates SQL with GROUP BY terminal and shipping line
2. **Pure unstructured** — routes to Cortex Search, retrieves environmental incident documents
3. **Mixed** — requires BOTH tools: Analyst for cargo volume, Search for safety incidents, then combines
4. **Bilingual** — French question routed to English-language tools, response synthesized in French

**What to look for**:
- Which tools did the agent select for each question?
- Did the mixed query correctly use both tools?
- Was the French response coherent and accurate?

**Agent vs. RAG**: The RAG pattern in Session 3 was a single retrieve-then-generate pipeline. The Agent is smarter — it can decide to use Search, then Analyst, then Search again based on the question. It splits complex questions into sub-tasks.
""")


PROMPT_4_3 = """In PORT_MTL_AI.PORT_OPS, enhance our agent by adding a custom tool.

1. Create a UDF that calculates estimated port congestion risk:

CREATE OR REPLACE FUNCTION PORT_MTL_AI.PORT_OPS.CALCULATE_CONGESTION_RISK(
    terminal_name VARCHAR,
    teu_count NUMBER,
    arrival_month NUMBER
)
RETURNS VARIANT
LANGUAGE SQL
AS
$$
    SELECT OBJECT_CONSTRUCT(
        'terminal', terminal_name,
        'teu_count', teu_count,
        'risk_score',
            CASE
                WHEN arrival_month IN (7,8,9,10) AND teu_count > 1000 THEN 'HIGH'
                WHEN arrival_month IN (7,8,9,10) OR teu_count > 1000 THEN 'MEDIUM'
                ELSE 'LOW'
            END,
        'recommendation',
            CASE
                WHEN arrival_month IN (7,8,9,10) AND teu_count > 1000 THEN 'Pre-allocate additional berth slots and crane resources. Peak Seaway season.'
                WHEN arrival_month IN (7,8,9,10) OR teu_count > 1000 THEN 'Monitor queue times and prepare standby resources'
                ELSE 'Standard operations'
            END
    )
$$;

2. Test the UDF with sample inputs.

3. Recreate PORT_OPS_AGENT to include CALCULATE_CONGESTION_RISK as an additional tool alongside the existing Analyst and Search tools.

4. Test the enhanced agent with: "What is the congestion risk for a 2000 TEU shipment arriving at Maisonneuve Terminal in August?"

Execute all SQL and show results."""

render_prompt("Prompt 4.3", "Agent with Custom Tool", PROMPT_4_3)

render_explanation("What this prompt does", """
Extends the Agent with a **custom UDF tool**:

**Custom tools** allow Agents to go beyond Search and Analyst:
- Business calculations (congestion risk scoring)
- External API calls (via external access integrations)
- Data transformations (formatting, currency conversion)
- Workflow triggers (creating tickets, sending notifications)

**The UDF** implements a rule-based congestion risk calculator. Peak months for the Port of Montreal are July–October (before the St. Lawrence Seaway closes for winter in December).

**How the Agent uses custom tools**: When the user asks about congestion risk, the Agent:
1. Recognizes this matches the CALCULATE_CONGESTION_RISK function
2. Extracts parameters (terminal=Maisonneuve, TEU=2000, month=8)
3. Calls the UDF with those parameters
4. Incorporates the result into its response

**This is the "agentic" pattern**: The Agent doesn't just retrieve data — it takes actions, calls functions, and orchestrates workflows.
""")


render_key_concepts([
    {"term": "Cortex Agent", "definition": "A first-class Snowflake object that orchestrates LLMs, Cortex Analyst, Cortex Search, and custom tools to answer complex questions. Supports planning, tool use, reflection, and multi-turn conversations."},
    {"term": "Tool Routing", "definition": "The Agent's ability to select the appropriate tool for each question. Structured data -> Analyst, unstructured search -> Search, calculations -> custom UDFs. The LLM decides routing based on the question and tool descriptions."},
    {"term": "Custom Tools", "definition": "SQL UDFs or stored procedures registered as Agent tools. The Agent calls them with extracted parameters. Enables custom business logic, external integrations, and workflow automation."},
    {"term": "Multi-tool Orchestration", "definition": "When a question requires multiple tools (e.g., 'show me cargo volume AND safety incidents'), the Agent plans a sequence of tool calls, executes them, and synthesizes a combined answer."},
])

render_what_you_built([
    "PORT_OPS_AGENT — Cortex Agent with Analyst + Search tools",
    "Tested structured, unstructured, mixed, and bilingual queries",
    "CALCULATE_CONGESTION_RISK UDF as a custom tool",
    "Enhanced agent with three tool types (Analyst + Search + custom)",
])
