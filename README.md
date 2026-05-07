# init-orch

Minimal Claude Code setup wizard. Run it once in a new repo, answer 3 questions, done.

## What it generates

- `CLAUDE.md` — project context, commands, rules, and response style examples
- `.claude/settings.json` — safe default permissions
- `.gitignore` entry for `.claude/settings.local.json`

## Install

```bash
git clone <repo-url> "$HOME/.local/share/init-orch"
chmod +x "$HOME/.local/share/init-orch/init-orch"
ln -sf "$HOME/.local/share/init-orch/init-orch" "$HOME/.local/bin/init-orch"
```

## Use

```bash
cd your-repo
init-orch
```

After that, edit `CLAUDE.md` directly. It is not regenerated.

## What to do next

Do not run `/init` in Claude Code after init-orch — it would overwrite `CLAUDE.md` and lose the rules and response style structure. Instead:

1. Paste the **"Generate Cursor core.mdc"** prompt from `prompt-dict.md` into Claude or Cursor to generate `.cursor/rules/core.mdc`.
2. Paste the **"Audit CLAUDE.md against the actual repo"** prompt — Claude reads your codebase and proposes improvements to `CLAUDE.md` without losing its structure. This replaces what `/init` would have done.

After your first real session, use the calibration prompts to tighten `CLAUDE.md`. As the project grows, use the extension prompts to add path-scoped rules and MCP servers.

## Local broader permissions

Create `.claude/settings.local.json` (gitignored) if you want Claude to edit and run commands without prompting:

```json
{
  "permissions": {
    "allow": ["Bash(*)", "Edit(*)", "Write(*)", "Read(*)", "Glob(*)", "Grep(*)", "WebFetch(*)", "WebSearch(*)"],
    "defaultMode": "acceptEdits"
  }
}
```

## MCP servers

Browse [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) (86k stars) for tools to add. Wire them via Claude Code's `/mcp` command or directly in settings.
