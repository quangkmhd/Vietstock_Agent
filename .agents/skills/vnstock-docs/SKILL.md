---
name: vnstock-docs
description: Use this skill whenever coding, debugging, or reviewing anything related to vnstock. It forces documentation-first lookup from local vnstock docs index and mapped files before writing code to avoid guessing APIs.
---

# Vnstock Documentation-First Skill

Use this skill to make vnstock implementation decisions based on local documentation, not memory.

## When to Use This Skill

Trigger this skill when user:
- Mentions `vnstock`, `vnstock3`, or asks for stock/financial data code using vnstock
- Asks to write or fix scripts that fetch market, company, financial, screener, macro, news, TA, or pipeline data
- Asks to migrate old vnstock code
- Requests API usage, method names, parameters, or examples related to vnstock

## Documentation Sources (Read in Order)

Always read these sources in sequence:

1. Index and mapping guide:
   - `/home/quangnhvn34/dev/me/Vietstock_Agent/docs/vnstock_docs_index.md`
2. Structured module docs folder:
   - `/home/quangnhvn34/dev/me/Vietstock_Agent/docs/vnstock_docs/`

Use the index file to pick exact target files before deep reading.

## Mandatory Workflow

### Step 1: Identify intent and map to doc files

From the user request, classify topic first, then map to files via `vnstock_docs_index.md`.

Quick mapping:
- V3 unified architecture/layers: `vnstocks.com_docs_vnstock-data_*.md`
- Legacy V2 domain APIs: `03-09` files and matching `vnstocks.com_docs_vnstock_*.md`
- Installation/migration/best practices: `02-installation.md`, `11-best-practices.md`, `12-migration-guide.md`
- TA: `vnstocks.com_docs_vnstock-ta_*.md`
- News: `vnstocks.com_docs_vnstock-news_*.md`
- Pipeline/realtime/storage: `vnstocks.com_docs_vnstock-pipeline_*.md`

### Step 2: Read only relevant files, but verify critical assumptions

Read the mapped files first. If uncertainty remains, expand to adjacent files in the same category.

Before generating code, verify:
- Correct module path and import style
- Correct method name and required parameters
- Applicable provider/layer constraints
- Whether request belongs to V3 style or legacy V2 migration path

### Step 3: Build evidence-backed implementation notes

Before coding, produce a short internal evidence summary from docs:
- Exact methods to use
- Required arguments
- Output shape assumptions
- Any caveats (provider support, limits, migration notes)

Do not invent unsupported methods or arguments.

### Step 4: Code with doc citations in response

When responding with code, include a short “Based on docs” section that names the source files used (paths or file names), so the user can verify quickly.

## Recommended Search Pattern

When scope is broad, use grep to narrow first, then read:

```bash
grep -Rin "<keyword>" /home/quangnhvn34/dev/me/Vietstock_Agent/docs/vnstock_docs
```

Example keywords:
- `ohlcv`, `quote`, `trades`
- `financial`, `balance`, `income`, `cashflow`
- `screener`, `macro`, `pipeline`, `websocket`, `migration`

## Quality Bar for vnstock Answers

A high-quality vnstock answer must:
- Reference the local index and at least one relevant vnstock doc file
- Use API names that exist in docs
- Distinguish V3 vs legacy guidance when relevant
- Avoid guessing undocumented behavior

If docs are missing or ambiguous, state uncertainty explicitly and ask a focused follow-up question.
