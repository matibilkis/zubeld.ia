# Quickstart

`init-orch` works best as a practical loop, but the first useful path should feel plug-and-play:

1. Bootstrap a repository with a short interactive setup.
2. Compile one source of truth into tool-specific files.
3. Use `--suggest`, `--refine`, `--review`, and `--parity` later only when they solve a real repo problem.

`init-orch.md` is the only high-level file you should edit directly. The generated files under `.cursor/`, `.claude/`, `AGENTS.md`, and `orch/` are derived outputs.

> Security warning: enabling edit, write, delete, shell, network, or external tool access can expose code, secrets, and local data to irreversible changes or exfiltration. Start with least privilege and require approval for high-impact actions.

## Fastest Useful Setup

If you want a minimal working agentic setup quickly, the shortest path is:

```bash
init-orch
# fill in the short bootstrap prompts
init-orch --all
```

That is usually enough to get a first ready-to-use Cursor/Claude structure in about 2-5 minutes.

If you also want better repo-specific verification, response style, cross-target checks, and safer defaults for a real repository, expect closer to 10-20 minutes with `--suggest`, `--refine`, `--review`, and `--parity`.

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

The preset is only a first draft. After bootstrap, edit `init-orch.md` to override any default.

In the generated file, `preset`, `workflowPreset`, and `domainPreset` record where the starting draft came from. The rest of the spec is still yours to change freely.

That includes `responseStyle`: presets now start with different response defaults for research, engineering, docs, and other repo shapes, but you can still edit tone, verbosity, structure, rules, length, and examples directly.

If you want the fastest path to a working setup, the best next step after bootstrap is:

```bash
init-orch --all
```

Presets are composed as `workflow-domain`.

If you want to inspect them before you choose, run:

```bash
init-orch --list-presets
init-orch --explain-preset engineering-web-app
```

Think of them this way:

- the workflow sets the working bias: research, engineering, or poc
- the domain sets the repo shape bias: generic, web-app, data-science, infra, docs, or multimedia
- the result is a starting default, not a lock-in

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

If you are unsure, use:

- `engineering-generic` for most software repos
- `research-docs` for exploratory or writing-heavy work
- `engineering-web-app` for UI/product work
- `poc-data-science` for notebook/experiment-heavy exploration

Typical override flow:

1. Pick the closest preset.
2. Bootstrap with `init-orch` or `init-orch --preset ... --no-interactive`.
3. Run `init-orch --all` for the first render.
4. Edit `init-orch.md` to change mission, `responseStyle`, verification, roles, imports, or anything else.
5. Re-run `init-orch --all`.

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

It prefers real repo checks from scripts, CI, and language-specific config over weaker generic fallbacks, and keeps docs-oriented checks separate from code-oriented checks. It also explains why each recommendation was made, groups evidence into identity/workflow/verification/safety buckets, and asks targeted questions when confidence is low instead of guessing aggressively. It prints the proposal first and only applies it if you confirm.

## 3. Compile

After bootstrap, render the target-specific outputs:

```bash
init-orch --all
```

If you want to review the generated plan before writing files, use:

```bash
init-orch --all --dry-run
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

1. Project shape and guardrails: preset, mission, success criteria, `responseStyle`, targets, stop conditions, verification, and `toolPolicy`.
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

If refine notes already exist, the command keeps them by default and only re-asks those answers if you choose to update them.

## 5. Review

When the setup feels stale, run:

```bash
init-orch --review
```

This prints a short snapshot, top immediate actions, and setup recommendations without rewriting files. It also tries to surface repo-specific issues such as missing canonical verification commands, workspace-style structure, or existing generated-path collisions, while suppressing unchanged setup recommendations that have already been recorded. Treat it as an opt-in review loop, not an autonomous control plane.

## 6. Parity

If you want to inspect Cursor/Claude alignment directly, run:

```bash
init-orch --parity
```

This shows what is shared between both targets, what each target gets specifically, which overrides are target-specific, and whether drift has appeared because one target was rendered while the other was left behind.

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
- set `responseStyle` if you already know the tone and brevity you want
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
