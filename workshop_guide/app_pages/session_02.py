import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(2, "Cortex Analyst & Semantic Views", "9:25 - 9:55 AM", "30 min", "Semantic view with relationships, metrics, and natural language queries")

render_technologies_used([
    {"name": "Cortex Analyst", "description": "Snowflake's text-to-SQL engine that converts natural language questions into SQL queries. Uses a semantic view to understand your data's business meaning, relationships, and metrics.", "icon": "chat"},
    {"name": "Semantic View", "description": "A first-class Snowflake object (CREATE SEMANTIC VIEW) that describes your data in business terms: tables, relationships, facts, dimensions, metrics, and synonyms. The bridge between natural language and SQL.", "icon": "description"},
    {"name": "AI_SQL_GENERATION", "description": "Custom instructions embedded in the semantic view that guide how Cortex Analyst generates SQL — providing domain context, business rules, and disambiguation hints.", "icon": "auto_fix_high"},
])


PROMPT_2_1 = """In PORT_MTL_AI.PORT_OPS, create a semantic view called PORT_OPERATIONS_VIEW for use with Cortex Analyst. It should cover these tables: CONTAINER_MANIFESTS, CARGO_INVOICES, RAIL_SCHEDULES, TERMINALS, VESSELS, CRANE_UTILIZATION, TRUCK_QUEUE_TIMES.

Include:
- Proper relationships between the tables (manifests join to terminals via destination_terminal = terminal_id, manifests join to vessels via vessel_id, invoices join to manifests via manifest_id, crane_utilization joins to terminals via terminal_id, truck_queue_times joins to terminals via terminal_id)
- Facts for all key numeric columns: container_count, teu_count, weight_tonnes, declared_value_cad, actual/estimated berth time hours, invoice values, moves_per_hour, utilization_pct, trucks_in_queue, avg_wait_minutes
- Dimensions for categorical columns like cargo_category, cbsa_declaration_status, terminal_name, shipping_line, railway, destination_city, weather_condition, operator_shift, and all date/time columns
- Add useful SYNONYMS on dimensions where users might use different terms (e.g. terminal_name could also be called 'dock' or 'berth', shipping_line could be 'carrier', cargo_category could be 'goods type')
- Metrics with pre-aggregated calculations: total TEU, total containers, average berth time, total trade value, shipment count, average crane utilization, average wait time
- Descriptive COMMENTs on every table, fact, dimension, and metric explaining the business meaning
- An AI_SQL_GENERATION instruction that provides domain context: this is Port of Montreal data on the St. Lawrence River, CBSA means Canada Border Services Agency, peak season is Jul-Oct (shipping season before Seaway winter closure), key terminals are Maisonneuve/Cast/Viau/Bickerdike/Racine, support English and French queries

Execute the SQL and confirm with DESCRIBE SEMANTIC VIEW."""

render_prompt("Prompt 2.1", "Create the Semantic View", PROMPT_2_1)

render_explanation("What this prompt does", """
Creates a **semantic view** — a first-class Snowflake object that enables natural language to SQL:

**Key components of a semantic view**:

- **TABLES**: Logical tables with aliases, primary keys, and comments
- **RELATIONSHIPS**: Foreign key joins between tables (e.g., manifests -> terminals)
- **FACTS**: Raw numeric columns available for computation (teu_count, weight_tonnes)
- **DIMENSIONS**: Categorical and temporal columns for grouping/filtering, with optional synonyms
- **METRICS**: Pre-defined aggregations (SUM, AVG, COUNT) that Cortex Analyst can use directly
- **AI_SQL_GENERATION**: Custom instructions that guide how Analyst generates SQL

**Synonyms** help Cortex Analyst understand different ways users refer to the same concept:
```sql
t.terminal_name ... WITH SYNONYMS = ('terminal', 'dock', 'berth')
```

**Facts vs Metrics**:
- Facts are raw columns (e.g., `teu_count`) — building blocks
- Metrics are pre-defined aggregations (e.g., `SUM(teu_count)`) — ready-to-use calculations
""")


PROMPT_2_2 = """Ask Cortex Analyst these questions using PORT_MTL_AI.PORT_OPS.PORT_OPERATIONS_VIEW:

1. "What are the top 5 terminals by total TEU volume?"
2. "Which shipping lines have the most containers with pending CBSA declarations?"
3. "What is the average truck queue wait time during peak hours vs off-peak?"
4. "Quels sont les terminaux les plus occupes par nombre de conteneurs?" (French query)

Show the generated SQL and results for each."""

render_prompt("Prompt 2.2", "Test with Natural Language Queries", PROMPT_2_2)

render_explanation("What this prompt does", """
Tests Cortex Analyst across different question types:

1. **"Top 5 terminals by TEU"** — Tests the `total_teu` metric and `terminal_name` dimension with a JOIN between manifests and terminals.

2. **"Pending CBSA by shipping line"** — Tests filtering on `cbsa_declaration_status` dimension and grouping by `shipping_line` with a JOIN to vessels.

3. **"Truck wait time peak vs off-peak"** — Tests the TRUCK_QUEUE_TIMES table with `is_peak_hour` as a grouping dimension and `avg_wait_minutes` as a fact.

4. **French query** — Tests bilingual support. The AI_SQL_GENERATION instruction told Analyst to support French, so it should correctly interpret "terminaux les plus occupes" as "busiest terminals."

**What to observe**: Look at the generated SQL — does it correctly identify which tables to join, which metrics to use, and how to filter? This demonstrates the power of the semantic layer.
""")


PROMPT_2_3 = """Now expand our PORT_OPERATIONS_VIEW semantic view in PORT_MTL_AI.PORT_OPS to also include the RAIL_SCHEDULES table with proper relationships and definitions.

1. Query INFORMATION_SCHEMA.COLUMNS to get the full schema of RAIL_SCHEDULES
2. Recreate PORT_OPERATIONS_VIEW with all original definitions plus RAIL_SCHEDULES, adding:
   - Relationship to TERMINALS via origin_terminal = terminal_id
   - Facts: num_containers, num_rail_cars
   - Dimensions: railway (with synonym 'rail company'), destination_city, cargo_type, status, delay_reason, departure/arrival datetimes
   - Metrics: total rail containers, average containers per train, delay rate (% with non-null delay_reason)
   - Appropriate comments

3. Test the expanded view by asking: "What percentage of rail shipments are delayed and what are the most common delay reasons?"

Execute all SQL and show the result."""

render_prompt("Prompt 2.3", "Expand the Semantic View", PROMPT_2_3)

render_explanation("What this prompt does", """
Demonstrates the **iterative semantic view development cycle**: expand the view, then immediately test.

**The expansion pattern**:
1. Check what columns exist in the new table via INFORMATION_SCHEMA
2. Recreate the view with CREATE OR REPLACE SEMANTIC VIEW
3. Add the new table, relationship, facts, dimensions, metrics
4. Test to confirm Analyst can now answer questions about rail data

**Key insight**: A semantic view is only as good as the tables and definitions it contains. When users ask about rail delays but RAIL_SCHEDULES isn't in the view, Analyst can't help. After expansion, it can.

**The delay rate metric** is interesting because it's a calculated metric:
```sql
METRIC delay_rate = COUNT_IF(delay_reason IS NOT NULL) / COUNT(*) * 100
```
This shows that metrics can be complex expressions, not just simple aggregations.
""")


render_key_concepts([
    {"term": "Cortex Analyst", "definition": "Snowflake's text-to-SQL engine. Takes natural language questions and generates SQL queries using a semantic view for context. Supports aggregations, joins, filtering, time-series analysis, and bilingual queries."},
    {"term": "Semantic View", "definition": "A first-class Snowflake object (CREATE SEMANTIC VIEW) that maps database tables to business concepts. Contains table definitions, relationships, facts, dimensions, metrics, synonyms, and AI instructions."},
    {"term": "Fact vs Dimension vs Metric", "definition": "Facts are raw numeric columns (teu_count). Dimensions are categorical/temporal columns for grouping and filtering (terminal_name, arrival_date). Metrics are pre-defined aggregations over facts (SUM(teu_count), AVG(wait_time))."},
    {"term": "AI_SQL_GENERATION", "definition": "Custom instructions embedded in the semantic view that guide SQL generation. Use this to provide domain-specific context, define business rules, and help with ambiguous terms."},
])

render_what_you_built([
    "PORT_OPERATIONS_VIEW semantic view with 7 tables and relationships",
    "Natural language queries in English and French",
    "Expanded view with RAIL_SCHEDULES and delay metrics",
    "Iterative semantic view development pattern",
])
