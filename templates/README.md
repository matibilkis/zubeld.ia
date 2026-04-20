# init-orch templates

These are reference copies for the blueprint-first workflow.

`init-orch.md` is the only file a repository owner is expected to edit directly. Everything under `.cursor/`, `.claude/`, `AGENTS.md`, and `orch/` should be treated as generated output.

The checked-in `templates/init-orch.md` mirrors the default `engineering-generic` preset.

The richer blueprint now supports:
- workflow and verification guidance
- response-style guidance for tone, verbosity, structure, and examples
- evaluator recommendations
- import declarations for MCPs and external capability packs
- explicit security warnings around powerful permissions

Import roadmap, as intended today:
- first render should work with the default `find-skills` import left in place only as a template, or removed entirely
- `mcp` imports can drive manifests and Cursor MCP config
- other import types stay declarative until a future resolver/installer exists
- the default `find-skills` import shows how to model other external skill imports

It also follows an importance-first order:
- start with project shape, verification, stop conditions, and permission boundaries
- add roles and handoffs next
- add imports, MCPs, skills, and evaluator refinements only after the core workflow feels right

Typical flow:

1. Run `init-orch` in a new repository.
2. Fill in `init-orch.md`.
3. Run `init-orch --cursor`, `init-orch --claude`, or `init-orch --all`.
4. Review the generated recommendations and decide what to fold back into `init-orch.md`.
