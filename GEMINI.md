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


# Vietstock Agent Documentation

## Directory Overview
This directory contains the foundational design, architecture, and requirements documentation for **Vietstock Agent**, a Multi-Agent Financial Advisor system. The system is designed to understand and answer questions from retail and institutional investors in the Vietnamese financial market. It leverages a multi-agent architecture (Market, Indicator, News, and Fundamental agents) combined with a Knowledge Graph and LLM reasoning to provide grounded investment insights. Currently, the directory serves as a knowledge base and planning workspace for the project.

## Key Files
*   **`require.md`**: Outlines the core functional requirements of the system, including ticker lookup, historical data retrieval, technical indicator calculation (SMA, RSI), sentiment analysis, and fundamental report synthesis.
*   **`architecture.md`**: Details the high-level system architecture, core design principles (LLMs for reasoning only, agents as single-task microservices), and the end-to-end execution flow (Router -> Planner -> Knowledge Graph -> Agents -> Advisor).
*   **`note.md`**: Contains specifications for data scraping strategies, data schemas, storage solutions (PostgreSQL, pgvector, Object Storage), and historical data volume requirements for the various agents.
*   **`vibe-trading-architecture.png`**: A visual representation of the project's trading/financial architecture.
*   **`Multi_Agent_Financial_Advisor.md`**: Supplementary documentation outlining the financial advisor concepts and use cases.

## Usage
This directory is intended to be used as the single source of truth for the system's design, architecture, and data engineering requirements. Developers and AI agents should refer to these Markdown files to understand the project's goals, structural constraints, data schemas, and agent interactions before beginning implementation. Any new architectural decisions, data source additions, or workflow modifications should be documented here to maintain alignment across the project.

## Environment & Dependency Management
- **No venv**: Do not use `venv` or `virtualenv` for environment management.
- **Use uv**: Use `uv` for all package installations and environment management tasks (e.g., `uv pip install`, `uv run`).