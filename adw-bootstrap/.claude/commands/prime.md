# Prime

Onboard to the codebase for a new session. Run this command when starting fresh to understand the project context and current work state.

## Instructions

1. Read core documentation and current work state
2. Check Linear for incomplete issues
3. Summarize your understanding and what to do next

## Explore

List all tracked files to understand the project structure:

```bash
git ls-files
```

## Read

Read these files in order:

1. **CLAUDE.md** - Project guidelines and workflow rules
2. **.claude/current-work.md** - Current work in progress (active issue, status, recent changes)
3. **.claude/commands/conditional_docs.md** - Documentation routing guide

## Check Linear

**IMPORTANT: NEVER query for Done or Canceled issues. Only query the three states listed below.**

1. Use `mcp__linear-server__list_issues` with project "Job Posting" and state "Backlog"
2. Use `mcp__linear-server__list_issues` with project "Job Posting" and state "Todo"
3. Use `mcp__linear-server__list_issues` with project "Job Posting" and state "In Progress"

Do NOT use `list_issues` without a state filter. Do NOT query for state "Done" or "Canceled".
Do NOT use `get_project`.

## Output

After reading, provide a concise summary:

1. **Current Work**: What's actively being worked on (from .claude/current-work.md)
2. **Open Issues**: List any incomplete issues (Backlog, Todo, In Progress). If none exist, state "All issues complete."
3. **Next Action**: What to do next — resume an issue with `/run <issue_id>`, or note that the workspace is idle
