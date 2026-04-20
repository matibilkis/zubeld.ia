# Build Plan: Intent-Aware `init-orch --suggest`

## Goal
Extend `init-orch --suggest` so it can optionally use a short user or agent brief as additional input, without treating a transient task prompt as the repo's source of truth.

The core product principle should remain:

- `init-orch.md` is the canonical repo-level orchestration contract
- repo files and existing orchestration artifacts are the main evidence
- user or agent intent is an optional, explicit input that helps shape a better first ansatz

This means the feature should support things like:

- `init-orch --suggest --brief "Analyze this database"`
- `init-orch --suggest --brief-file path/to/brief.md`
- `echo "Analyze this database" | init-orch --suggest --from-stdin`

But it should **not** silently scrape or depend on the latest Cursor or Claude session prompt by default.

## Problem To Solve
The current `--suggest` works from bounded repo evidence only. That is useful, but it can miss the user's real intent for the repo or overweight weak file-level signals.

Examples:

- A repo may contain one script file, but the real goal is research or documentation.
- A user may open Cursor or Claude and say "analyze this database," which is a strong clue about intended workflow.
- That clue is valuable, but by itself it is too transient and underspecified to become the orchestration contract automatically.

The solution is to make user or agent intent an **explicit hint** to `--suggest`, not a hidden or automatic authority.

## Product Principles

### 1. Keep the source of truth stable
Do not let a single task prompt silently redefine:

- `project.summary`
- `project.mission`
- `successCriteria`
- `verification`
- domain/workflow presets

Intent should shape a proposal, not directly replace the repo contract.

### 2. Make intent input explicit
If a user wants `--suggest` to consider a task framing, they should pass it intentionally.

Good:

- `--brief`
- `--brief-file`
- `--from-stdin`

Bad:

- silently reading the last Cursor prompt
- silently inferring the "current task" from transcripts

### 3. Preserve portability
The feature should work without requiring direct integration with Cursor, Claude Code, or any future platform runtime.

The first version should consume plain text input only. Platform-specific integrations can come later.

### 4. Keep `--suggest`, `--refine`, and `--review` separate

- `--suggest`: machine-generated proposal from repo evidence plus optional intent brief
- `--refine`: human-supplied local repo knowledge
- `--review`: ongoing maintenance and drift detection

## CLI Design

### Add flags
Support:

- `--brief "text"`
- `--brief-file path/to/file.md`
- `--from-stdin`

These should only be valid with `--suggest`.

### Validation rules

- `--brief`, `--brief-file`, and `--from-stdin` should be mutually exclusive
- they should error if used without `--suggest`
- `--from-stdin` should read a bounded amount of text
- `--brief-file` should only read text files

### Example UX

```bash
init-orch --suggest --brief "Analyze this database for schema quality, query patterns, and documentation gaps."
```

```bash
init-orch --suggest --brief-file db-brief.md
```

```bash
cat task-brief.md | init-orch --suggest --from-stdin
```

## Evidence Model

Refactor `--suggest` so it combines three evidence tiers:

### Tier A: orchestration-aware repo files
Highest priority:

- `init-orch.md`
- `AGENTS.md`
- `.cursor/`
- `.claude/`
- `orch/`

These define current workflow intent and should outweigh loose repo heuristics.

### Tier B: repo-shape evidence
Medium priority:

- `README*`
- manifests
- CI files
- entrypoints
- top-level docs

These help infer ecosystem and likely verification commands.

### Tier C: explicit intent brief
Optional but high-value:

- `--brief`
- `--brief-file`
- `--from-stdin`

This should act as a shaping input for:

- summary
- mission
- success criteria
- verification emphasis

But not override strong orchestration evidence unless the output explicitly says so.

## Brief Parsing Strategy

The first version should keep the brief format simple.

### Accept raw prose
Example:

`Analyze this database for schema quality, query patterns, and documentation gaps. Avoid writes. Prefer reproducible queries and a clear written report.`

### Optional future structured format
Later, support structured fields such as:

```text
Goal: analyze this database
Mode: exploratory
Outputs: findings, caveats, next steps
Verification: reproducible queries, explicit assumptions
Risk: avoid destructive writes
```

But do not require this initially.

## Implementation Tasks

### 1. Add intent input plumbing to CLI
Modify `parse_args()` and `main()` in `init-orch` to support:

- `--brief`
- `--brief-file`
- `--from-stdin`

Only route them through `--suggest`.

### 2. Add brief ingestion helper
Create something like:

```python
def load_suggest_brief(args: argparse.Namespace) -> dict | None:
    ...
```

Responsibilities:

- read raw brief text from the chosen input method
- normalize whitespace
- cap size
- return both:
  - raw text
  - a short derived summary if useful

### 3. Extend `collect_suggest_evidence()`
Add brief input into the evidence object:

```python
{
  "rawSpec": ...,
  "spec": ...,
  "metadata": ...,
  "repoHints": ...,
  "orchestrationFiles": ...,
  "repoFiles": ...,
  "brief": {
    "text": "...",
    "source": "brief|brief-file|stdin"
  } | None,
  "repoBrief": ...
}
```

### 4. Extend `build_repo_brief()`
Make the repo brief include:

- repo identity from files
- workflow identity from orchestration artifacts
- optional intent framing from the brief
- confidence notes about whether the brief looks transient, task-level, or repo-level

Expected output should include fields like:

- `repoIdentity`
- `workflowIdentity`
- `intentSummary`
- `intentScope`
- `intentConfidence`
- `likelyChecks`
- `suggestedDomain`

### 5. Add intent-scope classification
Create a lightweight helper like:

```python
def classify_brief_scope(brief_text: str) -> dict:
    ...
```

Purpose:

- distinguish task-like prompts from repo-like goals
- avoid overcommitting the orchestration to one temporary task

Possible categories:

- `task-local`
- `workflow-level`
- `repo-level`

Examples:

- "Analyze this database" -> likely `task-local`
- "This repo is for exploratory SQL analysis and documentation" -> likely `repo-level`

This does not need to be fancy. Simple heuristic language is fine.

### 6. Update suggestion generation
Modify:

- `suggest_summary()`
- `suggest_mission()`
- `suggest_success_criteria()`
- `build_verification_suggestions()`

New behavior:

- use the intent brief to shape language and emphasis
- do not let a task-local brief completely replace strong repo identity
- when the brief is task-local, generate suggestions that acknowledge uncertainty
- use the brief more strongly when repo evidence is weak or when the brief clearly describes durable workflow

### 7. Add brief-aware report formatting
Extend `format_suggestion_report()` so the output clearly shows:

- whether an intent brief was used
- what the brief contributed
- whether it was treated as task-level or repo-level input
- how strongly it influenced the proposal

Example section:

- intent input: `"Analyze this database ..."`
- inferred scope: `task-local`
- effect on suggestions: increased emphasis on exploratory verification and clear findings, but did not replace repo identity

### 8. Keep application logic unchanged
Do not expand `apply_suggestions_to_spec()` beyond:

- `project.summary`
- `project.mission`
- `project.successCriteria`
- `verification`

The intent-aware iteration is about improving proposal quality, not widening write scope.

## Guardrails

### Must do

- require explicit user input for the brief
- explain how the brief influenced suggestions
- keep repo/orchestration evidence higher-priority than one-off task phrasing
- preserve non-interactive print-only behavior unless explicit apply exists later

### Must not do

- silently ingest Cursor or Claude live session prompts
- silently rewrite the spec based on a single task request
- make `--suggest` tool-runtime dependent
- turn `--suggest` into a full session-history analyzer

## Regression Scenarios

### Scenario A: task-local brief on mixed repo
Repo like `qumatrix`

Brief:
- "Analyze this database"

Expected:
- brief influences tone and verification emphasis
- summary/mission do not collapse into "database analysis repo" unless repo evidence supports that

### Scenario B: repo-level brief on weak repo evidence
Sparse repo with little structure

Brief:
- "This repo is for exploratory SQL analysis and report generation"

Expected:
- brief strongly helps fill summary/mission/success criteria

### Scenario C: script-first repo with explicit brief
Repo like `init-orch`

Brief:
- "Improve orchestration safety and repo-aware setup suggestions"

Expected:
- still infer Python/tooling checks
- combine brief intent with repo identity cleanly

### Scenario D: no brief
Current behavior should remain valid.

## Suggested implementation order

1. Add `--brief`, `--brief-file`, `--from-stdin` CLI plumbing.
2. Implement brief loading and normalization.
3. Add brief into `collect_suggest_evidence()`.
4. Extend `build_repo_brief()` with intent fields.
5. Add brief-scope classification.
6. Update summary/mission/success/verification suggestion functions.
7. Update `format_suggestion_report()` to explain influence.
8. Run regression scenarios with and without a brief.

## Success criteria

This iteration is successful if:

- `--suggest` can accept a short user or agent brief explicitly
- task-style prompts help shape suggestions without overriding repo identity
- repo-level prompts materially improve first-draft quality on sparse repos
- the feature remains lightweight, deterministic, and tool-portable
- users can understand why the suggestion changed when a brief is supplied

## Short handoff note

If you need a short prompt for the next session:

> Improve `init-orch --suggest` so it can accept explicit intent input via `--brief`, `--brief-file`, or `--from-stdin`. Treat that input as optional evidence, not the source of truth. Refactor evidence collection and repo-brief building so repo/orchestration artifacts stay primary, classify the brief as task-local vs repo-level, and use it to shape summary/mission/success criteria/verification without letting transient prompts silently redefine the orchestration contract.
