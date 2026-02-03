"""Post a comment to a Linear issue."""

import os
import sys
import requests

LINEAR_API_URL = "https://api.linear.app/graphql"


def get_headers():
    api_key = os.environ.get("LINEAR_API_KEY")
    if not api_key:
        print("Error: LINEAR_API_KEY environment variable not set")
        sys.exit(1)
    return {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }


def graphql_request(query: str, variables: dict = None):
    response = requests.post(
        LINEAR_API_URL,
        headers=get_headers(),
        json={"query": query, "variables": variables or {}}
    )
    data = response.json()
    if "errors" in data:
        print(f"GraphQL Error: {data['errors']}")
        sys.exit(1)
    return data["data"]


def get_issue_by_identifier(identifier: str):
    """Get issue ID by its identifier (e.g., ACA-755)."""
    query = """
    query($identifier: String!) {
        issue(id: $identifier) {
            id
            identifier
            title
        }
    }
    """
    # Try with identifier directly
    try:
        result = graphql_request(query, {"identifier": identifier})
        return result["issue"]
    except:
        pass

    # Search by identifier
    query = """
    query($filter: IssueFilter) {
        issues(filter: $filter) {
            nodes {
                id
                identifier
                title
            }
        }
    }
    """
    team_key = identifier.split("-")[0]
    number = int(identifier.split("-")[1])
    result = graphql_request(query, {
        "filter": {
            "number": {"eq": number},
            "team": {"key": {"eq": team_key}}
        }
    })
    issues = result["issues"]["nodes"]
    if issues:
        return issues[0]
    return None


def post_comment(issue_id: str, body: str):
    """Post a comment on an issue."""
    query = """
    mutation($input: CommentCreateInput!) {
        commentCreate(input: $input) {
            success
            comment {
                id
                body
            }
        }
    }
    """
    variables = {
        "input": {
            "issueId": issue_id,
            "body": body
        }
    }
    result = graphql_request(query, variables)
    return result["commentCreate"]


def main():
    if len(sys.argv) < 3:
        print("Usage: python post_linear_comment.py <issue_identifier> <comment_file>")
        print("Example: python post_linear_comment.py ACA-755 comment.md")
        sys.exit(1)

    identifier = sys.argv[1]
    comment_file = sys.argv[2]

    # Read comment from file
    with open(comment_file, "r", encoding="utf-8") as f:
        comment_body = f.read()

    print(f"Finding issue {identifier}...")
    issue = get_issue_by_identifier(identifier)
    if not issue:
        print(f"Issue {identifier} not found")
        sys.exit(1)

    print(f"Found: {issue['identifier']} - {issue['title']}")
    print(f"Posting comment...")

    result = post_comment(issue["id"], comment_body)
    if result["success"]:
        print("Comment posted successfully!")
    else:
        print("Failed to post comment")
        sys.exit(1)


if __name__ == "__main__":
    main()
