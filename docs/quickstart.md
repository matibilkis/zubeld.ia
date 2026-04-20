# Quickstart

`init-orch` works best as a practical five-step loop:

1. Bootstrap a repository with a short interactive setup.
2. Ask for a repo-aware suggestion pass when you want a better first ansatz.
3. Compile one source of truth into tool-specific files.
4. Refine the setup with repo-specific details after the first render.
5. Review the setup deliberately when it starts feeling off.

`init-orch.md` is the only high-level file you should edit directly. The generated files under `.cursor/`, `.claude/`, `AGENTS.md`, and `orch/` are derived outputs.

> Security warning: enabling edit, write, delete, shell, network, or external tool access can expose code, secrets, and local data to irreversible changes or exfiltration. Start with least privilege and require approval for high-impact actions.

## 1. Bootstrap

In a new repository, run:

```bash
init-orch
```

In a terminal, `init-orch` can guide you through a short bootstrap flow. It asks only for:

- a `workflow-domain` preset
- a short project summary
- target platforms
- a risk posture

If you prefer to skip the prompts, bootstrap directly:

```bash
init-orch --preset research-docs --no-interactive
```

Presets are composed as `workflow-domain`.

Workflows:

| Workflow | Best for | Bias |
|------|------|------|
| `research` | exploration, synthesis, studies | stronger evidence review, less production pressure |
| `engineering` | maintainable long-term delivery | balanced default, stronger production-readiness |
| `poc` | fast experiments | lighter process, faster iteration |

Domains:

| Domain | Best for | Bias |
|------|------|------|
| `generic` | libraries, services, APIs, CLIs | broad default |
| `web-app` | frontend or full-stack apps | UI and behavior verification |
| `data-science` | notebooks, experiments, models | reproducibility and experiment review |
| `infra` | infrastructure or ops work | stricter approvals and plan-first behavior |
| `docs` | documentation-focused repos | editorial review and low implementation assumptions |
| `multimedia` | content and asset workflows | stronger review and provenance awareness |

The default preset is `engineering-generic`.

## 2. Suggest

If you want help filling the hardest fields in `init-orch.md`, run:

```bash
init-orch --suggest
```

This samples a bounded amount of repo evidence, prioritizes existing orchestration artifacts such as `init-orch.md`, `AGENTS.md`, `.cursor/`, `.claude/`, and `orch/`, and proposes updates for:

- `project.summary`
- `project.mission`
- `project.successCriteria`
- `verification`

It prints the proposal first and only applies it if you confirm.

## 3. Compile

After bootstrap, refine `init-orch.md` and then render the target-specific outputs:

```bash
init-orch --all
```

Or render only one target:

```bash
init-orch --cursor
init-orch --claude
```

If `init-orch` detects existing owned-looking structure such as `orch/`, `.cursor/`, `.claude/`, `AGENTS.md`, or a `.gitignore` update it needs to make, it will stop and ask for confirmation in a terminal. For non-interactive runs, re-run with:

```bash
init-orch --all --confirm-existing
```

## What to fill in first

If you are not fully sure what the project should look like yet, use this order:

1. Project shape and guardrails: preset, mission, success criteria, targets, stop conditions, verification, and `toolPolicy`.
   This mainly affects `orch/permissions.policy.json`, Claude settings/rules, core workflow rules, and recommendation quality.
2. Roles and collaboration shape: roles, handoffs, and repository rules.
   This mainly affects `AGENTS.md` and Claude agent files.
3. Capabilities and integrations: imports, MCPs, and target overrides.
   This mainly affects imports manifests, `orch/imports.lock.json`, and Cursor MCP output when relevant.
4. Reusable accelerators: skills.
   This mainly affects Cursor and Claude skill files.
5. Meta-iteration: evaluation and review refinements.
   This mainly affects `orch/evaluation.plan.json` and the long-term setup loop.

For a first useful pass, steps 1 and 2 are enough. The rest can stay rough until after the first render.

If `init-orch.md` already exists, the preset is ignored and your existing blueprint is preserved.

## 4. Refine

After the first render, tailor the setup to the actual repository:

```bash
init-orch --refine
```

This is a short second pass for high-value repo details such as:

- the most common kinds of changes
- the main verification command or manual check
- sensitive directories or file patterns
- existing conventions the generated setup should respect

## 5. Review

When the setup feels stale, run:

```bash
init-orch --review
```

This prints a short snapshot, immediate actions, and setup recommendations without rewriting files. It also tries to surface repo-specific issues such as missing canonical verification commands, workspace-style structure, or existing generated-path collisions. Treat it as an opt-in review loop, not an autonomous control plane.

## Minimal example

Keep the rest of the file as generated and replace the spec block with something like:

```json
{
  "version": 2,
  "preset": "engineering-generic",
  "workflowPreset": "engineering",
  "domainPreset": "generic",
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

You do not need to perfect every field before rendering. A solid first pass is:

- choose the preset
- write the project mission and success criteria
- define stop conditions, verification, and approvals
- add the core roles
- leave imports, skills, and evaluation lighter until the workflow feels real

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

Later, run `init-orch --review` to get practical recommendations and decide whether they should be folded back into the spec.

## Practical preset example

For a frontend-heavy app:

```bash
mkdir my-web-app && cd my-web-app
init-orch --preset engineering-web-app --no-interactive
init-orch --suggest
# review and fine-tune init-orch.md
init-orch --all
init-orch --refine
init-orch --review
```

That gives you a better first draft for UI-oriented workflow, verification, and imports than the generic default.
