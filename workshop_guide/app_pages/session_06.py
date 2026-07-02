import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(6, "Streamlit", "11:15 - 11:30 AM", "15 min", "Operations dashboard with AI chat interface")

render_technologies_used([
    {"name": "Streamlit in Snowflake (SiS)", "description": "Deploy Python-based data apps directly within Snowflake. Apps run on container runtime with full Python package support, access data natively via Snowpark, and inherit Snowflake's security model.", "icon": "web"},
    {"name": "Compute Pool", "description": "A managed pool of container nodes that powers SiS apps. Provides CPU/GPU resources, auto-scales, and supports any Python package from pip.", "icon": "memory"},
    {"name": "st.connection(\"snowflake\")", "description": "The Streamlit connection API for Snowflake on container runtime. Returns a connection object with .session() for Snowpark. No credentials needed — inherits the logged-in user's session.", "icon": "terminal"},
])


PROMPT_6_1 = """In PORT_MTL_AI.PORT_OPS, create a Streamlit app called PORT_OPS_DASHBOARD that runs on the container runtime.

First, create a compute pool for the app:
- Name: PORT_MTL_COMPUTE_POOL
- Use the CPU_X64_S instance family
- Min and max nodes of 1

Then create the Streamlit app on that compute pool with these 2 pages:

PAGE 1 - Operations Dashboard:
- KPI cards at the top showing: Total TEUs (from CONTAINER_MANIFESTS), Active Vessels (count of distinct vessels), Avg Wait Time (from TRUCK_QUEUE_TIMES), CBSA Clearance Rate (% with status 'cleared' from CONTAINER_MANIFESTS)
- A bar chart of TEU volume by terminal (join CONTAINER_MANIFESTS to TERMINALS)
- A line chart showing daily container arrivals over time
- A table of recent incidents from PORT_INCIDENT_LOGS with severity color coding

PAGE 2 - Port Intelligence Chat:
- A chat interface where users can type natural language questions
- Uses our PORT_OPS_AGENT via SNOWFLAKE.CORTEX.AGENT() to answer questions
- Has a sidebar showing summary stats: total incidents, total TEUs, number of terminals

Important for container runtime:
- Create an External Access Integration that allows access to pypi.org and files.pythonhosted.org
- Create a network rule for these hosts, then an integration referencing it
- Set EXTERNAL_ACCESS_INTEGRATIONS on the Streamlit app
- Include a pyproject.toml with dependencies: ["streamlit[snowflake]>=1.50.0", "plotly"]
- Use st.connection("snowflake") for the Snowflake connection
- Make it visually clean with st.columns for layout

Execute all SQL to create the compute pool, stage the files, and deploy the app."""

render_prompt("Prompt 6.1", "Create the Streamlit App", PROMPT_6_1)

render_explanation("What this prompt does", """
Creates a full **Streamlit in Snowflake** application on the **container runtime**:

**Step 1 — Compute pool**:
```sql
CREATE COMPUTE POOL PORT_MTL_COMPUTE_POOL
  MIN_NODES = 1 MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_S;
```

**Step 2 — External Access Integration** (so container can install pip packages):
```sql
CREATE NETWORK RULE pypi_network_rule
  MODE = EGRESS TYPE = HOST_PORT
  VALUE_LIST = ('pypi.org', 'files.pythonhosted.org');

CREATE EXTERNAL ACCESS INTEGRATION pypi_access_integration
  ALLOWED_NETWORK_RULES = (pypi_network_rule) ENABLED = TRUE;
```

**Step 3 — Stage files and deploy**:
- Write streamlit_app.py, pages, and pyproject.toml to a stage
- Create the Streamlit object on the compute pool

**Page 1 — Operations Dashboard** pattern:
```python
conn = st.connection("snowflake")
session = conn.session()
teu_df = session.sql("SELECT SUM(teu_count) FROM CONTAINER_MANIFESTS").collect()
st.metric("Total TEUs", f"{teu_df[0][0]:,.0f}")
```

**Page 2 — Chat interface** uses `st.chat_input` and `st.chat_message` with the PORT_OPS_AGENT for responses.

**Key advantages of SiS**:
- **No data movement**: App runs inside Snowflake
- **Security**: Inherits user's role and permissions
- **No infrastructure**: Compute pool auto-manages lifecycle
""")


PROMPT_6_2 = """Show me the SQL to verify the Streamlit app and compute pool:

1. SHOW COMPUTE POOLS;
2. SHOW STREAMLITS IN SCHEMA PORT_MTL_AI.PORT_OPS;
3. Describe the streamlit PORT_OPS_DASHBOARD;

Also provide me with the direct URL to open the Streamlit app in Snowsight."""

render_prompt("Prompt 6.2", "Verify & Access the App", PROMPT_6_2)

render_explanation("What this prompt does", """
Verification and access:

**SHOW COMPUTE POOLS** — confirms the pool is ACTIVE with correct instance family.

**SHOW STREAMLITS** — lists the app with its URL endpoint.

**DESCRIBE STREAMLIT** — shows main file, compute pool (confirms container runtime), and status.

**Accessing the app**: SiS apps are accessible via Snowsight at:
```
https://app.snowflake.com/<account>/#/streamlit-apps/PORT_MTL_AI.PORT_OPS.PORT_OPS_DASHBOARD
```

**Sharing the app** with other roles:
```sql
GRANT USAGE ON STREAMLIT PORT_OPS_DASHBOARD TO ROLE <role_name>;
```

This completes the workshop — you've built a full AI-powered operations platform from data loading through to a deployed application, all in under 3 hours!
""")


render_key_concepts([
    {"term": "Container Runtime", "definition": "The current SiS execution environment. Apps run on a compute pool, support any Python package via pip, and use versioned stage syntax. Replaces the legacy warehouse runtime."},
    {"term": "Compute Pool", "definition": "A managed pool of container nodes. Choose an instance family (CPU_X64_S, GPU_NV_S, etc.), set min/max nodes, and Snowflake handles provisioning and scaling."},
    {"term": "External Access Integration", "definition": "Required for container runtime apps that install pip packages. Container nodes can't reach the internet by default — you must allow egress to pypi.org via network rules."},
    {"term": "Streamlit in Snowflake (SiS)", "definition": "Snowflake's native app framework for Python data apps. Apps run on Snowflake compute, access data via Snowpark, and inherit security model. Deployed as first-class Snowflake objects."},
])

render_what_you_built([
    "PORT_MTL_COMPUTE_POOL — compute pool for container runtime",
    "PORT_OPS_DASHBOARD — 2-page Streamlit app",
    "Operations Dashboard with KPIs, charts, and incident table",
    "AI-powered chat interface connected to PORT_OPS_AGENT",
])
