# Agent Operating Guide

Source of truth: `init-orch.md`. Re-run `init-orch` after changing the orchestration design.

> Security warning: granting edit, write, delete, shell, network, or external tool access can expose code, secrets, and local data to irreversible changes or exfiltration. Use least privilege and require approval for high-impact actions.

## Project

- Name: your-repo
- Style: practical
- Targets: cursor, claude
- Risk posture: moderate
- Maturity: new

Describe what this repository does and what a successful change should optimize for.

## Mission

Keep human and agent work aligned around practical, reviewable improvements.

## Roles

- `planner`: Plan non-trivial changes before implementation.
- `implementer`: Make focused code changes and verify the result.
- `reviewer`: Review diffs for bugs, regressions, and missing checks.
- `evaluator`: Assess how the human-agent workflow is performing over time.

## Working Rules

- Ask before destructive or irreversible actions.
- Prefer focused verification after changes.
- Do not edit secrets or production credentials.

## Workflow

- Plan first for non-trivial or ambiguous changes.
- Prefer the smallest safe change that improves the repository.

## Evaluation Loop

- Review the workflow after meaningful changes.
- Use generated recommendations to refine `init-orch.md`.
