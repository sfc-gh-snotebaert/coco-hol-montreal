import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(3, "Cortex Search", "9:55 - 10:20 AM", "25 min", "Knowledge base, Cortex Search service, and RAG query pattern")

render_technologies_used([
    {"name": "Cortex Search Service", "description": "A managed hybrid search engine combining vector (semantic) and keyword search with automatic reranking. Created with a single SQL statement; handles embedding, indexing, and serving automatically.", "icon": "search"},
    {"name": "RAG (Retrieval Augmented Generation)", "description": "A pattern that retrieves relevant documents first, then passes them as context to an LLM for grounded answer generation. Reduces hallucination by anchoring responses in actual data.", "icon": "hub"},
    {"name": "SEARCH_PREVIEW", "description": "SQL function to query a Cortex Search Service. Supports text queries, column selection, filtering, and result limits. Returns JSON with ranked results.", "icon": "preview"},
])


PROMPT_3_1 = """In PORT_MTL_AI.PORT_OPS:

1. First, create a unified text table for search called PORT_KNOWLEDGE_BASE that combines:
   - PORT_INCIDENT_LOGS: incident_id as doc_id, 'incident_log' as doc_type, description_text || ' Resolution: ' || resolution_text as content, category as metadata_category, severity as metadata_priority, incident_date as doc_date
   - MARINE_SAFETY_REPORTS: report_id as doc_id, 'safety_report' as doc_type, report_text || ' Recommended: ' || recommended_actions as content, report_type as metadata_category, status as metadata_priority, report_date as doc_date
   - CBSA_INSPECTION_REPORTS: report_id as doc_id, 'inspection_report' as doc_type, findings_text as content, inspection_type as metadata_category, outcome as metadata_priority, inspection_date as doc_date

2. Then create a Cortex Search Service:
   CREATE OR REPLACE CORTEX SEARCH SERVICE port_knowledge_search
     ON content
     ATTRIBUTES metadata_category, metadata_priority, doc_type
     WAREHOUSE = PORT_MTL_WH
     TARGET_LAG = '1 hour'
     EMBEDDING_MODEL = 'snowflake-arctic-embed-l-v2.0'
     AS (
       SELECT doc_id, doc_type, content, metadata_category, metadata_priority, doc_date
       FROM PORT_KNOWLEDGE_BASE
     );

Execute all SQL. Then verify the service is created by running SHOW CORTEX SEARCH SERVICES."""

render_prompt("Prompt 3.1", "Create Cortex Search Service", PROMPT_3_1)

render_explanation("What this prompt does", """
Two major steps: building a unified knowledge base and creating a search service.

**Step 1 — PORT_KNOWLEDGE_BASE**: A UNION ALL table combining three document sources into a common schema:
- `doc_type` enables filtering by source (incidents vs. safety vs. inspections)
- `metadata_category` and `metadata_priority` become filter attributes
- Content is concatenated (description + resolution) for full context

**Step 2 — CREATE CORTEX SEARCH SERVICE**: This single SQL statement:

1. **Embeds** every row's `content` column using `snowflake-arctic-embed-l-v2.0`
2. **Indexes** both vector (semantic) and keyword (lexical) search
3. **Deploys** a low-latency serving endpoint
4. **Auto-refreshes** when source data changes (within TARGET_LAG)

**How hybrid search works**:
1. Query text is embedded into the same vector space
2. Vector similarity finds semantically similar documents
3. Keyword search finds lexically matching documents
4. A reranker combines and re-scores results
""")


PROMPT_3_2 = """In PORT_MTL_AI.PORT_OPS, query our port_knowledge_search service using SEARCH_PREVIEW with these searches:

1. Search: "equipment failure crane" - show top 3 results
2. Search: "oil spill environmental pollution" - show top 3 results
3. Search: "customs cargo discrepancy" filtered to doc_type = 'inspection_report' - show top 3 results
4. Search: "winter storm ice delay" - show top 3 results

Use this pattern for each:
SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'PORT_MTL_AI.PORT_OPS.port_knowledge_search',
    '{
      "query": "<search_query>",
      "columns": ["doc_id", "doc_type", "content", "metadata_category"],
      "limit": 3
    }'
  )
)['results'] as results;

Execute all 4 searches and show results."""

render_prompt("Prompt 3.2", "Query the Search Service", PROMPT_3_2)

render_explanation("What this prompt does", """
Four search queries demonstrating different capabilities:

1. **"equipment failure crane"** — Tests keyword + semantic overlap. Should find crane malfunction incidents even if they don't use the exact word "failure."

2. **"oil spill environmental pollution"** — Tests semantic search. Should find pollution incidents that describe "sheen," "contamination," or "discharge" without using "spill."

3. **"customs cargo discrepancy" with filter** — Tests **attribute filtering**:
```json
{
  "query": "customs cargo discrepancy",
  "columns": ["doc_id", "doc_type", "content"],
  "filter": {"@eq": {"doc_type": "inspection_report"}},
  "limit": 3
}
```

4. **"winter storm ice delay"** — Tests seasonal/weather concept matching across incident logs and safety reports.

**Why hybrid search matters**: Pure keyword search misses synonyms ("spill" vs "discharge"). Pure vector search can return semantically similar but factually irrelevant results. Cortex Search combines both with reranking.
""")


PROMPT_3_3 = """In PORT_MTL_AI.PORT_OPS, implement a RAG pattern that:

1. Takes a user question: "What are the most common safety incidents at Port of Montreal terminals and what preventive measures have been effective?"

2. First retrieves the top 5 most relevant documents from port_knowledge_search using SEARCH_PREVIEW

3. Then passes the retrieved context + question to SNOWFLAKE.CORTEX.COMPLETE() to generate a grounded answer:

WITH search_results AS (
    SELECT PARSE_JSON(
        SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
            'PORT_MTL_AI.PORT_OPS.port_knowledge_search',
            '{
                "query": "common safety incidents terminals preventive measures",
                "columns": ["doc_id", "doc_type", "content", "metadata_category"],
                "limit": 5
            }'
        )
    )['results'] AS results
),
context AS (
    SELECT LISTAGG(r.value:content::STRING, '\\n\\n---\\n\\n') AS combined_context
    FROM search_results, LATERAL FLATTEN(input => results) r
)
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'claude-sonnet-4-6',
    'You are a port safety expert at the Port of Montreal. Based ONLY on the following source documents, answer the user question. Cite specific incidents by their doc_id when referencing findings. If the documents do not contain enough information, say so.

SOURCE DOCUMENTS:
' || combined_context || '

USER QUESTION: What are the most common safety incidents at Port of Montreal terminals and what preventive measures have been effective?

Provide a structured answer with: 1) Common incident types, 2) Root causes, 3) Effective preventive measures, 4) Recommendations.'
) AS rag_response
FROM context;

Execute and show the RAG response."""

render_prompt("Prompt 3.3", "RAG Pattern: Search + Generate", PROMPT_3_3)

render_explanation("What this prompt does", """
Implements the full **RAG (Retrieval Augmented Generation)** pattern in a single SQL query:

**Step 1 — Retrieve**: SEARCH_PREVIEW finds the 5 most relevant documents.

**Step 2 — Augment**: LATERAL FLATTEN + LISTAGG combines retrieved documents into a single context string.

**Step 3 — Generate**: CORTEX.COMPLETE() receives context + question and generates a grounded answer.

**RAG architecture**:
```
User Question
     |
     v
[Cortex Search] --> Top 5 documents
     |
     v
[Context Assembly] --> "SOURCE DOCUMENTS: doc1... doc2..."
     |
     v
[LLM (COMPLETE)] --> Grounded answer with citations
```

**Why RAG works better than raw LLM**:
- **Reduces hallucination**: LLM answers "ONLY" from provided documents
- **Provides citations**: "Cite specific incidents by doc_id" enables traceability
- **Fresh data**: Search service reflects latest data; LLM knowledge is static
- **Domain-specific**: Your enterprise data isn't in the LLM's training set
""")


render_key_concepts([
    {"term": "Cortex Search Service", "definition": "A managed hybrid search engine created with SQL. Handles embedding, indexing (vector + keyword), reranking, and auto-refresh. Think of it as Elasticsearch-as-a-SQL-statement."},
    {"term": "RAG (Retrieval Augmented Generation)", "definition": "An AI pattern: (1) retrieve relevant documents from a knowledge base, (2) include them as context in an LLM prompt, (3) generate an answer grounded in the retrieved data. The standard pattern for enterprise AI chatbots."},
    {"term": "Hybrid Search", "definition": "Combining vector search (semantic similarity) with keyword search (exact/fuzzy text matching). Better than either alone because vector search catches synonyms while keyword search catches specific terms."},
    {"term": "LATERAL FLATTEN + LISTAGG", "definition": "LATERAL FLATTEN expands a JSON array into rows. LISTAGG concatenates row values into a single string. Together, they convert search result arrays into a context string for LLM prompts."},
])

render_what_you_built([
    "PORT_KNOWLEDGE_BASE — unified document table from 3 sources (85 documents)",
    "port_knowledge_search — Cortex Search service with hybrid search",
    "4 search queries demonstrating keyword, semantic, and filtered search",
    "Full RAG pipeline: retrieve + augment + generate in a single SQL query",
])
