"""
Create Linear issues for the Rent a Car Backend API project.

Usage:
    python scripts/create_linear_issues.py

Requires:
    - LINEAR_API_KEY environment variable
    - requests library (pip install requests)
"""

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

def get_teams():
    """Get all teams to find the team ID."""
    query = """
    query {
        teams {
            nodes {
                id
                name
                key
            }
        }
    }
    """
    return graphql_request(query)["teams"]["nodes"]

def get_projects(team_id: str):
    """Get projects for a team."""
    query = """
    query($teamId: String!) {
        team(id: $teamId) {
            projects {
                nodes {
                    id
                    name
                }
            }
        }
    }
    """
    return graphql_request(query, {"teamId": team_id})["team"]["projects"]["nodes"]

def create_project(team_id: str, name: str, description: str):
    """Create a new project."""
    query = """
    mutation($input: ProjectCreateInput!) {
        projectCreate(input: $input) {
            success
            project {
                id
                name
                url
            }
        }
    }
    """
    variables = {
        "input": {
            "name": name,
            "teamIds": [team_id],
            "description": description
        }
    }
    result = graphql_request(query, variables)
    return result["projectCreate"]["project"]

def create_issue(team_id: str, project_id: str, title: str, description: str, priority: int):
    """Create an issue in Linear."""
    query = """
    mutation($input: IssueCreateInput!) {
        issueCreate(input: $input) {
            success
            issue {
                id
                identifier
                title
                url
            }
        }
    }
    """
    variables = {
        "input": {
            "teamId": team_id,
            "projectId": project_id,
            "title": title,
            "description": description,
            "priority": priority
        }
    }
    result = graphql_request(query, variables)
    return result["issueCreate"]["issue"]

# Feature definitions
FEATURES = [
    {
        "title": "Project setup & database",
        "priority": 1,
        "description": """## Description
Initialize the FastAPI project with the layered architecture, configure async SQLAlchemy with SQLite, and create all database models.

## Acceptance Criteria
- [ ] FastAPI application starts successfully
- [ ] Database tables are created on startup
- [ ] Project follows the defined folder structure
- [ ] Configuration management is in place

## Technical Details
- FastAPI with Python 3.11+
- Async SQLAlchemy 2.0 with SQLite
- Pydantic v2 for validation
- Layered architecture: Routes → Services → Repositories

## Dependencies
None - this is the foundation."""
    },
    {
        "title": "Car CRUD operations",
        "priority": 1,
        "description": """## Description
Implement full Create, Read, Update, Delete operations for cars with filtering capabilities.

## Acceptance Criteria
- [ ] POST `/api/v1/cars` - Create a new car
- [ ] GET `/api/v1/cars` - List all cars with optional filters (status, category)
- [ ] GET `/api/v1/cars/{id}` - Get car by ID
- [ ] PUT `/api/v1/cars/{id}` - Update car details
- [ ] DELETE `/api/v1/cars/{id}` - Delete a car
- [ ] Validation: License plate must be unique
- [ ] Proper error responses (404, 400, etc.)

## Car Model Fields
- id (UUID)
- make, model, year
- license_plate (unique)
- daily_rate (decimal)
- category (enum: economy, standard, luxury, suv)
- status (enum: available, rented, maintenance)
- created_at

## Dependencies
- Project setup & database"""
    },
    {
        "title": "Customer CRUD operations",
        "priority": 1,
        "description": """## Description
Implement full Create, Read, Update, Delete operations for customers.

## Acceptance Criteria
- [ ] POST `/api/v1/customers` - Register a new customer
- [ ] GET `/api/v1/customers` - List all customers
- [ ] GET `/api/v1/customers/{id}` - Get customer by ID
- [ ] PUT `/api/v1/customers/{id}` - Update customer details
- [ ] DELETE `/api/v1/customers/{id}` - Delete a customer
- [ ] Validation: Email must be unique
- [ ] Proper error responses (404, 400, etc.)

## Customer Model Fields
- id (UUID)
- first_name, last_name
- email (unique)
- phone
- driver_license
- created_at

## Dependencies
- Project setup & database"""
    },
    {
        "title": "Create booking (reservation)",
        "priority": 1,
        "description": """## Description
Allow customers to create a booking/reservation for a car within a specified date range.

## Acceptance Criteria
- [ ] POST `/api/v1/bookings` - Create a new booking
- [ ] Validate car exists and is not in maintenance
- [ ] Validate customer exists
- [ ] Validate date range (start_date < end_date, start_date >= today)
- [ ] Check car availability for the requested dates
- [ ] Calculate total_cost = daily_rate × number of days
- [ ] Set booking status to "reserved"
- [ ] Prevent double-booking (same car, overlapping dates)

## Booking Model Fields
- id (UUID)
- car_id (FK)
- customer_id (FK)
- start_date, end_date
- actual_return_date (nullable)
- total_cost (decimal)
- status (enum: reserved, active, completed, cancelled)
- created_at

## Dependencies
- Car CRUD operations
- Customer CRUD operations"""
    },
    {
        "title": "Car availability check",
        "priority": 1,
        "description": """## Description
Check if a specific car is available for a given date range.

## Acceptance Criteria
- [ ] GET `/api/v1/cars/{id}/availability?start_date=X&end_date=Y`
- [ ] Returns availability status (true/false)
- [ ] If unavailable, returns conflicting booking dates
- [ ] Considers bookings with status "reserved" or "active"
- [ ] Does not consider "completed" or "cancelled" bookings

## Dependencies
- Car CRUD operations
- Create booking (reservation)"""
    },
    {
        "title": "Pickup car (start rental)",
        "priority": 1,
        "description": """## Description
Transition a booking from reserved to active when the customer picks up the car.

## Acceptance Criteria
- [ ] POST `/api/v1/bookings/{id}/pickup`
- [ ] Validate booking exists and status is "reserved"
- [ ] Update booking status to "active"
- [ ] Update car status to "rented"
- [ ] Return updated booking details

## Dependencies
- Create booking (reservation)"""
    },
    {
        "title": "Return car (complete rental)",
        "priority": 1,
        "description": """## Description
Complete a rental when the customer returns the car.

## Acceptance Criteria
- [ ] POST `/api/v1/bookings/{id}/return`
- [ ] Validate booking exists and status is "active"
- [ ] Set actual_return_date to current date
- [ ] Update booking status to "completed"
- [ ] Update car status to "available"
- [ ] Return updated booking details with final cost

## Dependencies
- Pickup car (start rental)"""
    }
]

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Create Linear issues for Rent a Car Backend API")
    parser.add_argument("--create-project", action="store_true", help="Create a new project")
    parser.add_argument("--project", type=str, help="Use existing project by name")
    parser.add_argument("--team", type=str, help="Team name to use")
    args = parser.parse_args()

    print("=" * 60)
    print("Linear Issue Creator - Rent a Car Backend API")
    print("=" * 60)

    # Get teams
    print("\nFetching teams...")
    teams = get_teams()

    if not teams:
        print("No teams found. Please create a team in Linear first.")
        sys.exit(1)

    print("\nAvailable teams:")
    for i, team in enumerate(teams, 1):
        print(f"  {i}. {team['name']} ({team['key']})")

    # Select team
    if len(teams) == 1:
        team = teams[0]
        print(f"\nUsing team: {team['name']}")
    elif args.team:
        team = next((t for t in teams if t['name'].lower() == args.team.lower()), None)
        if not team:
            print(f"Team '{args.team}' not found")
            sys.exit(1)
        print(f"\nUsing team: {team['name']}")
    else:
        print("\nError: Multiple teams found. Use --team to specify.")
        sys.exit(1)

    team_id = team["id"]

    # Check for existing projects or create new
    print("\nFetching projects...")
    projects = get_projects(team_id)

    if args.create_project:
        print("\nCreating project...")
        project = create_project(
            team_id,
            "Rent a Car Backend API",
            "RESTful backend API for managing a car rental business. Handles car inventory, customer records, and the full booking lifecycle."
        )
        print(f"Created project: {project['name']}")
        print(f"URL: {project['url']}")
    elif args.project:
        project = next((p for p in projects if p['name'].lower() == args.project.lower()), None)
        if not project:
            print(f"Project '{args.project}' not found. Available projects:")
            for p in projects:
                print(f"  - {p['name']}")
            sys.exit(1)
        print(f"\nUsing project: {project['name']}")
    else:
        print("\nAvailable projects:")
        for p in projects:
            print(f"  - {p['name']}")
        print("\nError: Use --create-project to create new, or --project 'Name' to use existing")
        sys.exit(1)

    project_id = project["id"]

    # Create issues
    print("\n" + "=" * 60)
    print("Creating issues...")
    print("=" * 60)

    created_issues = []
    for feature in FEATURES:
        print(f"\nCreating: {feature['title']}...")
        issue = create_issue(
            team_id=team_id,
            project_id=project_id,
            title=feature["title"],
            description=feature["description"],
            priority=feature["priority"]
        )
        created_issues.append(issue)
        print(f"  [OK] {issue['identifier']}: {issue['title']}")
        print(f"    {issue['url']}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nProject: {project.get('name', 'Rent a Car Backend API')}")
    print(f"Issues created: {len(created_issues)}")
    print("\nIssue IDs:")
    for issue in created_issues:
        print(f"  - {issue['identifier']}: {issue['title']}")

    print("\n[OK] Done! Issues are ready in Linear.")

if __name__ == "__main__":
    main()
