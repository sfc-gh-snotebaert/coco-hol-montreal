import streamlit as st

st.title("Port of Montreal AI Workshop")
st.markdown("Building Intelligence for Canada's Eastern Gateway with Snowflake Cortex")

st.space("small")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Annual trade", "$100B+", help="Port of Montreal annual trade value")
col2.metric("Sessions", "6", help="Hands-on lab sessions")
col3.metric("Prompts", "16", help="Total Cortex Code prompts")
col4.metric("Duration", "3 hrs", help="Total workshop time")

st.space("medium")

st.markdown("#### How this workshop works")

st.markdown("""
Each session has **numbered prompts** that you copy and paste directly into **Cortex Code**.
Cortex Code interprets your natural language instruction and executes the appropriate
SQL, Python, or configuration against your Snowflake account.

All prompts build on each other sequentially — run them in order throughout the morning.
""")

st.space("small")

st.markdown("#### The scenario")
with st.container(border=True):
    st.markdown("""
The **Port of Montreal** is Canada's second-largest port and the gateway to eastern North America,
handling over **$100 billion in goods annually**. Located 1,600 km inland on the St. Lawrence River,
it connects European and Mediterranean exporters with Canadian and US markets across Quebec, Ontario,
and the Midwest.

We'll build a complete AI platform covering:

| Data type | Examples |
|-----------|---------|
| **Structured** | Container manifests, shipping schedules, CBSA declarations, cargo invoices, CN/CP Rail schedules |
| **Unstructured** | CBSA inspection reports, marine safety reports, incident logs |
| **Time series** | Crane utilization, truck queue times |
""")

st.space("small")

st.markdown("#### What we're building")

with st.container(border=True):
    st.markdown("""
In 3 hours, we build a complete AI-powered operations platform:

**1. Data Foundation** — Load structured and unstructured port operations data into Snowflake from pre-generated CSV files.

**2. Natural Language Analytics** — Create a Semantic View over operational tables and query them with plain English/French via Cortex Analyst.

**3. Intelligent Search** — Build a Cortex Search service over safety documents and inspection reports for hybrid semantic + keyword search.

**4. AI Agents** — Create a Cortex Agent that orchestrates structured data queries AND document search through a single conversational interface.

**5. Collaborative AI** — Use CoWork to collaboratively analyze port data with AI assistance.

**6. Operations Dashboard** — Deploy a Streamlit app with live KPIs, charts, and an AI chat interface.
""")

st.space("small")

st.markdown("#### Prerequisites")
with st.container(border=True):
    st.markdown("""
- Snowflake account with **ACCOUNTADMIN** role — see **Getting Started** in the sidebar to provision a free trial
- **Cortex Code** open in Snowsight and connected to your account
- Cross-region inference enabled (for Cortex LLM functions)
""")

st.space("medium")
st.caption("Built for the July 7, 2026 workshop  :material/location_on:  Sid Lee Place #12102, Montréal, QC")
