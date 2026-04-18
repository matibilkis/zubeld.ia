# init-orch

`init-orch` bootstraps and re-renders agent orchestration files for a repository from one editable source: `init-orch.md`.

Project's name on [Osvaldo Zubeldía](https://es.wikipedia.org/wiki/Osvaldo_Zubeld%C3%ADa), former DT Estudiantes de La Plata, world-champion 1968.

Instead of hand-editing `.cursor/`, `.claude/`, `AGENTS.md`, and related config files, you describe your intended workflow, permissions, roles, imports, and evaluation loop once, then generate the target-specific files from that blueprint.

## What It Does

- Creates `init-orch.md` in a new repo.
- Uses that file as the canonical source of truth.
- Can bootstrap that first blueprint from a composed workflow-domain preset.
- Generates:
  - `AGENTS.md`
  - `orch/permissions.policy.json`
  - `orch/imports.lock.json`
  - `orch/evaluation.plan.json`
  - `.cursor/` rules, skills, imports, and MCP config
  - `.claude/` settings, rules, agents, skills, and imports
- Re-generates recommendations so you can iteratively improve the orchestration as the project evolves.

## Why It Helps

Most adjacent tools either:
- generate one agent file,
- sync configs across tools,
- or ship reusable prompt/skill packs.

`init-orch` is different in one important way: it treats the whole repo setup as a small orchestration system compiled from a single spec.

That makes it useful when you want to:
- keep Cursor and Claude aligned without duplicating effort,
- evolve your human-agent workflow over time,
- import MCPs or capability packs in a structured way,
- keep permissions and safety expectations explicit,
- review recommendations before changing the canonical setup.

## Practical Use

In a brand new repo:

```bash
init-orch
```

That creates `init-orch.md`.

If you want a stronger first draft, start with a preset:

```bash
init-orch --preset engineering-web-app
```

Presets now compose a workflow and a domain in `workflow-domain` form, for example:

- `research-docs`
- `engineering-web-app`
- `poc-data-science`

Available workflows:

| Workflow | Best For | Strengths | Weaknesses |
| --- | --- | --- | --- |
| `research` | Academic or exploratory work, synthesis, literature review, and careful iteration | Stronger evidence discipline, clearer assumptions, better support for source-driven work | Less optimized for shipping production-ready changes quickly |
| `engineering` | Long-term software delivery and maintainable production work | Stronger maintainability, reviewability, and production-readiness | Can feel heavy for open-ended exploration or very early ideas |
| `poc` | Rapid prototyping and quick idea validation | Low ceremony, fast iteration, optimized for momentum | Encourages shortcuts that should later harden into research or engineering |

Available domains:

| Domain | Best For | Strengths | Weaknesses |
| --- | --- | --- | --- |
| `generic` | Libraries, APIs, backends, CLIs, and general software repos | Broad default with minimal assumptions | Less tailored than domain-specific presets |
| `web-app` | Frontend or full-stack apps with UI flows and browser-based verification | Good fit for interaction testing, app flows, and user-facing checks | Adds unnecessary assumptions for non-UI repos |
| `data-science` | Notebook-heavy analysis, experiments, modeling, and evaluation | Better support for experiments, metrics, and reproducibility notes | Less focused on production hardening by default |
| `infra` | Ops, deployment, automation, and environment-heavy repositories | Stronger operational safety, explicit blast-radius review, careful change control | Can slow down fast product exploration |
| `docs` | Documentation-first repos and writing-heavy workflows | Clearer editorial structure, consistency, and reviewability | Less tailored to runtime behavior and implementation work |
| `multimedia` | Projects involving media assets, generation, transformation, or review | Better fit for multimodal workflows and asset-heavy tasks | Less useful for pure codebases with little media handling |

The default preset is `engineering-generic`.

`project.riskPosture` is still a separate field in `init-orch.md`. It is not part of the preset; use it only if you want to tune how cautious or permissive the orchestration should be beyond the workflow/domain default.

Future direction: a later version could ask for a short free-form project description and recommend the closest workflow-domain preset automatically.

Edit `init-orch.md` with:
- your project mission,
- roles such as planner / implementer / reviewer / evaluator,
- workflow and verification rules,
- permission policy,
- imports such as MCPs or capability packs.

Then render everything:

```bash
init-orch --all
```

Now work normally in the repo. When the setup feels off, update `init-orch.md`, re-run `init-orch --all`, and review the generated recommendations block to decide what should become part of the canonical orchestration.

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
init-orch --preset research-docs
# edit init-orch.md
init-orch --all
```

If you want a longer example, see `docs/quickstart.md`.

## Roadmap

Not implemented yet, but planned:

- stronger import resolution for real MCP registries and third-party packs
- better target-specific rendering beyond Cursor and Claude
- richer evaluator logic based on actual repo usage, not only static spec analysis
- interactive workflow-domain recommendation from a short project description
- adapters for external orchestration runtimes and ecosystems
