# TDL: init-orch Meta-Plan

This document turns the current product direction into an incremental build plan.

Guiding principle: keep `init-orch` small, fast, and trustworthy. The goal is not to become a general agent platform. The goal is to make repo-local Cursor/Claude setup useful in minutes, then keep it reviewable over time.

## Product Goal

Ship a version of `init-orch` that is:

- ready to use in 2-5 minutes for a minimal setup
- clearly preset-driven but easy to override
- strong enough at `--suggest` that it saves real setup work
- good at shaping assistant behavior through `responseStyle`
- trustworthy in what it generates and conservative in what it changes
- clearly valuable for mixed Cursor/Claude workflows

## Non-Goals

- do not become a swarm runtime or agent execution engine
- do not add more generated files unless they clearly improve trust or usability
- do not make first-run setup slower in exchange for theoretical flexibility

## Prioritization Rule

Build in this order:

1. make first-run setup dead simple
2. make `--suggest` dramatically better and more explainable
3. make presets inspectable and override flow obvious
4. make `responseStyle` preset-aware
5. make generated files shorter and more trustworthy
6. add mixed-target parity and review features
7. only then add more power features

## The 10 Items

### 1. Minimal First-Run Path
Priority: now

Goal:
- get from zero to a working Cursor/Claude setup in 2-5 minutes

Work:
- add a minimal-first bootstrap path
- keep initial prompts to the smallest useful set
- render immediately useful outputs after bootstrap
- print exactly one best next step after completion

Acceptance:
- new user can run `init-orch`, answer a few prompts, run `init-orch --all`, and have usable generated files without reading long docs first
- README and quickstart both show this path clearly

### 2. Preset Discovery UX
Priority: now

Goal:
- make presets understandable before the user commits to one

Work:
- add `--list-presets`
- add `--explain-preset <name>`
- improve CLI help text around workflow vs domain
- show recommended defaults for uncertain users

Acceptance:
- user can understand what `engineering-web-app` or `research-docs` means without opening code or docs
- preset choice feels guided, not guessy

### 3. Override Flow And Provenance
Priority: now

Goal:
- make it obvious what came from the preset and what the user can freely change

Work:
- improve docs and generated comments around “preset = starting draft”
- mark or explain preset-derived defaults in `init-orch.md`
- add a preset comparison or diff view later if still needed

Acceptance:
- new user understands that every field in `init-orch.md` is editable
- users do not confuse preset defaults with hard constraints

### 4. `--suggest` Verification Inference
Priority: now

Goal:
- infer better repo checks and safer verification guidance

Work:
- prefer real repo commands from manifests, CI, and test configs
- improve language-specific verification detection
- avoid weak or misleading fallback checks
- keep docs checks separate from code checks

Acceptance:
- `--suggest` names useful verification commands in common repos
- smoke tests on mixed repos and script-first repos stay clean

### 5. `--suggest` Explainability And Confidence
Priority: next

Goal:
- make suggestion output easier to trust

Work:
- expose why a summary, mission, or check was suggested
- classify evidence by identity, workflow, verification, and safety
- prefer conservative suggestions when confidence is low
- ask targeted open questions instead of guessing aggressively

Acceptance:
- suggestion report explains what evidence drove each recommendation
- users can tell when the tool is confident and when it is probing

### 6. Preset-Aware `responseStyle`
Priority: next

Goal:
- make response behavior feel native to presets, not bolted on

Work:
- add workflow/domain-specific `responseStyle` defaults
- define a few named style profiles internally
- keep `responseStyle` editable in the spec
- ensure generated Cursor/Claude guidance reflects it consistently

Acceptance:
- `research-*`, `engineering-*`, and `docs-*` feel meaningfully different in generated style guidance
- user can still override tone, verbosity, structure, length, rules, and examples directly

### 7. Trustworthy Generated Files
Priority: next

Goal:
- make generated outputs easy to read and easy to trust

Work:
- keep generated files short and purpose-specific
- add or preserve clear generated headers
- support dry-run and diff-oriented workflows where useful
- reduce unnecessary noise in generated content

Acceptance:
- generated files look intentional, not bloated
- users can review them quickly and understand why they exist

### 8. Low-Babysitting Refinement And Review
Priority: next

Goal:
- reduce repeated manual steering and repetitive recommendations

Work:
- make every command end with one best next step
- avoid re-asking known repo facts in `--refine`
- make `--review` shorter and better ranked
- suppress repeated recommendations unless state changed

Acceptance:
- repeated use feels lighter, not more annoying
- refinement and review save time instead of creating recurring chores

### 9. Mixed Cursor/Claude Parity
Priority: later

Goal:
- make the cross-target value obvious and measurable

Work:
- add a target comparison or parity view
- explain what is shared vs target-specific
- surface drift between Cursor and Claude outputs in review
- preserve one-source-of-truth while allowing target-specific differences

Acceptance:
- users can clearly see why using `init-orch` is better than hand-maintaining `.cursor/` and `.claude/` separately

### 10. Adoption Proof And Product Tightening
Priority: later

Goal:
- validate that `init-orch` is solving a real problem and not becoming config theater

Work:
- run more realistic smoke tests on live repos
- keep onboarding docs short and practical
- tighten product positioning around the real wedge
- prune features that do not improve first-week usefulness

Acceptance:
- setup time stays low
- docs remain beginner-friendly
- the project description stays honest: blueprint-first repo-local agent setup, not a full agent runtime

## Suggested Session Order

### Session A
- item 1: minimal first-run path
- item 2: preset discovery UX
- item 3: override flow and provenance

### Session B
- item 4: `--suggest` verification inference
- item 5: `--suggest` explainability and confidence

### Session C
- item 6: preset-aware `responseStyle`
- item 7: trustworthy generated files

### Session D
- item 8: low-babysitting refinement and review
- item 9: mixed Cursor/Claude parity

### Session E
- item 10: adoption proof and product tightening

## Success Metrics

- new user can reach first render in 2-5 minutes
- realistic repo setup with `--suggest` and `--refine` fits in 10-20 minutes
- generated outputs are reviewed, not ignored
- `--suggest` feels more helpful than generic
- mixed Cursor/Claude users feel clear value from one source of truth

## Final Product Test

This plan is working if a user can say:

- “I got a usable setup fast.”
- “I understood the preset and changed what mattered.”
- “The suggestions were mostly right and easy to trust.”
- “The generated files looked clean.”
- “I did not have to babysit the tool much.”
- “It actually helped keep Cursor and Claude aligned.”

If that is not true, the right move is not more abstraction. The right move is to simplify the product again.
