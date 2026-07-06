import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(1, "Data Prep", "9:00 - 9:25 AM", "25 min", "Database, schema, warehouse, and 10 operational tables loaded from CSV")

render_technologies_used([
    {"name": "Database & Schema", "description": "Snowflake's organizational hierarchy for objects. A database contains schemas, and schemas contain tables, views, and other objects.", "icon": "database"},
    {"name": "CSV File Format", "description": "Snowflake can infer schema and load data directly from CSV files hosted at HTTP URLs using file formats and COPY INTO commands.", "icon": "table_chart"},
    {"name": "Virtual Warehouse", "description": "Snowflake's compute engine. A warehouse provides the CPU and memory to execute queries and load data. Scales independently of storage.", "icon": "memory"},
])


PROMPT_1_1 = """Create the following Snowflake objects for our Port of Montreal AI workshop:

1. A database called PORT_MTL_AI
2. A schema called PORT_OPS inside that database
3. A stage called DATA in the schema PORT_OPS with a directory table and server side encryption
3. A warehouse called PORT_MTL_WH (size MEDIUM, auto-suspend after 60 seconds, auto-resume enabled)
4. Set the session context to use these objects

Execute all SQL and confirm each object was created."""

render_prompt("Prompt 1.1", "Create Database, Schema & Warehouse", PROMPT_1_1)

render_explanation("What this prompt does", """
Creates the foundational Snowflake objects:

```sql
CREATE DATABASE PORT_MTL_AI;
CREATE SCHEMA PORT_MTL_AI.PORT_OPS;
CREATE WAREHOUSE PORT_MTL_WH
  WAREHOUSE_SIZE = 'MEDIUM'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

USE DATABASE PORT_MTL_AI;
USE SCHEMA PORT_OPS;
USE WAREHOUSE PORT_MTL_WH;
```

**Why MEDIUM?** We're loading ~1,500 rows total — even X-SMALL would work. MEDIUM gives us comfortable headroom for the Cortex functions we'll use later. With AUTO_SUSPEND = 60 seconds, it will pause immediately after queries finish, minimizing credit usage.
""")


PROMPT_1_2 = """In PORT_MTL_AI.PORT_OPS, the 10 CSV files have been uploaded to an internal stage called DATA.

For all 10 tables (TERMINALS, VESSELS, CONTAINER_MANIFESTS, CARGO_INVOICES, RAIL_SCHEDULES, CRANE_UTILIZATION, TRUCK_QUEUE_TIMES, PORT_INCIDENT_LOGS, MARINE_SAFETY_REPORTS, CBSA_INSPECTION_REPORTS):

1. Create a file format (CSV with PARSE_HEADER=TRUE, FIELD_OPTIONALLY_ENCLOSED_BY='"')
2. Create the tables with appropriate column types inferred from the data. Ensure to convert the column names to uppercase.
3. Load the data

Use CREATE TABLE with INFER_SCHEMA from a stage and then COPY INTO them. The key requirement is that all 10 tables are created and populated.

Execute all SQL."""

st.markdown("""
**Before running the prompt below, download the 10 CSV files and upload them to the `DATA` stage:**

1. Download all files from [github.com/sfc-gh-snotebaert/coco-hol-montreal/tree/main/workshop_guide/data](https://github.com/sfc-gh-snotebaert/coco-hol-montreal/tree/main/workshop_guide/data):
   `terminals.csv`, `vessels.csv`, `container_manifests.csv`, `cargo_invoices.csv`, `rail_schedules.csv`, `crane_utilization.csv`, `truck_queue_times.csv`, `port_incident_logs.csv`, `marine_safety_reports.csv`, `cbsa_inspection_reports.csv`
2. Using Snowsight, use the Horizon Catalog to browse to the `PORT_MTL_AI.PORT_OPS.DATA` stage to upload all 10 files.
3. Then copy the prompt below into Cortex Code and execute.
""")

render_prompt("Prompt 1.2", "Load and Create Tables from CSV", PROMPT_1_2)

render_explanation("What this prompt does", """
Loads all 10 operational data tables from CSV files uploaded to the internal stage `DATA`. Cortex Code will use INFER_SCHEMA to detect column types automatically:

```sql
CREATE OR REPLACE FILE FORMAT csv_format
  TYPE = CSV
  PARSE_HEADER = TRUE
  FIELD_OPTIONALLY_ENCLOSED_BY = '"';

CREATE OR REPLACE TABLE TERMINALS
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(INFER_SCHEMA(
      LOCATION => '@PORT_MTL_AI.PORT_OPS.DATA/terminals.csv',
      FILE_FORMAT => 'csv_format'
    ))
  );

COPY INTO TERMINALS
  FROM @PORT_MTL_AI.PORT_OPS.DATA/terminals.csv
  FILE_FORMAT = csv_format;
```

**The 10 tables**:
| Table | Rows | Description |
|-------|------|-------------|
| TERMINALS | 5 | Montreal port terminals |
| VESSELS | 20 | Ships servicing the St. Lawrence |
| CONTAINER_MANIFESTS | 200 | Shipping manifests |
| CARGO_INVOICES | 300 | Commercial invoices |
| RAIL_SCHEDULES | 150 | CN/CP Rail schedules |
| CRANE_UTILIZATION | 400 | Crane performance metrics |
| TRUCK_QUEUE_TIMES | 300 | Truck gate queue data |
| PORT_INCIDENT_LOGS | 40 | Safety/operations incidents |
| MARINE_SAFETY_REPORTS | 20 | Marine safety narratives |
| CBSA_INSPECTION_REPORTS | 25 | Customs inspection reports |
""")


PROMPT_1_3 = """Run a query in PORT_MTL_AI.PORT_OPS that shows every table name and its row count, ordered by row count descending. Format it nicely."""

render_prompt("Prompt 1.3", "Verify All Data Tables", PROMPT_1_3)

render_explanation("What this prompt does", """
A quick verification query:

```sql
SELECT table_name, row_count
FROM PORT_MTL_AI.INFORMATION_SCHEMA.TABLES
WHERE table_schema = 'PORT_OPS'
  AND table_type = 'BASE TABLE'
ORDER BY row_count DESC;
```

You should see approximately **1,460 total rows** across 10 tables.
""")


render_key_concepts([
    {"term": "External Stage", "definition": "A named Snowflake object that points to an external location (S3, Azure Blob, GCS, or HTTP URL). Used to reference files for loading without moving them into Snowflake first."},
    {"term": "INFER_SCHEMA", "definition": "A Snowflake table function that automatically detects column names and types from files in a stage. Eliminates manual CREATE TABLE DDL for well-structured CSV/Parquet files."},
    {"term": "File Format", "definition": "A named object specifying how to parse files (CSV delimiters, headers, quoting, compression). Created once and reused across multiple COPY INTO operations."},
])

render_what_you_built([
    "PORT_MTL_AI database and PORT_OPS schema",
    "PORT_MTL_WH warehouse (Medium, auto-suspend 60s)",
    "10 operational data tables loaded from CSV (~1,460 total rows)",
])
