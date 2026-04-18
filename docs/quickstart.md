# Quickstart

`init-orch` now works in two steps:

1. Run `init-orch` in a new repository. This creates `init-orch.md`.
2. Edit `init-orch.md`, then run `init-orch --cursor`, `init-orch --claude`, or `init-orch --all`.

`init-orch.md` is the only high-level file you should edit directly. The generated files under `.cursor/`, `.claude/`, `AGENTS.md`, and `orch/` are derived outputs.

> Security warning: enabling edit, write, delete, shell, network, or external tool access can expose code, secrets, and local data to irreversible changes or exfiltration. Start with least privilege and require approval for high-impact actions.

## Presets

You can bootstrap the first `init-orch.md` from a preset:

```bash
init-orch --preset research
```

Available presets:

| Preset | Best for | Bias |
|------|------|------|
| `research` | exploration, synthesis, studies | stronger planning, lower edit risk |
| `engineering` | general software projects | balanced default |
| `web-app` | frontend or full-stack apps | UI and behavior verification |
| `poc` | fast experiments | lighter process, faster iteration |
| `multimedia` | content and asset workflows | stronger review and external pack awareness |
| `infra` | infrastructure or ops work | stricter approvals and plan-first behavior |
| `docs` | documentation-focused repos | low-risk editing and lighter verification |

If `init-orch.md` already exists, the preset is ignored and your existing blueprint is preserved.

## Minimal example

Keep the rest of the file as generated and just replace the spec block with something like:

```json
{
  "version": 2,
  "preset": "engineering",
  "project": {
    "name": "api-service",
    "summary": "Internal API service. Optimize for safe edits, clear plans, and focused verification.",
    "mission": "Let agents make small safe changes while humans stay in control of risky actions.",
    "style": "practical",
    "successCriteria": [
      "Small safe diffs",
      "Focused verification",
      "Low babysitting overhead"
    ],
    "riskPosture": "moderate",
    "maturity": "growing"
  },
  "targets": ["cursor", "claude"],
  "roles": [
    {
      "id": "planner",
      "role": "Plan non-trivial work before coding.",
      "responsibilities": ["Clarify scope", "Propose the smallest safe path"],
      "deliverables": ["Short plan"]
    },
    {
      "id": "implementer",
      "role": "Make focused code changes and run relevant checks.",
      "responsibilities": ["Implement", "Verify"],
      "deliverables": ["Diff", "Verification notes"]
    },
    {
      "id": "evaluator",
      "role": "Review how the human-agent loop is working.",
      "responsibilities": ["Spot friction", "Recommend orchestration changes"],
      "deliverables": ["Recommendations"]
    }
  ],
  "rules": [
    "Ask before destructive actions.",
    "Run focused tests after changes."
  ],
  "workflow": {
    "planningTrigger": "Plan first for non-trivial work.",
    "implementationFocus": "Prefer the smallest safe change.",
    "reviewChecklist": [
      "Confirm the change worked.",
      "Confirm the checks were relevant."
    ],
    "escalation": [
      "Escalate when requirements are ambiguous.",
      "Escalate before destructive actions."
    ],
    "stopConditions": [
      "Stop when credentials are missing.",
      "Stop when risk is too high without human review."
    ]
  },
  "verification": [
    {
      "changeType": "code",
      "required": ["Run focused tests or explain why none were available."]
    }
  ],
  "skills": [
    {
      "id": "change-plan",
      "when": "Use before multi-step implementation work.",
      "steps": [
        "State the goal.",
        "Outline the smallest safe change.",
        "List the checks to run."
      ],
      "outputs": ["Plan", "Checks"]
    }
  ],
  "toolPolicy": {
    "allow": ["Read(*)", "Glob(*)", "Grep(*)", "WebFetch", "WebSearch"],
    "risky": ["Edit(*)", "Write(*)", "Bash(*)"],
    "deny": ["Bash(rm -rf *)", "Bash(sudo *)"],
    "requiresApproval": ["Bash(*)", "Edit(.env*)"]
  },
  "evaluation": {
    "cadence": "After meaningful workflow changes.",
    "signals": [
      "Humans repeat context too often.",
      "Agents get blocked by unclear permissions."
    ],
    "goals": [
      "Reduce babysitting.",
      "Keep safety high."
    ],
    "recommendationFormat": "Short actionable recommendations."
  },
  "imports": [
    {
      "id": "design-pack",
      "type": "skillPack",
      "source": "https://ui-ux-pro-max-skill.nextlevelbuilder.io/",
      "version": "reference",
      "targets": ["cursor", "claude"],
      "trust": { "level": "review-required", "reviewedByHuman": false },
      "provides": {
        "notes": ["Review the pack before relying on it in production."],
        "skills": []
      }
    },
    {
      "id": "example-mcp",
      "type": "mcp",
      "source": "npm:example-mcp-server",
      "version": "latest",
      "targets": ["cursor"],
      "trust": { "level": "review-required", "reviewedByHuman": false },
      "transport": {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "example-mcp-server"],
        "env": {}
      },
      "provides": {
        "notes": ["Review the MCP tool surface before enabling it."],
        "skills": []
      }
    }
  },
  "claude": {
    "settingsLocalExample": {
      "permissions": {
        "allow": ["Bash(*)", "Edit(*)", "Write(*)", "Read(*)"],
        "defaultMode": "acceptEdits"
      }
    }
  }
}
```

Then run:

```bash
init-orch --all
```

That will regenerate:

- `init-orch.md` metadata
- `init-orch.md` recommendations
- `AGENTS.md`
- `orch/permissions.policy.json`
- `orch/imports.lock.json`
- `orch/evaluation.plan.json`
- `.cursor/rules/*`, `.cursor/skills/*`, `.cursor/imports/manifest.json`, and `.cursor/mcp.json` when MCP imports target Cursor
- `.claude/settings.json`, `.claude/settings.local.json.example`, `.claude/rules/*`, `.claude/agents/*`, `.claude/skills/*`, and `.claude/imports/manifest.json`

Iterate by editing `init-orch.md`, re-running `init-orch --all`, and then deciding whether the generated recommendations should be folded back into the spec.

## Practical preset example

For a frontend-heavy app:

```bash
mkdir my-web-app && cd my-web-app
init-orch --preset web-app
# review and fine-tune init-orch.md
init-orch --all
```

That gives you a better first draft for UI-oriented workflow, verification, and imports than the generic default.
