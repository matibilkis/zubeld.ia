# init-orch

`init-orch` bootstraps and re-renders agent orchestration files for a repository from one editable source: `init-orch.md`.

Instead of hand-editing `.cursor/`, `.claude/`, `AGENTS.md`, and related config files, you describe your intended workflow, permissions, roles, imports, and evaluation loop once, then generate the target-specific files from that blueprint.

## What It Does

- Creates `init-orch.md` in a new repo.
- Uses that file as the canonical source of truth.
- Can bootstrap that first blueprint from a repo-type preset.
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
init-orch --preset web-app
```

Available presets:

| Preset | Best For | Strengths | Weaknesses |
| --- | --- | --- | --- |
| `research` | Exploratory work, experiments, rapid iteration, evaluation-heavy loops | Flexible, fast to adapt, good for trying ideas and debugging on the fly | Less opinionated about delivery discipline and production hardening |
| `engineering` | Shipping software with clear implementation, review, and verification stages | Repeatable workflow, stronger quality controls, clearer role separation | Can feel heavy for open-ended exploration or very early ideas |
| `web-app` | Frontend or full-stack apps with UI flows and browser-based verification | Good fit for interaction testing, app flows, and user-facing checks | Adds unnecessary assumptions for non-UI repos |
| `poc` | Proving an idea quickly with minimal setup | Low ceremony, fast to start, optimized for momentum | Weaker on long-term maintainability, review depth, and hardening |
| `multimedia` | Projects involving media assets, generation, transformation, or review | Better fit for multimodal workflows and asset-heavy tasks | Less useful for pure codebases with little media handling |
| `infra` | Ops, deployment, automation, and environment-heavy repositories | Stronger safety posture, explicit permissions, careful change control | Can slow down fast product exploration |
| `docs` | Documentation-first repos and writing-heavy workflows | Clearer editorial structure, consistency, and reviewability | Less tailored to implementation and runtime verification |

Future direction: a later version could ask for a short free-form project description and recommend the closest preset automatically.

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
init-orch --preset research
# edit init-orch.md
init-orch --all
```

If you want a longer example, see `docs/quickstart.md`.

## Roadmap

Not implemented yet, but planned:

- stronger import resolution for real MCP registries and third-party packs
- better target-specific rendering beyond Cursor and Claude
- richer evaluator logic based on actual repo usage, not only static spec analysis
- interactive preset recommendation from a short project description
- adapters for external orchestration runtimes and ecosystems
- composable profiles beyond a single preset, such as vertical + risk posture
