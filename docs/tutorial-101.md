# Tutorial 101

This walkthrough shows the full `init-orch` lifecycle on a small new repository.

## What you will learn

By the end, you will know how to:

1. bootstrap a first draft
2. improve that draft with `--suggest`
3. compile the generated files
4. tailor the setup with `--refine`
5. review the setup over time with `--review`

## The mental model

`init-orch.md` is the only high-level file you edit directly.

Everything else is generated from it:

- `AGENTS.md`
- `orch/*`
- `.cursor/*`
- `.claude/*`

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

## Step 2: Suggest

Before rendering, ask for a stronger first ansatz:

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

## Step 3: Compile

Once `init-orch.md` looks good enough, compile the target-specific files:

```bash
init-orch --all
```

This generates the files used by supported tools.

If `init-orch` detects existing owned-looking structure such as `.cursor/`, `.claude/`, `AGENTS.md`, or `orch/`, it stops and asks before overwriting in an interactive terminal.

For non-interactive runs:

```bash
init-orch --all --confirm-existing
```

## Step 4: Refine

After the first render, tailor the setup to the actual repository:

```bash
init-orch --refine
```

This asks for a short second pass of repo-specific details such as:

- the most common kinds of changes
- the main verification command
- sensitive paths
- existing conventions

Use this when the setup is structurally right but still missing local knowledge.

## Step 5: Review

Later, when the setup feels stale or off, run:

```bash
init-orch --review
```

This prints:

- a snapshot of the current state
- immediate actions
- setup recommendations

Use this as the maintenance loop after real work has happened in the repo.

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
- define success criteria
- add basic verification
- render once

Then refine and review as the repo becomes more real.
