"""
Full workflow - Runs complete pipeline.

This workflow orchestrates:
1. Develop (fetches requirements from Linear, plans, implements)
2. Test
3. Review
4. Deploy (commit + push + PR + merge)
"""

import sys
from pathlib import Path

# Add parent (adw) directory to path for imports
adw_dir = Path(__file__).parent.parent
if str(adw_dir) not in sys.path:
    sys.path.insert(0, str(adw_dir))

from state import WorkflowState
from logger import create_logger, log_section, log_success, log_error
from linear import LinearIssue
from git_ops import (
    create_branch, generate_branch_name, push_branch, get_diff_stat,
    get_changed_files, create_pr, generate_pr_body, review_pr, merge_pr,
)

from workflows.develop import run_develop
from workflows.test import run_test
from workflows.review import run_review


def run_full(issue: LinearIssue, auto_push: bool = True) -> int:
    """Run the full pipeline.

    Args:
        issue: Linear issue or manual issue
        auto_push: Whether to automatically push at the end (default True)

    Returns:
        Exit code (0 for success)
    """
    # Create workflow state
    state = WorkflowState.create(issue_id=issue.identifier)
    state.update(
        issue_title=issue.title,
        issue_description=issue.description,
        issue_type=issue.issue_type,
    )

    logger = create_logger(state.workflow_id, "full")

    # Create feature branch
    branch_name = generate_branch_name(
        issue_type=issue.issue_type,
        issue_id=issue.identifier,
        workflow_id=state.workflow_id,
        title=issue.title,
    )

    success, error = create_branch(branch_name, logger)
    if not success:
        log_error(logger, f"Failed to create branch: {error}")
        return 1

    state.update(branch_name=branch_name)
    state.save(logger)

    # Phase 1: Develop
    print("\n" + "=" * 60)
    print("  PHASE 1: DEVELOP")
    print("=" * 60 + "\n")

    # Reload state
    state = WorkflowState.load(state.workflow_id)
    if not state:
        print("Error: Could not reload workflow state")
        return 1

    result = run_develop(state)
    if result != 0:
        print(f"\nPipeline failed at DEVELOP phase")
        return result

    # Phase 2: Test
    print("\n" + "=" * 60)
    print("  PHASE 2: TEST")
    print("=" * 60 + "\n")

    # Reload state
    state = WorkflowState.load(state.workflow_id)
    if not state:
        print("Error: Could not reload workflow state")
        return 1

    result = run_test(state)
    if result != 0:
        print(f"\nPipeline failed at TEST phase")
        return result

    # Phase 3: Review
    print("\n" + "=" * 60)
    print("  PHASE 3: REVIEW")
    print("=" * 60 + "\n")

    # Reload state
    state = WorkflowState.load(state.workflow_id)
    if not state:
        print("Error: Could not reload workflow state")
        return 1

    result = run_review(state)
    if result != 0:
        print(f"\nPipeline failed at REVIEW phase")
        return result

    # Phase 4: Deploy (Push + PR + Merge)
    print("\n" + "=" * 60)
    print("  PHASE 4: DEPLOY")
    print("=" * 60 + "\n")

    # Reload state
    state = WorkflowState.load(state.workflow_id)
    if not state:
        print("Error: Could not reload workflow state")
        return 1

    if auto_push and state.branch_name:
        logger = create_logger(state.workflow_id, "deploy")
        logger.info(f"Pushing branch {state.branch_name} to remote...")

        success, message = push_branch(state.branch_name, logger)
        if not success:
            logger.error(f"Failed to push: {message}")
            print(f"\nPipeline failed at DEPLOY phase: {message}")
            return 1

        logger.info(f"Successfully pushed: {message}")

        # Show diff stats
        diff_stat = get_diff_stat("origin/main", logger)
        if diff_stat:
            print("\nChanges pushed:")
            print(diff_stat)

        # Create PR
        logger.info("Creating pull request...")
        changed_files = get_changed_files("origin/main", logger)

        pr_title = f"feat({state.issue_id}): {state.issue_title}"
        pr_body = generate_pr_body(
            issue_id=state.issue_id,
            issue_title=state.issue_title,
            summary=state.review_results.get("summary", f"Implements {state.issue_title}") if state.review_results else f"Implements {state.issue_title}",
            changes=changed_files,
            linear_url=f"https://linear.app/acadexis/issue/{state.issue_id}" if state.issue_id else None,
        )

        pr_success, pr_result = create_pr(pr_title, pr_body, logger=logger)
        if pr_success:
            logger.info(f"PR created: {pr_result}")
            state.pr_url = pr_result

            # Auto-approve the PR
            logger.info("Auto-approving PR...")
            review_success, review_msg = review_pr(pr_result, approve=True, logger=logger)
            if review_success:
                logger.info(f"PR approved: {review_msg}")
            else:
                logger.warning(f"Could not auto-approve PR: {review_msg}")

            # Auto-merge the PR
            logger.info("Auto-merging PR...")
            merge_success, merge_msg = merge_pr(pr_result, method="squash", delete_branch=True, logger=logger)
            if merge_success:
                logger.info(f"PR merged: {merge_msg}")
                state.merged = True
            else:
                logger.warning(f"Could not auto-merge PR: {merge_msg}")
                print(f"\nWarning: PR created but not merged: {merge_msg}")
        else:
            logger.warning(f"Could not create PR: {pr_result}")
            print(f"\nWarning: Could not create PR automatically: {pr_result}")

        # Update state
        state.phase = "deployed"
        state.phases_completed.append("deploy")
        state.save()
    else:
        print("Skipping push (auto_push=False or no branch)")

    # Success!
    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE")
    print("=" * 60)
    print(f"\nWorkflow ID: {state.workflow_id}")
    print(f"Branch: {state.branch_name}")
    print(f"\nAll phases completed successfully!")

    if auto_push and state.branch_name:
        print(f"\nBranch '{state.branch_name}' has been pushed to remote.")
        if hasattr(state, 'pr_url') and state.pr_url:
            print(f"Pull Request: {state.pr_url}")
            if hasattr(state, 'merged') and state.merged:
                print("PR has been auto-merged!")
            else:
                print("PR is ready for review.")
        else:
            print("You can now create a Pull Request.")

    return 0
