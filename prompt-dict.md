# Prompt Dictionary

Copy-paste prompts for recurring tasks on new repos. Ordered by when in the lifecycle you'd use them.

---

## Stage 1 — Setup (day 1, after init-orch)

### Generate Cursor core.mdc from CLAUDE.md

```
Read CLAUDE.md and generate .cursor/rules/core.mdc with the same content.
Add YAML frontmatter at the top:
---
description: Core project rules
alwaysApply: true
---
Use plain bullet points for the rules. Replace the XML <examples> block with two plain inline examples under a "Response style" bullet. Create the file.
```

### Create .claude/settings.local.json

```
Create .claude/settings.local.json with this exact content:
{
  "permissions": {
    "allow": ["Bash(*)", "Edit(*)", "Write(*)", "Read(*)", "Glob(*)", "Grep(*)", "WebFetch(*)", "WebSearch(*)"],
    "defaultMode": "acceptEdits"
  }
}
```

### Grant Cursor full local permissions

Paste this into Cursor. Cursor has no settings file equivalent to Claude's settings.local.json — permissions are set via rules.

```
Add a Permissions section to .cursor/rules/core.mdc, right after the frontmatter and before any other section:

## Permissions

You have full access to this repo: read, create, edit, and delete any file without asking. Run terminal commands freely. Do not ask for confirmation on individual file or shell operations — treat this the same as a developer's local environment.
```

---

## Stage 2 — Calibration (after first real session)

### Audit CLAUDE.md against the actual repo

```
Read CLAUDE.md. Then scan the repo: list top-level structure, check that the commands in CLAUDE.md actually exist, verify the stack description matches what you find in config files (package.json, pyproject.toml, go.mod, etc.), and note any important paths or patterns that are missing.
Propose a minimal diff to CLAUDE.md — flag stale lines, suggest additions. Do not rewrite the whole file.
```

### Test what Claude actually knows

```
Treat CLAUDE.md as your only context — ignore everything else you know about this repo from this session. Based solely on that file: what would you do first if asked to make a change? What's ambiguous? What's missing that would meaningfully help you? Report this as a short bullet list, then stop.
```

---

## Stage 3 — Extension (as the project grows)

### Add a path-scoped rule for a specific area

```
Read the files under [path or glob, e.g. src/api/]. Identify the naming conventions, patterns, and non-obvious constraints actually present in those files. Then create .claude/rules/[topic].md with YAML frontmatter:
---
paths:
  - "[same glob]"
---
Write rules grounded in what you found — not generic advice. Max 8 bullet points.
```

### Suggest MCP servers for this stack

```
Read CLAUDE.md. Based on the stack and what this project does, suggest 2-3 MCP servers from https://github.com/punkpeye/awesome-mcp-servers that would genuinely help — not just generic ones. For each: one sentence on what it does, one sentence on why it fits this specific project, and the install/config snippet to add it.
```
