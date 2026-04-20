# Tutorial 101

This walkthrough is the lightweight 101 for `init-orch`.

The goal is not to teach every feature up front. The goal is to get to a usable first render quickly, then show which extra steps are worth using later.

For a minimal working setup, expect roughly:

- 2-5 minutes to bootstrap and render a first ready-to-use Cursor/Claude setup
- 10-20 minutes if you also want to tune verification, response style, and repo-specific defaults

## What you will learn

By the end, you will know how to:

1. bootstrap a first draft
2. improve that draft with `--suggest`
3. compile the generated files
4. decide when `--suggest`, `--refine`, `--review`, and `--parity` are actually worth using

## The mental model

`init-orch.md` is the only high-level file you edit directly.

Everything else is generated from it:

- `AGENTS.md`
- `orch/*`
- `.cursor/*`
- `.claude/*`

That means the first success condition is simple: get a usable `init-orch.md`, render once, and stop. Everything after that is enhancement, not mandatory overhead.

## Step 1: Bootstrap

In a new repository, run:

```bash
init-orch
```

This creates `init-orch.md`.

If you already know the preset you want, you can skip the prompts:

```bash
init-orch --preset engineering-generic --no-interactive
```

The preset is only the starting point. After bootstrap, edit `init-orch.md` to override any default.

### Choosing a preset quickly

Presets use `workflow-domain` form:

- workflows: `research`, `engineering`, `poc`
- domains: `generic`, `web-app`, `data-science`, `infra`, `docs`, `multimedia`

Good defaults when you are unsure:

- `engineering-generic` for most software repos
- `research-docs` for exploratory or writing-heavy work
- `engineering-web-app` for product/UI repos
- `poc-data-science` for experiment-heavy notebook work

Think of the preset as a first draft, not a lock-in. Pick the closest one, then edit `init-orch.md` to change mission, `responseStyle`, verification, roles, imports, or anything else.

## Optional Step 2: Suggest

Before rendering, ask for a stronger first ansatz only if the first draft is still too generic:

```bash
init-orch --suggest
```

This proposes updates for:

- `project.summary`
- `project.mission`
- `project.successCriteria`
- `verification`

It prints the proposal first and only applies it if you confirm.

Use this when the generated spec is directionally right but still too generic.

## Step 2: Compile

Once `init-orch.md` looks good enough, compile the target-specific files:

```bash
init-orch --all
```

This generates the files used by supported tools.

If you want a review-first path before writing files:

```bash
init-orch --all --dry-run
```

If `init-orch` detects existing owned-looking structure such as `.cursor/`, `.claude/`, `AGENTS.md`, or `orch/`, it stops and asks before overwriting in an interactive terminal.

For non-interactive runs:

```bash
init-orch --all --confirm-existing
```

## Optional integrations later

The first useful render does not require more imports than the default template entry.

- keep the default `find-skills` import only as a template, or delete it if you do not want an external skill example yet
- `mcp` imports are the only ones that currently affect MCP wiring
- `skillPack` and `capabilityPack` imports are declarative today, not installed automatically
- copy the default `find-skills` import when you want to model another external skill
- add reusable `skills` only after repeated work patterns are real

For the exact roadmap and behavior, see `README.md` or `docs/quickstart.md`.

## Optional Step 3: Refine

After the first render, tailor the setup to the actual repository:

```bash
init-orch --refine
```

This asks for a short second pass of repo-specific details such as:

- the most common kinds of changes
- the main verification command
- sensitive paths
- existing conventions

Use this when the setup is structurally right but still missing local knowledge. If refine notes already exist, the command keeps them by default and only re-asks them if you choose to update them.

## Optional Step 4: Review

Later, when the setup feels stale or off, run:

```bash
init-orch --review
```

This prints:

- a snapshot of the current state
- immediate actions
- setup recommendations

Use this as the maintenance loop after real work has happened in the repo.

## Optional Step 5: Parity

If you want to inspect Cursor/Claude alignment directly:

```bash
init-orch --parity
```

Use this when you want to see what is shared, what is target-specific, and whether one target has drifted behind the other.

## Example full flow

```bash
mkdir my-new-repo && cd my-new-repo
init-orch
init-orch --suggest
# review and edit init-orch.md
init-orch --all
init-orch --refine
init-orch --review
```

## When to stop

Do not try to perfect the whole spec before the first render.

A good first pass is:

- choose the preset
- write a usable summary and mission
- set `responseStyle` if you already know the tone and length you want
- define success criteria
- add basic verification
- render once

Then stop. Only add `--suggest`, `--refine`, `--review`, or `--parity` when the repo actually needs them.
