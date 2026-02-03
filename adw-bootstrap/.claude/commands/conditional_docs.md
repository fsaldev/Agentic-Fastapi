# Conditional Documentation Guide

This guide helps you read only the documentation relevant to your current task.
**Read this file first** when starting any new session or task.

## Instructions

1. Identify your current task/context
2. Find matching conditions below
3. Read ONLY the documentation that matches your task
4. Skip irrelevant documentation to preserve context

## Documentation Routes

### Project Understanding
- **Linear Projects** (via `mcp__linear-server__get_project`)
  - When: Checking current project status
  - When: Need to see which features are done vs pending
  - When: Looking up Linear issue IDs for features

### Linear Issue Details
- **`mcp__linear-server__get_issue`** + **`mcp__linear-server__list_comments`**
  - When: Starting development on an issue (fetching requirements)
  - When: Reviewing implementation (checking acceptance criteria)
  - When: Looking for the implementation plan (posted as a comment during /develop)
  - Note: Linear is the single source of truth for requirements and plans

### Backend Development
- **app/server/README.md** (if exists)
  - When: Working on Python backend code
  - When: Adding API endpoints
  - When: Modifying database operations

- **app/client/src/style.css**
  - When: Making style/CSS changes to the client

### Frontend Development
- **app/client/README.md** (if exists)
  - When: Working on TypeScript/React frontend
  - When: Modifying UI components
  - When: Adding client-side features

### Testing
- **.claude/commands/test.md**
  - When: Running the test suite
  - When: Understanding test structure
  - When: Fixing failed tests

## Quick Reference

| Task | Read First |
|------|------------|
| New to project | CLAUDE.md |
| Project status | Linear Projects (MCP tools) |
| Implement feature | Linear issue details + comments |
| Review implementation | Linear issue + plan comment |
| Fix test | .claude/commands/test.md |
| Backend work | app/server/ |
| Frontend work | app/client/ |

## Notes

- Linear is the single source of truth for project status, requirements, and plans
- Use `mcp__linear-server__get_issue` for detailed implementation requirements
- Implementation plans are posted as Linear comments during the /develop phase
- Check issue comments for plan details when reviewing or resuming work
