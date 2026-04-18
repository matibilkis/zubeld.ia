# Init Orch

`init-orch.md` is the only high-level file you should edit directly. The generated files under `.cursor/`, `.claude/`, `AGENTS.md`, and `orch/` are derived outputs.

> Security warning: Granting edit, write, delete, shell, network, or external tool access can expose code, secrets, and local data to irreversible changes or exfiltration. Use least-privilege defaults, require approval for high-impact actions, and review imported capabilities before enabling them.

Preset: `engineering`. Balanced default for general software projects such as libraries, backends, and services.

Edit the JSON block below to describe the orchestration structure you want for this repository.

<!-- Edit the JSON spec below. Everything else is generated from it. -->

<!-- init-orch:spec:start -->
```json
{
  "version": 2,
  "preset": "engineering",
  "project": {
    "name": "your-repo",
    "summary": "Describe what this repository does and what a successful change should optimize for.",
    "mission": "Keep human and agent work aligned around practical, reviewable improvements.",
    "style": "practical",
    "successCriteria": [
      "Ship small safe changes quickly.",
      "Keep guidance easy for humans to update."
    ],
    "riskPosture": "moderate",
    "maturity": "new"
  },
  "targets": [
    "cursor",
    "claude"
  ],
  "roles": [
    {
      "id": "planner",
      "role": "Plan non-trivial changes before implementation.",
      "responsibilities": [
        "Clarify the goal and constraints.",
        "Propose the smallest safe path forward."
      ],
      "deliverables": [
        "Short implementation plan"
      ]
    },
    {
      "id": "implementer",
      "role": "Make focused code changes and verify the result.",
      "responsibilities": [
        "Implement the agreed change.",
        "Run the most relevant checks."
      ],
      "deliverables": [
        "Code changes",
        "Verification notes"
      ]
    },
    {
      "id": "reviewer",
      "role": "Review diffs for bugs, regressions, and missing checks.",
      "responsibilities": [
        "Look for correctness and safety issues.",
        "Call out missing tests or risky assumptions."
      ],
      "deliverables": [
        "Review findings or approval"
      ]
    },
    {
      "id": "evaluator",
      "role": "Assess how the human-agent workflow is performing over time.",
      "responsibilities": [
        "Identify friction in prompts, permissions, and handoffs.",
        "Recommend changes to the orchestration design."
      ],
      "deliverables": [
        "Recommendations for init-orch.md"
      ]
    }
  ],
  "rules": [
    "Ask before destructive or irreversible actions.",
    "Prefer focused verification after changes.",
    "Do not edit secrets or production credentials."
  ],
  "workflow": {
    "planningTrigger": "Plan first for non-trivial or ambiguous changes.",
    "implementationFocus": "Prefer the smallest safe change that improves the repository.",
    "reviewChecklist": [
      "Confirm behavior changed as intended.",
      "Check for missing verification."
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
      "from": "planner",
      "to": "implementer",
      "expects": [
        "Goal summary",
        "Constraints",
        "Proposed plan"
      ]
    },
    {
      "from": "implementer",
      "to": "reviewer",
      "expects": [
        "Diff summary",
        "Verification notes",
        "Known risks"
      ]
    }
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
  "evaluation": {
    "cadence": "Review after meaningful project changes or when the workflow feels brittle.",
    "signals": [
      "Humans repeatedly have to restate context.",
      "Agents stall because permissions are too weak or too broad.",
      "Reviews catch recurring classes of mistakes."
    ],
    "goals": [
      "Reduce human babysitting.",
      "Improve safety without making normal work painful."
    ],
    "recommendationFormat": "Short actionable recommendations grouped by risk and ergonomics."
  },
  "imports": [
    {
      "id": "paperclip",
      "type": "capabilityPack",
      "source": "https://paperclip.ing/",
      "version": "reference",
      "targets": [
        "cursor",
        "claude"
      ],
      "note": "Track external orchestrator ideas or future adapters here.",
      "trust": {
        "level": "review-required",
        "reviewedByHuman": false
      },
      "provides": {
        "notes": [
          "Review governance and ticketing patterns before adopting."
        ],
        "skills": []
      }
    },
    {
      "id": "example-mcp",
      "type": "mcp",
      "source": "npm:example-mcp-server",
      "version": "latest",
      "targets": [
        "cursor"
      ],
      "note": "Replace with a real MCP server when needed.",
      "trust": {
        "level": "review-required",
        "reviewedByHuman": false
      },
      "transport": {
        "type": "stdio",
        "command": "npx",
        "args": [
          "-y",
          "example-mcp-server"
        ],
        "env": {}
      },
      "provides": {
        "notes": [
          "Review what tools the MCP exposes."
        ],
        "skills": []
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

## Workflow

1. Fill in the spec block above.
2. Run `init-orch --cursor`, `init-orch --claude`, or `init-orch --all`.
3. Re-run the command whenever you change the orchestration design.
4. Review the generated recommendations block and decide which changes belong in the spec.

The generator will only rewrite the metadata and recommendations blocks below.

<!-- init-orch:generated:start -->
```json
{
  "version": 2,
  "lastRenderedAt": null,
  "renderedTargets": [],
  "generatedFiles": [],
  "bootstrapPreset": "engineering",
  "resolvedImports": []
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
