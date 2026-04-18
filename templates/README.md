# init-orch templates

These are reference copies for the blueprint-first workflow.

`init-orch.md` is the only file a repository owner is expected to edit directly. Everything under `.cursor/`, `.claude/`, `AGENTS.md`, and `orch/` should be treated as generated output.

The checked-in `templates/init-orch.md` mirrors the default `engineering` preset.

The richer blueprint now supports:
- workflow and verification guidance
- evaluator recommendations
- import declarations for MCPs and external capability packs
- explicit security warnings around powerful permissions

Typical flow:

1. Run `init-orch` in a new repository.
2. Fill in `init-orch.md`.
3. Run `init-orch --cursor`, `init-orch --claude`, or `init-orch --all`.
4. Review the generated recommendations and decide what to fold back into `init-orch.md`.
