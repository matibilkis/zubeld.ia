# Claude Agentic Structure

Minimal project setup for Claude Code. Edit the files below; delete any section you don't need.

---

## File tree

```
repo/
├── CLAUDE.md                        ← always loaded, main context
├── .gitignore                       ← add .claude/settings.local.json
└── .claude/
    ├── settings.json                ← committed, default permissions
    ├── settings.local.json          ← gitignored, your local overrides
    └── rules/
        ├── project.md               ← always loaded, project rules
        └── {topic}.md               ← path-scoped, only when touching matching files
```

---

## CLAUDE.md

```markdown
# {Project Name}

{One paragraph: what this repo does and what a good change looks like.}

## Stack

{Language, frameworks, key libs. One line each.}

## Commands

- Run: `{command}`
- Test: `{command}`
- Lint: `{command}`

## Key paths

- `{path}` — {what it is}
- `{path}` — {what it is}
```

---

## .claude/settings.json

```json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Glob(*)",
      "Grep(*)",
      "WebFetch",
      "WebSearch"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Edit(.env*)"
    ]
  }
}
```

---

## .claude/settings.local.json

Broader permissions for your own machine. Keep gitignored.

```json
{
  "permissions": {
    "allow": [
      "Bash(*)",
      "Edit(*)",
      "Write(*)",
      "Read(*)",
      "Glob(*)",
      "Grep(*)",
      "WebFetch(*)",
      "WebSearch(*)"
    ],
    "defaultMode": "acceptEdits"
  }
}
```

---

## .claude/rules/project.md

Always loaded. Keep short — everything here costs context on every session.

```markdown
# Project Rules

## Mission

{One sentence: what you're optimizing for in this repo.}

## Rules

- {Positive framing: "Do X" not "Don't do X".}
- Confirm with the user before destructive or irreversible actions.
- Leave secrets and production credentials untouched.

## Response style

- Lead with the answer, not a preamble.
- Short by default. Expand only when asked.

<examples>
- Do: `Auth bug: expiry check uses > instead of >=. Fix on line 42.`
- Avoid: `Sure! I'd be happy to help. The issue may be caused by...`
</examples>
```

---

## .claude/rules/{topic}.md

Only loaded when Claude touches files matching the `paths` pattern.
One file per concern. Delete if unused.

```markdown
---
paths:
  - "{glob pattern, e.g. src/api/**/*.py}"
---
# {Topic}

- {Rule specific to these files.}
- {Rule specific to these files.}
```
