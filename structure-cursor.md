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

---

## Resources

### Rules collections (copy-paste starting points)

| Repo | Stars | What to grab |
|------|-------|--------------|
| [sanjeed5/awesome-cursor-rules-mdc](https://github.com/sanjeed5/awesome-cursor-rules-mdc) | 3.5k | Modern `.mdc` format, organized by stack. Grab the rule for your framework and drop it in `.cursor/rules/`. |
| [PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) | 39k | Larger collection, but uses the old `.cursorrules` single-file format. Convert by splitting into `.mdc` files with `globs:` frontmatter. |

Workflow: find your stack in one of those repos → copy the content → paste into a `.mdc` file with the right frontmatter → trim anything that doesn't apply to your project.

### MCP servers (extend what Cursor can do)

Cursor supports MCP natively. Same servers work as in Claude Code.

| Repo | Stars | What to grab |
|------|-------|--------------|
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | 85k | Official reference implementations: `filesystem`, `fetch`, `git`, `memory`, `sequential-thinking` |
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | 86k | Community curated list, organized by category |

Add chosen servers to `.cursor/mcp.json`. Cursor picks them up on restart.
