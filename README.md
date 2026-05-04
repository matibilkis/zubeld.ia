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
