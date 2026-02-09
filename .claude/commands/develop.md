# Develop

Implement a feature from a Linear issue. Fetches requirements, plans, and implements.

Can be run standalone (`/develop ACA-123`) or as part of the `/run` pipeline.

## Variables

- `issue_id`: $1 - Linear issue ID (e.g., "ACA-123") or feature description

## Instructions

1. **Fetch Issue Details**
   - Use `mcp__linear-server__get_issue` to fetch the issue by `issue_id`
   - Extract: title, description, labels, priority, acceptance criteria
   - Use `mcp__linear-server__list_comments` to check for any existing context or plan comments

2. **Read Context**
   - Read `.claude/commands/conditional_docs.md`
   - Read any additional docs relevant to the task
   - Explore relevant source files to understand existing patterns

3. **Create Implementation Plan**
   Build a plan covering:
   - Summary of what needs to be done
   - Implementation steps (ordered)
   - Files to modify/create
   - Validation commands to run after

4. **Post Plan to Linear**
   Post the plan as a comment on the issue using `mcp__linear-server__create_comment`:
   ```markdown
   ## Implementation Plan

   ### Summary
   {2-3 sentence description}

   ### Steps
   1. {Step 1}
   2. {Step 2}
   ...

   ### Files to Modify
   - `path/to/file` - {reason}

   ### Validation
   - {How to verify the implementation works}
   ```

5. **Implement**
   - Follow the plan steps in order
   - Make changes to the listed files
   - Follow existing code patterns

6. **Validate**
   - Run the validation commands from the plan
   - Fix any issues that arise
   - Ensure all tests pass

7. **Post Completion Comment**
   Post a comment using `mcp__linear-server__create_comment`:
   ```markdown
   ## Development Complete

   ### Files Changed
   {list files from git diff --stat}

   ### Summary
   {what was implemented}
   ```

### 8. **Update Tracking** (standalone only — skip if called from `/run`)
   - Update `.claude/current-work.md` with recent changes and files modified

## Guidelines

- Follow existing code style and patterns
- Don't over-engineer - implement exactly what's needed
- If something is unclear, check the Linear issue again
- Commit frequently with clear messages
- The agent should strictly limit its work to what is explicitly stated in the ticket and must not perform any tasks outside the scope of the issue.
