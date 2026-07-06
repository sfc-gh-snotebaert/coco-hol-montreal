# Plan: Session 01 CSV Loading Refactor

## Context

**Files involved:**
- [`workshop_guide/app_pages/session_01.py`](workshop_guide/app_pages/session_01.py) — main page with all prompt content
- [`workshop_guide/components.py`](workshop_guide/components.py) — `SESSION_PROMPTS` dict drives the completion-tracking checkboxes

**Key findings:**

- `render_prompt(prompt_id, title, text)` creates a bordered card with a "Done" checkbox keyed to `prompt_id`. Changing the ID string changes which checkbox key is tracked.
- `SESSION_PROMPTS[1]` in `components.py` lists the IDs that must all be checked for the session to count as complete. It must stay in sync with whatever `prompt_id` values are passed to `render_prompt`.
- The current `PROMPT_1_2` text tells Cortex Code to use a notebook with external access integrations and load directly from GitHub raw URLs — this fails on trial accounts.
- There is no existing "step description" component; adding a `st.markdown()` block before `render_prompt` is the right pattern (same page, no new component needed).

## Implementation Steps

### Task 1 — Update `SESSION_PROMPTS` in `components.py`

In `components.py` line 4, change:
```python
1: ["Prompt 1.1", "Prompt 1.2", "Prompt 1.3"],
```
to:
```python
1: ["Prompt 1.1", "Step 1.2", "Prompt 1.4"],
```

### Task 2 — Rename the `render_prompt` call (Prompt 1.2 → Step 1.2)

In `session_01.py` line 70, change:
```python
render_prompt("Prompt 1.2", "Load All Data Tables from CSV", PROMPT_1_2)
```
to:
```python
render_prompt("Step 1.2", "Load and Create Tables from CSV", PROMPT_1_2)
```

### Task 3 — Add download instruction block before Step 1.2

Insert a `st.markdown()` block immediately **before** the `render_prompt("Step 1.2", ...)` call. Content:

```
**Before running the prompt below, download the 10 CSV files and upload them to a Snowflake internal stage:**

1. Download each file by clicking the links in the table below.
2. In Snowsight, go to **Data > Add Data > Load files into a Stage**.
3. Create an internal stage named **`csv_stage`** in `PORT_MTL_AI.PORT_OPS`.
4. Upload all 10 downloaded files to that stage.
5. Then copy the prompt below into Cortex Code and execute.

| File | Download |
|------|----------|
| terminals.csv | [Download](https://github.com/sfc-gh-obenning/coco-hol-montreal/raw/refs/heads/main/workshop_guide/static/terminals.csv) |
| vessels.csv | [Download](https://github.com/sfc-gh-obenning/coco-hol-montreal/raw/refs/heads/main/workshop_guide/static/vessels.csv) |
| container_manifests.csv | [Download](https://github.com/sfc-gh-obenning/coco-hol-montreal/raw/refs/heads/main/workshop_guide/static/container_manifests.csv) |
| cargo_invoices.csv | [Download](https://github.com/sfc-gh-obenning/coco-hol-montreal/raw/refs/heads/main/workshop_guide/static/cargo_invoices.csv) |
| rail_schedules.csv | [Download](https://github.com/sfc-gh-obenning/coco-hol-montreal/raw/refs/heads/main/workshop_guide/static/rail_schedules.csv) |
| crane_utilization.csv | [Download](https://github.com/sfc-gh-obenning/coco-hol-montreal/raw/refs/heads/main/workshop_guide/static/crane_utilization.csv) |
| truck_queue_times.csv | [Download](https://github.com/sfc-gh-obenning/coco-hol-montreal/raw/refs/heads/main/workshop_guide/static/truck_queue_times.csv) |
| port_incident_logs.csv | [Download](https://github.com/sfc-gh-obenning/coco-hol-montreal/raw/refs/heads/main/workshop_guide/static/port_incident_logs.csv) |
| marine_safety_reports.csv | [Download](https://github.com/sfc-gh-obenning/coco-hol-montreal/raw/refs/heads/main/workshop_guide/static/marine_safety_reports.csv) |
| cbsa_inspection_reports.csv | [Download](https://github.com/sfc-gh-obenning/coco-hol-montreal/raw/refs/heads/main/workshop_guide/static/cbsa_inspection_reports.csv) |
```

### Task 4 — Rewrite `PROMPT_1_2` text

Replace lines 44-68 with:

```python
PROMPT_1_2 = """In PORT_MTL_AI.PORT_OPS, the 10 CSV files have been uploaded to an internal stage called csv_stage.

For all 10 tables (TERMINALS, VESSELS, CONTAINER_MANIFESTS, CARGO_INVOICES, RAIL_SCHEDULES, CRANE_UTILIZATION, TRUCK_QUEUE_TIMES, PORT_INCIDENT_LOGS, MARINE_SAFETY_REPORTS, CBSA_INSPECTION_REPORTS):

1. Create a file format (CSV with SKIP_HEADER=1, FIELD_OPTIONALLY_ENCLOSED_BY='"')
2. Create the tables with appropriate column types inferred from the data
3. Load the data

Use CREATE TABLE with INFER_SCHEMA from a stage and then COPY INTO them. The key requirement is that all 10 tables are created and populated.

Execute all SQL."""
```

### Task 5 — Update the `render_explanation` block for Step 1.2

Replace the existing two-pattern explanation with a single internal-stage pattern:

```sql
CREATE OR REPLACE FILE FORMAT csv_format
  TYPE = CSV
  SKIP_HEADER = 1
  FIELD_OPTIONALLY_ENCLOSED_BY = '"';

CREATE OR REPLACE TABLE TERMINALS
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(INFER_SCHEMA(
      LOCATION => '@PORT_MTL_AI.PORT_OPS.csv_stage/terminals.csv',
      FILE_FORMAT => 'csv_format'
    ))
  );

COPY INTO TERMINALS
  FROM @PORT_MTL_AI.PORT_OPS.csv_stage/terminals.csv
  FILE_FORMAT = csv_format;
```

Keep the 10-table summary table (rows/description) as-is — it's still accurate.

### Task 6 — Rename Prompt 1.3 → Prompt 1.4

Line 114, change:
```python
render_prompt("Prompt 1.3", "Verify All Data Tables", PROMPT_1_3)
```
to:
```python
render_prompt("Prompt 1.4", "Verify All Data Tables", PROMPT_1_3)
```

(The variable name `PROMPT_1_3` can stay unchanged — it's internal.)

## Verification

After implementing:
1. Run `source .venv/bin/activate && streamlit run workshop_guide/streamlit_app.py`
2. Navigate to Session 1 and confirm:
   - Step 1.2 card renders with the download table above it (hyperlinks clickable)
   - Step 1.2 prompt code box shows the new internal-stage prompt text
   - Prompt 1.4 renders correctly
   - Checking "Done" on all three prompts (1.1, Step 1.2, Prompt 1.4) marks the session complete

## Critical Files

- [`workshop_guide/app_pages/session_01.py`](workshop_guide/app_pages/session_01.py) — all prompt content changes
- [`workshop_guide/components.py`](workshop_guide/components.py) — `SESSION_PROMPTS[1]` completion tracking
