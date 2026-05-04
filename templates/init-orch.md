# Init Orch

`init-orch.md` is the only high-level file you should edit directly. The generated files under `.cursor/`, `.claude/`, `AGENTS.md`, and `orch/` are derived outputs.

> Security warning: Granting edit, write, delete, shell, network, or external tool access can expose code, secrets, and local data to irreversible changes or exfiltration. Use least-privilege defaults, require approval for high-impact actions, and review imported capabilities before enabling them.

Preset: `engineering-generic`. Workflow `engineering`: Long-term delivery workflow focused on maintainable, production-ready changes. Domain `generic`: General software projects such as libraries, APIs, backends, and internal services.

## Preset Provenance

`engineering-generic` supplied the starting draft for this file. Workflow `engineering` sets the working-style bias and domain `generic` sets the repo-shape bias.

- `preset`, `workflowPreset`, and `domainPreset` record that starting point.
- The initial defaults in the JSON block below came from the preset plus any answers you gave during bootstrap.
- Preset-influenced areas usually include `project`, `responseStyle`, `workflow`, `verification`, `toolPolicy`, and the guidance sections in this file.
- Nothing in the spec is locked. Edit any field directly when the repository needs something different.
- Keep `project.riskPosture` separate from the preset when you only want to change caution level.

Edit the JSON block below freely to describe the orchestration structure you want for this repository.

## What To Fill In First

If your project idea is still fuzzy, make the Priority 1 and 2 decisions first. You can leave later priorities rough or incomplete until after the first render.
The top-level JSON keys below follow the same order, so you can edit from top to bottom without hunting around.

### Priority 1: Project shape and guardrails

Start here. Decide:
A solid first render usually only needs this priority plus Priority 2.
- `preset`, `workflowPreset`, `domainPreset`
- `project.summary`, `project.mission`, `project.successCriteria`
- `targets`
- `workflow.stopConditions`
- `verification`
- `toolPolicy`

This mainly influences:
- `orch/permissions.policy.json`
- core Cursor and Claude workflow rules
- Claude settings and approval boundaries
- recommendation quality

### Priority 2: Collaboration shape

Add next. Decide:
Add the smallest collaboration loop that makes reviews and handoffs obvious.
- `handoffs`
- `rules`

This mainly influences:
- `AGENTS.md`
- clear ownership and review flow

### Priority 3: Capabilities and integrations

Add once the core workflow is clear. Decide:
Keep this light on the first render. The default `find-skills` entry is an optional template you can keep, copy, or delete.
- `imports`
- MCP declarations
- `targetOverrides`
- `claudeRules` — path-scoped Claude rules loaded only when Claude touches matching files. Example: `{"id": "python-style", "globs": ["**/*.py"], "rules": ["Use type hints on all signatures."]}`. Generated as `.claude/rules/{id}.md` with YAML frontmatter.

This mainly influences:
- `orch/imports.lock.json`
- Cursor and Claude import manifests
- Cursor MCP configuration when relevant
- `.claude/rules/*.md` path-scoped rule files

### Priority 4: Reusable accelerators

Optional for now. Decide:
Add reusable skills only after you notice repeated patterns worth codifying.
- `skills`

This mainly influences:
- Cursor and Claude skill files
- reusable workflows for repeated tasks

### Priority 5: Meta-iteration

Tune later. Decide:
Use this after real work has happened and you have evidence that the setup should change.
- `evaluation`
- retrospective cadence and recommendation hygiene

This mainly influences:
- `orch/evaluation.plan.json`
- better long-term workflow tuning

### Preset Emphasis For `engineering-generic`

- Treat maintainability, approval gates, and production-ready verification as part of Priority 1.
- Stay with the global order unless the repository has unusual domain-specific constraints.

<!-- Edit the JSON spec below freely. Every field is editable. Everything else is generated from it. -->

<!-- init-orch:spec:start -->
```json
{
  "version": 2,
  "preset": "engineering-generic",
  "workflowPreset": "engineering",
  "domainPreset": "generic",
  "project": {
    "name": "your-repo",
    "summary": "Engineering-oriented project. Optimize for maintainable, production-ready changes with focused verification.",
    "mission": "Let agents deliver small, reviewable improvements that hold up in long-term maintenance and production use.",
    "style": "practical",
    "successCriteria": [
      "Ship small safe changes quickly.",
      "Keep guidance easy for humans to update.",
      "Ship maintainable changes that can survive long-term ownership.",
      "Keep verification focused on correctness, regressions, and operability."
    ],
    "riskPosture": "moderate",
    "maturity": "growing"
  },
  "responseStyle": {
    "tone": "direct",
    "verbosity": "balanced",
    "structure": "answer-first",
    "defaultLength": "short",
    "rules": [
      "Lead with the answer or recommendation.",
      "Keep responses concise unless the user asks for more detail.",
      "Use bullets only when the content is naturally list-shaped."
    ],
    "examples": [
      "Do: `Bug in auth middleware. Expiry check should use <=. Fix:`",
      "Avoid: `Sure! I'd be happy to help. The issue may be caused by...`"
    ]
  },
  "targets": [
    "cursor",
    "claude"
  ],
  "verification": [
    {
      "changeType": "code",
      "required": [
        "Run focused tests or explain why none were available."
      ]
    },
    {
      "changeType": "config",
      "required": [
        "Review generated files before enabling broad permissions."
      ]
    }
  ],
  "toolPolicy": {
    "allow": [
      "Read(*)",
      "Glob(*)",
      "Grep(*)",
      "WebFetch",
      "WebSearch"
    ],
    "risky": [
      "Edit(*)",
      "Write(*)",
      "Delete(*)",
      "Bash(*)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Edit(.env*)"
    ],
    "requiresApproval": [
      "Delete(*)",
      "Bash(*)",
      "Edit(.env*)"
    ]
  },
  "workflow": {
    "planningTrigger": "Plan first for non-trivial or cross-cutting implementation work.",
    "implementationFocus": "Prefer the smallest production-ready change that solves the real problem.",
    "reviewChecklist": [
      "Confirm behavior changed as intended.",
      "Check for missing verification.",
      "Confirm the design still looks maintainable in six months.",
      "Check for missing tests, rollback concerns, or obvious operational gaps."
    ],
    "escalation": [
      "Escalate when requirements are ambiguous.",
      "Escalate before destructive actions or production-impacting changes."
    ],
    "stopConditions": [
      "Stop when missing credentials or required access blocks progress.",
      "Stop when the requested action would be unsafe without human review."
    ]
  },
  "handoffs": [
    {
      "from": "planning",
      "to": "implementation",
      "expects": [
        "Goal summary",
        "Constraints",
        "Proposed plan"
      ]
    },
    {
      "from": "implementation",
      "to": "review",
      "expects": [
        "Diff summary",
        "Verification notes",
        "Known risks"
      ]
    }
  ],
  "rules": [
    "Confirm with the user before destructive or irreversible actions.",
    "Run focused verification after every change.",
    "Leave secrets and production credentials untouched.",
    "Prefer maintainable solutions over clever shortcuts.",
    "Keep diffs small and verification scoped to the actual change."
  ],
  "claudeRules": [],
  "imports": [
    {
      "id": "find-skills",
      "type": "skillPack",
      "source": "https://skills.sh/vercel-labs/skills/find-skills",
      "version": "reference",
      "targets": [
        "cursor",
        "claude"
      ],
      "note": "Optional template import for external skills. Copy this entry for other skills or delete it if unused.",
      "trust": {
        "level": "reference",
        "reviewedByHuman": true
      },
      "provides": {
        "notes": [
          "Template import for skills.sh-compatible skills. Duplicate it and change `id`, `source`, and provided skill details for other imports."
        ],
        "skills": [
          {
            "id": "find-skills",
            "when": "Use when you need to discover a specialized external skill or workflow.",
            "steps": [
              "Identify the domain and the exact task you need help with.",
              "Search for a relevant skill and verify source quality before adoption.",
              "Record the chosen skill back in `init-orch.md` before relying on it."
            ],
            "outputs": [
              "Skill candidates",
              "Adoption note",
              "Follow-up import update"
            ]
          }
        ]
      }
    }
  ],
  "targetOverrides": {
    "cursor": {
      "alwaysApplyRules": [
        "core",
        "orchestrator-policy",
        "workflow",
        "evaluation"
      ]
    },
    "claude": {
      "notes": [
        "Keep `.claude/settings.local.json` uncommitted."
      ]
    }
  },
  "skills": [
    {
      "id": "change-plan",
      "when": "Use for multi-step work that benefits from a short implementation plan.",
      "steps": [
        "Summarize the goal and important constraints.",
        "Outline the smallest safe change.",
        "List the checks needed before finishing."
      ],
      "outputs": [
        "Plan",
        "Verification checklist"
      ]
    }
  ],
  "evaluation": {
    "cadence": "Review after meaningful project changes or when the workflow feels brittle.",
    "signals": [
      "Humans repeatedly have to restate context.",
      "Agents stall because permissions are too weak or too broad.",
      "Reviews catch recurring classes of mistakes."
    ],
    "goals": [
      "Reduce human babysitting.",
      "Improve safety without making normal work painful.",
      "Reduce human babysitting without weakening production discipline.",
      "Keep the workflow maintainable as the repository grows."
    ],
    "recommendationFormat": "Short actionable recommendations grouped by risk and ergonomics."
  },
  "claude": {
    "settingsLocalExample": {
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
  }
}
```
<!-- init-orch:spec:end -->

## Render Loop

1. Fill in Priority 1 and 2 first. Keep the default `find-skills` import only as an optional template until the workflow feels real.
2. Run `init-orch --cursor`, `init-orch --claude`, or `init-orch --all`.
3. Run `init-orch --suggest` when you want a repo-aware proposal for summary, mission, success criteria, and verification.
4. Copy or edit the default `find-skills` import when you want to add other skills, or replace it with MCP declarations when you need external tools.
5. Re-run the command whenever you change the orchestration design.
6. Review the generated recommendations block and decide which changes belong in the spec.

The generator will only rewrite the metadata and recommendations blocks below.

<!-- init-orch:generated:start -->
```json
{
  "version": 2,
  "lastRenderedAt": null,
  "renderedTargets": [],
  "generatedFiles": [],
  "resolvedImports": [],
  "bootstrapPreset": "engineering-generic",
  "workflowPreset": "engineering",
  "domainPreset": "generic"
}
```
<!-- init-orch:generated:end -->

<!-- init-orch:recommendations:start -->
```json
{
  "version": 1,
  "summary": "Render the targets to populate recommendations.",
  "items": []
}
```
<!-- init-orch:recommendations:end -->
