# Review

Review implementation against the Linear issue requirements.

Can be run standalone (`/review ACA-123`) or as part of the `/run` pipeline.

## Variables

- `issue_id`: $1 - Linear issue ID (e.g., "ACA-123")

## Instructions

1. **Check Context**
   - Run `git branch` to see current branch
   - Run `git diff origin/main --stat` to see all changes

2. **Read Requirements**
   - Use `mcp__linear-server__get_issue` to fetch the issue by `issue_id`
   - Use `mcp__linear-server__list_comments` to find the implementation plan comment
   - Understand what was supposed to be built from the issue description and plan

3. **Compare Implementation**
   - Review the code changes against requirements
   - Check if all plan steps were completed
   - Verify all listed files were modified appropriately

4. **Classify Issues**
   For each issue found, classify as:
   - `blocker`: Must fix before release - breaks functionality
   - `tech_debt`: Should fix later - not ideal but works
   - `skippable`: Minor - informational only

5. **Take Screenshots (if UI changes)**
   - Navigate to the application
   - Capture 1-5 screenshots of key functionality
   - Save screenshots to the working directory

6. **Post Linear Comment**
   Post a comment using `mcp__linear-server__create_comment`:

   ```markdown
   ## Review Complete

   **Status:** Approved / Changes Needed

   ### Acceptance Criteria
   - [x] {criteria 1}
   - [x] {criteria 2}
   - [ ] {criteria 3 - if not met}

   ### Findings
   {List any issues found, or "All requirements met. Implementation matches plan."}

   ### Issues
   | # | Severity | Description |
   |---|----------|-------------|
   | 1 | blocker/tech_debt/skippable | {description} |
   ```

## Output

Return ONLY valid JSON:

```json
{
  "success": true,
  "review_summary": "The feature was implemented correctly. All requirements from the issue are met.",
  "review_issues": [
    {
      "review_issue_number": 1,
      "issue_description": "Missing error handling for empty response",
      "issue_resolution": "Add try-catch block in fetchData function",
      "issue_severity": "tech_debt"
    }
  ],
  "screenshots": [
    "/absolute/path/to/screenshot1.png"
  ],
  "linear_comment_posted": true
}
```

## Success Criteria

- `success: true` if NO blockers found
- `success: false` if ANY blockers found
- Can have tech_debt/skippable issues and still pass

## Rules

- Be thorough but practical
- Focus on functionality, not style preferences
- Only flag real issues, not nitpicks
- Post Linear comment before returning JSON (only if issue_id provided)
- Output ONLY the JSON, no other text
