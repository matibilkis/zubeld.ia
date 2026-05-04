# Cursor Agentic Structure

Minimal project setup for Cursor. Edit the files below; delete any section you don't need.

---

## File tree

```
repo/
└── .cursor/
    ├── rules/
    │   ├── core.mdc           ← always applied
    │   └── {topic}.mdc        ← path-scoped, only when touching matching files
    └── mcp.json               ← optional, MCP server config
```

---

## .cursor/rules/core.mdc

Always applied in every session. Keep it short.

```markdown
---
description: Core project rules
alwaysApply: true
---

# {Project Name}

{One sentence: what this repo does and what a good change looks like.}

## Stack

{Language, frameworks, key libs.}

## Commands

- Run: `{command}`
- Test: `{command}`
- Lint: `{command}`

## Rules

- {Positive framing: "Do X" not "Don't do X".}
- Confirm with the user before destructive or irreversible actions.
- Leave secrets and production credentials untouched.
- Lead with the answer. Short by default.
```

---

## .cursor/rules/{topic}.mdc

Only loaded when Cursor touches files matching the glob.
One file per concern. Delete if unused.

```markdown
---
description: {What this rule covers}
globs:
  - "{glob pattern, e.g. src/api/**/*.py}"
alwaysApply: false
---

# {Topic}

- {Rule specific to these files.}
- {Rule specific to these files.}
```

---

## .cursor/mcp.json

Optional. Only needed if connecting external tools via MCP.

```json
{
  "mcpServers": {
    "{server-id}": {
      "command": "{command}",
      "args": ["{arg1}", "{arg2}"],
      "env": {}
    }
  }
}
```
