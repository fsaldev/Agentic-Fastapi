#!/usr/bin/env python3
"""
ADW CLI - AI Developer Workflow Command Line Interface

Usage:
    uv run .claude/adw/cli.py run <feature>      # ZERO-TOUCH: Develop, test, review, push
    uv run .claude/adw/cli.py project <desc>     # INTERACTIVE: Plan project, create issues, then run
    uv run .claude/adw/cli.py develop <id>       # Develop from workflow ID
    uv run .claude/adw/cli.py test <id>          # Run tests for workflow
    uv run .claude/adw/cli.py review <id>        # Review implementation
    uv run .claude/adw/cli.py list               # List all workflows
    uv run .claude/adw/cli.py status <id>        # Show workflow status

Zero-touch example:
    uv run .claude/adw/cli.py run "Add dark mode toggle to settings page"

Interactive project planning:
    uv run .claude/adw/cli.py project "Build a job posting application"
"""

import argparse
import sys
from pathlib import Path

# Add adw directory to path for imports when running directly
adw_dir = Path(__file__).parent
if str(adw_dir) not in sys.path:
    sys.path.insert(0, str(adw_dir))

from state import WorkflowState, list_workflows, find_workflow_by_issue
from logger import create_logger, log_section
from linear import is_linear_issue_id, create_issue_from_text, create_issue_placeholder


def cmd_develop(args: argparse.Namespace) -> int:
    """Execute develop workflow."""
    from workflows.develop import run_develop

    workflow_id = args.workflow_id

    # Load workflow state
    state = WorkflowState.load(workflow_id)
    if not state:
        print(f"Error: Workflow not found: {workflow_id}")
        return 1

    return run_develop(state)


def cmd_test(args: argparse.Namespace) -> int:
    """Execute test workflow."""
    from workflows.test import run_test

    workflow_id = args.workflow_id

    # Load workflow state
    state = WorkflowState.load(workflow_id)
    if not state:
        print(f"Error: Workflow not found: {workflow_id}")
        return 1

    return run_test(state)


def cmd_review(args: argparse.Namespace) -> int:
    """Execute review workflow."""
    from workflows.review import run_review

    workflow_id = args.workflow_id

    # Load workflow state
    state = WorkflowState.load(workflow_id)
    if not state:
        print(f"Error: Workflow not found: {workflow_id}")
        return 1

    return run_review(state)


def cmd_run(args: argparse.Namespace) -> int:
    """Execute zero-touch full pipeline (develop -> test -> review -> push).

    This is the simplest way to use ADW - just provide a feature description
    and everything happens automatically.
    """
    from workflows.full import run_full

    feature = args.feature
    logger = create_logger("init", "cli")

    print("\n" + "=" * 60)
    print("  ADW ZERO-TOUCH MODE")
    print("=" * 60)
    print(f"\nFeature: {feature}")
    print("\nThis will automatically:")
    print("  1. Develop the feature")
    print("  2. Run tests (with auto-fix)")
    print("  3. Review the implementation")
    print("  4. Push to remote")
    print("\n" + "=" * 60 + "\n")

    # Determine if input is a Linear issue ID or text
    if is_linear_issue_id(feature):
        logger.info(f"Linear issue detected: {feature}")
        logger.info("Issue details will be fetched via Linear MCP during development")
        issue = create_issue_placeholder(feature, logger)
    else:
        logger.info("Creating manual issue from text input")
        issue = create_issue_from_text(feature, logger)

    return run_full(issue, auto_push=True)


def cmd_project(args: argparse.Namespace) -> int:
    """Execute interactive project planning.

    This starts a conversation to:
    1. Break down a project into features
    2. Create Linear issues for each feature
    3. Optionally run the full pipeline for all issues
    """
    from workflows.project import run_project

    description = args.description
    auto_run = args.auto_run

    print("\n" + "=" * 60)
    print("  ADW INTERACTIVE PROJECT PLANNING")
    print("=" * 60)
    print(f"\nProject: {description}")
    print("\nThis interactive session will help you:")
    print("  1. Break down your project into features")
    print("  2. Define acceptance criteria")
    print("  3. Create Linear issues")
    if auto_run:
        print("  4. Automatically run pipeline for all issues")
    else:
        print("  4. (Manual mode - issues created but not run)")
    print("\n" + "=" * 60 + "\n")

    return run_project(description, auto_run=auto_run)


def cmd_list(args: argparse.Namespace) -> int:
    """List all workflows."""
    workflows = list_workflows()

    if not workflows:
        print("No workflows found.")
        return 0

    print(f"\n{'ID':<10} {'Phase':<12} {'Issue':<15} {'Title':<40} {'Updated':<20}")
    print("-" * 100)

    for w in workflows:
        issue_id = w.issue_id or "manual"
        title = (w.issue_title or "")[:38]
        updated = w.updated_at[:19] if w.updated_at else ""
        print(f"{w.workflow_id:<10} {w.phase:<12} {issue_id:<15} {title:<40} {updated:<20}")

    print(f"\nTotal: {len(workflows)} workflow(s)")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Show workflow status."""
    workflow_id = args.workflow_id

    state = WorkflowState.load(workflow_id)
    if not state:
        print(f"Error: Workflow not found: {workflow_id}")
        return 1

    print(f"\n{'='*60}")
    print(f"  Workflow: {state.workflow_id}")
    print(f"{'='*60}")
    print(f"  Issue ID:     {state.issue_id or 'manual'}")
    print(f"  Issue Title:  {state.issue_title or 'N/A'}")
    print(f"  Issue Type:   {state.issue_type or 'N/A'}")
    print(f"  Branch:       {state.branch_name or 'Not created'}")
    print(f"  Phase:        {state.phase}")
    print(f"  Created:      {state.created_at}")
    print(f"  Updated:      {state.updated_at}")
    print(f"  Completed:    {', '.join(state.phases_completed) or 'None'}")

    if state.error:
        print(f"  Error:        {state.error}")

    print(f"{'='*60}\n")

    return 0


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ADW - AI Developer Workflow CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # run command (zero-touch)
    run_parser = subparsers.add_parser("run", help="ZERO-TOUCH: Develop, test, review, and push")
    run_parser.add_argument("feature", help="Feature description or Linear issue ID")
    run_parser.set_defaults(func=cmd_run)

    # project command (interactive planning)
    project_parser = subparsers.add_parser("project", help="INTERACTIVE: Plan project, create Linear issues")
    project_parser.add_argument("description", help="Project description or goal")
    project_parser.add_argument(
        "--auto-run", "-a",
        action="store_true",
        default=False,
        help="Automatically run pipeline for all created issues"
    )
    project_parser.set_defaults(func=cmd_project)

    # develop command
    develop_parser = subparsers.add_parser("develop", help="Implement a feature")
    develop_parser.add_argument("workflow_id", help="Workflow ID to develop")
    develop_parser.set_defaults(func=cmd_develop)

    # test command
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument("workflow_id", help="Workflow ID to test")
    test_parser.set_defaults(func=cmd_test)

    # review command
    review_parser = subparsers.add_parser("review", help="Review implementation")
    review_parser.add_argument("workflow_id", help="Workflow ID to review")
    review_parser.set_defaults(func=cmd_review)

    # list command
    list_parser = subparsers.add_parser("list", help="List all workflows")
    list_parser.set_defaults(func=cmd_list)

    # status command
    status_parser = subparsers.add_parser("status", help="Show workflow status")
    status_parser.add_argument("workflow_id", help="Workflow ID")
    status_parser.set_defaults(func=cmd_status)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
