import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(5, "CoWork", "11:00 - 11:15 AM", "15 min", "Collaborative AI analysis with CoWork")

render_technologies_used([
    {"name": "Snowflake CoWork", "description": "An AI-powered collaborative workspace inside Snowsight where you can analyze data, generate insights, and share findings with your team — all through natural language conversation.", "icon": "group"},
    {"name": "Data Analysis", "description": "CoWork can query your Snowflake data, generate visualizations, and provide insights without writing SQL. It understands your semantic views and table structures.", "icon": "analytics"},
    {"name": "Sharing & Collaboration", "description": "CoWork sessions can be shared with team members, creating a collaborative space for data exploration and decision-making.", "icon": "share"},
])


PROMPT_5_1 = """Open CoWork in Snowsight and start a new conversation about our Port of Montreal data.

In CoWork, ask the following questions to explore the data collaboratively:

1. "Show me an overview of the Port of Montreal operations — how many containers have we processed, what's our busiest terminal, and what's the average truck wait time?"

2. "Create a visualization showing TEU volume by terminal and month. Are there seasonal patterns?"

3. "What are the top safety concerns at the port based on incident data? Show me a breakdown by category and severity."

4. "Compare the crane utilization rates across terminals. Which terminals are operating most efficiently?"

Note: CoWork is accessed through Snowsight's left navigation panel. It provides a chat-based interface that can query your data, create charts, and generate insights without requiring you to write SQL.

Try these questions and observe how CoWork generates queries and visualizations automatically."""

render_prompt("Prompt 5.1", "Explore Data with CoWork", PROMPT_5_1)

render_explanation("What this prompt does", """
**CoWork** is Snowflake's collaborative AI workspace. Unlike Cortex Code (which executes prompts as SQL/Python), CoWork is designed for **interactive data exploration and team collaboration**.

**How CoWork differs from Cortex Code**:
- **Cortex Code**: Developer tool — executes SQL, creates objects, builds infrastructure
- **CoWork**: Analyst tool — explores data, generates visualizations, shares insights

**What CoWork does with these questions**:
1. Queries your tables automatically (it discovers PORT_MTL_AI.PORT_OPS tables)
2. Generates appropriate SQL behind the scenes
3. Creates visualizations (charts, tables) inline
4. Provides natural language explanations of the results

**Key capabilities**:
- Understands your semantic views and table relationships
- Creates charts and visualizations automatically
- Supports follow-up questions in context
- Can be shared with team members for collaborative analysis
""")


PROMPT_5_2 = """Continue in CoWork with more advanced analysis:

1. "Based on the incident data and crane utilization patterns, are there any terminals that seem to have both high utilization AND more safety incidents? Could overworked equipment be a factor?"

2. "Generate a summary report of port operations health that I could share with the port authority board. Include key metrics, trends, and areas of concern."

3. "What would you recommend as the top 3 operational improvements based on all the data you can see?"

Observe how CoWork maintains context from the previous questions and builds on earlier analysis. This is the collaborative intelligence pattern — AI that helps teams make decisions together."""

render_prompt("Prompt 5.2", "Advanced Analysis & Insights", PROMPT_5_2)

render_explanation("What this prompt does", """
Demonstrates CoWork's ability to:

**1. Cross-table analysis**: The first question requires joining incident data with crane utilization — CoWork should identify the correlation between high utilization and incidents.

**2. Report generation**: CoWork can synthesize multiple data points into a structured executive summary, combining quantitative metrics with qualitative observations.

**3. Recommendations**: Based on patterns in the data, CoWork generates actionable recommendations — this is the "intelligence" layer on top of raw analytics.

**The collaboration pattern**:
- CoWork maintains conversation context (like a smart analyst in a meeting)
- You can share the session with colleagues
- Team members can add their own questions
- The AI builds on everyone's exploration

**When to use CoWork vs. Cortex Code vs. Cortex Agent**:
| Tool | Best for |
|------|----------|
| Cortex Code | Building infrastructure, creating objects, writing SQL |
| CoWork | Exploring data, generating insights, team collaboration |
| Cortex Agent | End-user Q&A interface (deployed as a product) |
""")


render_key_concepts([
    {"term": "CoWork", "definition": "Snowflake's collaborative AI workspace for data exploration. Provides a conversational interface that queries data, creates visualizations, and generates insights. Designed for business analysts and team collaboration."},
    {"term": "Collaborative Intelligence", "definition": "The pattern where AI assists a team in making decisions together. CoWork sessions can be shared, allowing multiple people to ask questions, build on each other's analysis, and reach conclusions collectively."},
    {"term": "Context Maintenance", "definition": "CoWork maintains conversation history so follow-up questions build on previous analysis. Ask 'Show me TEU by terminal' then 'Now filter to just peak months' — it remembers the context."},
])

render_what_you_built([
    "Explored port operations data through conversational AI",
    "Generated visualizations and cross-table analysis",
    "Created an executive summary of port operations health",
    "Demonstrated the CoWork collaborative analysis pattern",
])
