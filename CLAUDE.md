# Claude Code Guidelines

Project-specific instructions for Claude Code when working in this repository.

## Project Context

- **Project**: Rent a Car Backend API
- **Language**: Python
- **Framework**: FastAPI (assumed based on project structure)

## Current Work Tracking (MANDATORY)

**You MUST keep `.claude/current-work.md` updated at all times.**

This file tracks what's currently being worked on. Update it:
- **When starting work** - Set the active issue, title, and status
- **During development** - Update status, recent changes, and files modified
- **When completing work** - Clear the active issue or note completion
- **When switching tasks** - Update to reflect the new work

### What to Update

```markdown
## Active Issue
- **Issue**: Issue ID (or "None" / "Ad-hoc")
- **Title**: Brief description
- **Branch**: current branch name
- **Started**: YYYY-MM-DD

## Status
What you're currently doing (1-2 sentences)

## Recent Changes
- Change 1
- Change 2

## Files Modified
- path/to/file1.py
- path/to/file2.py

## Next Steps
- What needs to be done next

## Notes
Any important context, blockers, or decisions
```

### When to Update

| Action | Update current-work.md |
|--------|----------------------|
| Start working on an issue | Set Active Issue, Status |
| Make code changes | Add to Recent Changes, Files Modified |
| Complete a task | Update Status, Next Steps |
| Hit a blocker | Add to Notes |
| Finish work | Clear Active Issue or mark complete |
| Answer questions / research | Update Status with context |

## Commit Message Conventions

- `feat:` - New feature
- `fix:` - Bug fix
- `chore:` - Maintenance tasks
- `refactor:` - Code refactoring
- `docs:` - Documentation changes
- `test:` - Adding or updating tests

## Code Style

- Follow existing patterns in the codebase
- Use Python type hints where appropriate
- Follow PEP 8 conventions
- Keep changes minimal and focused

## Testing

Before completing work:
- Verify changes work as expected
- Run existing tests if available
- Test edge cases when relevant

## Linear Integration

- Use MCP tools (`mcp__linear__*`) for Linear operations when configured
- Link issues to the relevant project
- Update issue status when work is complete
