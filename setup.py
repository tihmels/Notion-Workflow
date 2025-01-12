import os
import json
import sys
from notion_client import Client

DATABASES_FILE = "databases.json"
TEMPLATES_FILE = "templates.json"

TOKEN = os.getenv("NOTION_TOKEN")
if not TOKEN:
    print("Error: NOTION_TOKEN environment variable is not set.")
    sys.exit(1)

notion = Client(auth=TOKEN)


def fetch_shared_databases():
    """Fetch all databases shared with the integration."""
    try:
        response = notion.search(
            query="",
            filter={"value": "database", "property": "object"},
            sort={"direction": "ascending", "timestamp": "last_edited_time"}
        )
        return response.get("results", [])
    except Exception as e:
        print(f"Error fetching databases: {e}")
        sys.exit(1)


def write_json(file_path, data):
    """Write JSON data to a file."""
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Configuration written to {file_path}")
    except Exception as e:
        print(f"Error writing configuration file: {e}")
        sys.exit(1)


def main():
    print("Fetching shared databases...")
    databases = fetch_shared_databases()
    if not databases:
        print("No shared databases found.")
        sys.exit(0)

    db_config = {"databases": [{"label": db.get("title", [{}])[0].get("plain_text", "Untitled"), "id": db["id"]} for db in databases]}
    write_json(DATABASES_FILE, db_config)

    # Ensure the templates.json file exists
    if not os.path.exists(TEMPLATES_FILE):
        write_json(TEMPLATES_FILE, {"templates": []})


if __name__ == "__main__":
    main()