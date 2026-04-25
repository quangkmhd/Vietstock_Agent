# CLAUDE.md


# Karpathy behavioral guidelines

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

<claude-mem-context>
# Memory Context from Past Sessions

*No context yet. Complete your first session and context will appear here.*
</claude-mem-context>

<!-- context7 -->
Use Context7 MCP to fetch current documentation whenever the user asks about a library, framework, SDK, API, CLI tool, or cloud service -- even well-known ones like React, Next.js, Prisma, Express, Tailwind, Django, or Spring Boot. This includes API syntax, configuration, version migration, library-specific debugging, setup instructions, and CLI tool usage. Use even when you think you know the answer -- your training data may not reflect recent changes. Prefer this over web search for library docs.

Do not use for: refactoring, writing scripts from scratch, debugging business logic, code review, or general programming concepts.

## Steps

1. Always start with `resolve-library-id` using the library name and the user's question, unless the user provides an exact library ID in `/org/project` format
2. Pick the best match (ID format: `/org/project`) by: exact name match, description relevance, code snippet count, source reputation (High/Medium preferred), and benchmark score (higher is better). If results don't look right, try alternate names or queries (e.g., "next.js" not "nextjs", or rephrase the question). Use version-specific IDs when the user mentions a version
3. `query-docs` with the selected library ID and the user's full question (not single words)
4. Answer using the fetched docs
<!-- context7 -->



This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository status
- This repository is currently a **documentation/spec workspace** (no application source tree yet).
- There are no detected build manifests or test runners (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.).
- Treat this repo as architecture + requirements source-of-truth for future implementation.

## Working commands (current repo)
Because this repo is docs-only right now, there are no project build/lint/test commands to run yet.

Useful local commands during doc updates:
- `ls -la` — inspect top-level docs
- `git status` — check doc changes (if/when repo is initialized as git)

When code is added later, update this file with:
- install/dependency command
- build command
- lint/type-check command
- full test command
- single-test command

## Key documents to read first
- `require.md` — product requirements for the Vietnamese market financial advisor.
- `architecture.md` — high-level multi-agent architecture and execution flow.
- `note.md` — data ingestion/storage/schema guidance.
- ` Multi_Agent_Financial_Advisor.md` — extended operational architecture (note: filename starts with a leading space).
- `vibe-trading-architecture.png` — visual architecture diagram.
- `GEMINI.md` — imported behavioral guidelines and short repo summary.

## High-level architecture (big picture)
The target system is a **multi-agent financial analysis and decision-support pipeline**:

1. **Interface layer**
   - CLI / Web UI / MCP client submits user question.

2. **Gateway + orchestration core**
   - FastAPI gateway (streaming responses), intent routing, planning, context building, memory/compression.

3. **Swarm orchestration / DAG execution**
   - Parallel specialized workers coordinated by a runtime/mailbox pattern.

4. **Specialized analyst agents**
   - Market Agent (OHLCV retrieval/trend)
   - Indicator Agent (SMA/RSI deterministic calculation)
   - News/Sentiment Agent (search, read, score, evidence)
   - Fundamental Agent (RAG over reports)
   - Portfolio/Advisor Agent (final synthesis and recommendation)

5. **Policy/compliance gate before final output**
   - Enforce disclaimer and evidence/citation quality before returning answer.

## Canonical execution flow
1. User question arrives.
2. Router classifies intent.
3. Planner expands to task graph + parameters (including defaults like RSI window/time range when missing).
4. Knowledge graph/context expansion identifies related entities (e.g., macro drivers).
5. Agents execute:
   - Parallel: market/news/fundamental branches.
   - Sequential dependency: market output feeds indicator calculations.
6. Shared context/state is merged.
7. Advisor synthesizes recommendation from structured outputs (rule + LLM explanation).
8. Compliance checks run.
9. Stream final response.

## Data architecture assumptions (from docs)
- **PostgreSQL** as primary store.
- Time-series price data table for OHLCV by ticker/date.
- Company profile table for issuer metadata.
- News table with ticker/macro tags and summarized content.
- Report files in object storage + chunked embeddings in vector-capable Postgres (e.g., `pgvector`) for RAG.

## Important implementation constraints
- Use LLM for reasoning/synthesis, not for deterministic math or raw DB retrieval logic.
- Keep agent responsibilities narrow and explicit.
- Prefer evidence-backed outputs with citations.
- Optimize for speed/token/correctness via:
  - parallel execution where independent,
  - cached computed features,
  - compressed shared context,
  - deterministic indicator calculations.
- **Environment Management**: Do not use `venv`. Use `uv` for all package installations and dependency management.

## Notes for future contributors
- If source code is introduced, add concrete developer commands immediately in this file.
- If architecture decisions change, update both `architecture.md` and this file to keep operational guidance aligned.