# Zero-Touch Development

Automatically develop, test, review, and deploy a feature with no manual intervention.

**This is the standard entry point for all implementation work.** It orchestrates the full SDLC by calling each phase command in sequence: develop → test → review → deploy.

## Variables

- `feature`: $1 - Linear issue ID (e.g., "ACA-123") or feature description

## Instructions

Execute the complete development pipeline automatically.

### If Linear Issue

If `feature` looks like a Linear issue ID (e.g., "LIN-123", "ACA-42"):
1. Fetch issue details using `mcp__linear-server__get_issue`
2. Store the issue ID for commenting throughout the pipeline
3. Use issue title and description as requirements

### Pipeline Phases

Execute each phase in sequence. If a phase fails, follow the retry/stop rules below.

#### 1. DEVELOP
- Create feature branch: `feat-{issue-id}-{slug}`
- **Read and follow `.claude/commands/develop.md`** using the issue ID
- This phase fetches requirements from Linear, posts a plan comment, then implements
- **Linear Comment**: Plan posted before coding, completion posted after

#### 2. TEST
- **Read and follow `.claude/commands/test.md`** using the issue ID
- Run tests with auto-fix (up to 3 retries)
- **If tests fail after 3 retries, STOP the pipeline.** Post a failure comment to Linear and report the failure. Do not proceed to REVIEW.
- **Linear Comment**: Post test results (pass/fail counts)

#### 3. REVIEW
- **Read and follow `.claude/commands/review.md`** using the issue ID
- Review implementation against Linear issue requirements
- If blockers are found, fix them and re-review (up to 2 times)
- **If blockers remain after 2 re-reviews, STOP the pipeline.** Post a failure comment to Linear and report the failure. Do not proceed to DEPLOY.
- **Linear Comment**: Post review summary with any issues found

#### 4. DEPLOY
- Commit changes with conventional commit message
- Push branch to remote
- Create pull request
- Auto-approve the PR
- Auto-merge the PR (squash merge, delete branch)
- **Linear Comment**: Post final summary with branch name, PR link, and merge status

### Linear Comment Templates

Use `mcp__linear-server__create_comment` with these formats:

**TEST Results:**
```markdown
## Test Results

| Test | Status |
|------|--------|
| {test_name} | Pass / Fail |

{error details if any failures}
```

**REVIEW Summary:**
```markdown
## Review Complete

**Status:** {Approved / Changes Needed}

### Findings
{list any issues or confirm all requirements met}
```

**DEPLOY Complete:**
```markdown
## Deployed & Merged

**Branch:** `{branch_name}`
**Commit:** `{commit_hash}`
**PR:** {github_pr_link}
**Status:** Merged / Pending review

{merge_status_details}
```

**Pipeline Failure:**
```markdown
## Pipeline Stopped

**Phase:** {TEST / REVIEW}
**Reason:** {description of failure}
**Retries:** {n} of {max}

{error details}
```

### On Completion

1. Update Linear issue status to "Done" using `mcp__linear-server__update_issue`
2. Report summary:

```
BRANCH: {branch_name}
STATUS: deployed
REMOTE: pushed
PR: {pr_url}
MERGED: yes/no
LINEAR: {issue_id} -> Done (with {n} comments)
```

The feature has been deployed and merged to main.
