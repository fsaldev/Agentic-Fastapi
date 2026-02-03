# ADW - AI Developer Workflow

An agentic development environment that automates the software development lifecycle using Claude Code.

## Features

- **Zero-Touch Mode**: Provide a feature description, ADW automatically implements, tests, reviews, and deploys
- **Interactive Project Mode**: Collaborate with Claude to plan an entire project, create Linear issues, then execute
- **Full Pipeline**: Develop → Test → Review → Deploy

## Quick Start

### 1. Install Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- [uv](https://github.com/astral-sh/uv) package manager
- [GitHub CLI](https://cli.github.com/) (`gh`)
- Git repository initialized

### 2. Run Setup Script

```bash
# From your project root
./adw-bootstrap/setup.sh
```

Or manually:
```bash
# Copy .claude folder to your project
cp -r adw-bootstrap/.claude .

# Add to .gitignore
echo ".claude/workflows/" >> .gitignore

# Create pyproject.toml if needed (for uv)
cat >> pyproject.toml << 'EOF'
[project]
name = "your-project"
version = "0.1.0"
requires-python = ">=3.11"
EOF
```

### 3. Configure Linear MCP (Optional)

For Linear issue tracking, add to your Claude Code MCP config (`~/.claude/mcp.json` or `.claude/.mcp.json`):

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server"],
      "env": {
        "LINEAR_API_KEY": "your_linear_api_key"
      }
    }
  }
}
```

### 4. Configure Permissions

Add these permissions to `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(git status:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(git checkout:*)",
      "Bash(git branch:*)",
      "Bash(git log:*)",
      "Bash(git diff:*)",
      "Bash(gh pr create:*)",
      "Bash(gh pr merge:*)",
      "Bash(gh pr review:*)",
      "Bash(uv run:*)",
      "Bash(npm:*)",
      "mcp__linear__list_projects",
      "mcp__linear__get_project",
      "mcp__linear__create_project",
      "mcp__linear__update_project",
      "mcp__linear__list_issues",
      "mcp__linear__get_issue",
      "mcp__linear__create_issue",
      "mcp__linear__update_issue",
      "Edit",
      "Write"
    ]
  }
}
```

### 5. Create Project Guidelines (Optional)

Copy and customize `CLAUDE.md.template` for project-specific Claude Code guidelines:

```bash
cp adw-bootstrap/CLAUDE.md.template CLAUDE.md
# Edit CLAUDE.md with your project details
```

This includes the **bug documentation policy** - all bug fixes are automatically logged to Linear.

## Usage

### CLI Commands

```bash
# Zero-touch: full pipeline from description
uv run .claude/adw/cli.py run "Add user authentication"

# Interactive project planning
uv run .claude/adw/cli.py project "Build a todo app"

# Individual phases (using workflow ID)
uv run .claude/adw/cli.py develop <workflow_id>
uv run .claude/adw/cli.py test <workflow_id>
uv run .claude/adw/cli.py review <workflow_id>

# Status
uv run .claude/adw/cli.py list
uv run .claude/adw/cli.py status <workflow_id>
```

### Slash Commands (in Claude Code)

| Command | Description |
|---------|-------------|
| `/run` | Zero-touch: develop, test, review, deploy |
| `/project` | Interactive project planning with Linear |
| `/develop` | Implement from Linear issue |
| `/test` | Run tests and fix failures |
| `/review` | Review implementation against requirements |
| `/bugfix` | Fix a bug and auto-document in Linear |
| `/prime` | Onboard to the codebase |

## Pipeline Flow

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ DEVELOP │───►│  TEST   │───►│ REVIEW  │───►│ DEPLOY  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │
     ▼              ▼              ▼              ▼
  Fetches from   Runs tests    Reviews vs    Commits &
  Linear, plans  with auto-    requirements  pushes to
  & implements   fix retry     fixes issues  remote
```

## Directory Structure

```
.claude/
├── adw/                        # Core Python framework
│   ├── cli.py                  # CLI entry point
│   ├── agent.py                # Claude Code integration
│   ├── git_ops.py              # Git/GitHub operations
│   ├── linear.py               # Linear MCP integration
│   ├── logger.py               # Logging utilities
│   ├── state.py                # Workflow state management
│   └── workflows/              # Pipeline phases
│       ├── develop.py
│       ├── test.py
│       ├── review.py
│       ├── full.py
│       └── project.py
├── commands/                   # Slash commands
│   ├── bugfix.md
│   ├── conditional_docs.md
│   ├── develop.md
│   ├── prime.md
│   ├── project.md
│   ├── review.md
│   ├── run.md
│   └── test.md
└── workflows/                  # Runtime state (gitignored)
    └── {workflow_id}/
        ├── state.json
        └── logs/
```

## Customization

### Adding Test Commands

Edit `.claude/commands/test.md` to specify your project's test command:

```markdown
## Test Command
npm test
# or: pytest, go test, etc.
```

### Modifying Review Criteria

Edit `.claude/commands/review.md` to adjust code review standards.

### Custom Pipeline Phases

Add new phases by:
1. Creating `.claude/adw/workflows/your_phase.py`
2. Creating `.claude/commands/your_phase.md`
3. Integrating into `full.py` pipeline

## Troubleshooting

### Claude Code not found
```bash
export CLAUDE_CODE_PATH=/path/to/claude
```

### Linear issues not fetching
Ensure Linear MCP is configured in your Claude Code settings.

### Tests failing repeatedly
Check `.claude/workflows/{id}/logs/` for detailed test output.

## License

MIT
