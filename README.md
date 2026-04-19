# init-orch

`init-orch` is the practical runtime behind Zubeldia: a simple loop for solo coders who want to bootstrap an agent setup quickly, suggest a stronger repo-aware first draft, compile it from one source of truth, refine it for the actual repo, and review it deliberately over time.

Project's name on [Osvaldo Zubeldía](https://es.wikipedia.org/wiki/Osvaldo_Zubeld%C3%ADa), former DT Estudiantes de La Plata, world-champion 1968.

Instead of hand-editing `.cursor/`, `.claude/`, `AGENTS.md`, and related config files, you describe the workflow once in `init-orch.md` and generate the tool-specific files from that blueprint.

## The Product Loop

### Bootstrap

Run `init-orch` in a new repository and it can guide you through a short interactive setup:

```bash
init-orch
```

The bootstrap flow is intentionally small. It asks only for:

- a `workflow-domain` preset
- a short project summary
- target platforms
- a risk posture

It then creates a ready-to-edit `init-orch.md` and points you to the next fields worth refining.

If you already know what you want, you can skip the prompts and bootstrap directly:

```bash
init-orch --preset engineering-web-app --no-interactive
```

### Compile

`init-orch.md` is the canonical source of truth. Edit that file, then compile the target-specific outputs:

```bash
init-orch --all
```

That generates:

- `AGENTS.md`
- `orch/permissions.policy.json`
- `orch/imports.lock.json`
- `orch/evaluation.plan.json`
- `.cursor/` rules, skills, imports, and MCP config
- `.claude/` settings, rules, agents, skills, and imports

The compile step is the strongest idea in the project: one high-level spec, many generated outputs, explicit review before changing the setup.

If `init-orch` detects existing owned-looking structure such as `orch/`, `.cursor/`, `.claude/`, `AGENTS.md`, or an existing `.gitignore` line update, it will stop and ask for confirmation in a terminal. In non-interactive runs, re-run with:

```bash
init-orch --all --confirm-existing
```

### Suggest

If you want a better first ansatz before rendering, ask for a repo-aware proposal:

```bash
init-orch --suggest
```

This samples a small amount of repo evidence and proposes updates for `project.summary`, `project.mission`, `project.successCriteria`, and `verification`. It prints the proposal first and only applies it if you confirm.

### Refine

After the first render, tailor the setup to the real repository:

```bash
init-orch --refine
```

This asks for a short second pass of repo-specific details such as the most important verification command, sensitive paths, and existing conventions. The goal is to keep bootstrap minimal while still making the setup feel native to the repo.

### Review

When the setup feels stale or off, ask for a deliberate review:

```bash
init-orch --review
```

This prints a short snapshot, immediate actions, and practical setup recommendations without rewriting files. It now also tries to surface repo-specific issues such as path collisions, missing canonical verification commands, and workspace-style structure. The goal is not an always-on orchestration brain. The goal is a lightweight review loop that helps you tighten the setup when it matters.

## Why This Is Useful

This is aimed at solo coders and small independent setups, not enterprise governance.

It is useful when you want to:

- get from zero to a decent multi-agent setup in a few minutes
- keep Cursor and Claude aligned without duplicating effort
- keep permissions, roles, and verification expectations explicit
- improve the setup over time without rebuilding it from scratch
- carry the same orchestration intent from project to project

The practical promise is portability of intent, not perfect invariance across every future platform.

## Presets

Presets use `workflow-domain` form, for example:

- `research-docs`
- `engineering-web-app`
- `poc-data-science`

Available workflows:

| Workflow | Best For | Bias |
| --- | --- | --- |
| `research` | Exploratory work, synthesis, and careful source-driven iteration | Stronger evidence discipline, less production pressure |
| `engineering` | Maintainable long-term delivery | Balanced default, stronger production-readiness |
| `poc` | Fast experiments and idea validation | Lighter process, faster iteration |

Available domains:

| Domain | Best For | Bias |
| --- | --- | --- |
| `generic` | Libraries, APIs, backends, CLIs, and general software repos | Broad default |
| `web-app` | Frontend or full-stack apps with UI work | Stronger UI and behavior verification |
| `data-science` | Notebooks, experiments, and models | Stronger reproducibility and experiment review |
| `infra` | Infrastructure, automation, and ops work | Stricter safety and approval defaults |
| `docs` | Documentation-first repositories | Stronger editorial review |
| `multimedia` | Asset-heavy or multimodal workflows | Stronger review and provenance awareness |

The default preset is `engineering-generic`.

`project.riskPosture` stays separate from the preset so you can tune how cautious the setup should be.

## What To Fill In First

If the project is still fuzzy, do not try to perfect the whole spec.

1. Start with project shape and guardrails: `preset`, mission, success criteria, targets, stop conditions, verification, and `toolPolicy`.
2. Add roles, handoffs, and high-level rules.
3. Add imports, MCPs, and target-specific overrides once the core workflow is clear.
4. Add skills after that.
5. Tune evaluation and review refinements last.

For a first useful pass, steps 1 and 2 are enough.

## Installation

Requirements:

- `python3`

Clone the repo and make the script available on your `PATH`:

```bash
git clone <your-repo-url> "$HOME/.local/share/init-orch"
chmod +x "$HOME/.local/share/init-orch/init-orch"
mkdir -p "$HOME/.local/bin"
ln -sf "$HOME/.local/share/init-orch/init-orch" "$HOME/.local/bin/init-orch"
```

Make sure `~/.local/bin` is on your `PATH`, then verify:

```bash
init-orch --help
```

## Short Example

```bash
mkdir my-new-repo && cd my-new-repo
init-orch
init-orch --suggest
# review and refine init-orch.md
init-orch --all
init-orch --refine
init-orch --review
```

If you want a longer walkthrough, see `docs/quickstart.md`.

## Roadmap

Planned next steps:

- keep improving the bootstrap flow while preserving a fast non-interactive path
- make the refine step smarter without turning it into a long interview
- strengthen review recommendations with limited local context
- improve target-specific rendering without bloating the core workflow
- explore additional adapters after the bootstrap and review loop feel solid
