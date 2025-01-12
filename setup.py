import os
import json
import sys
from notion_client import Client

CONFIG_FILE = "config.json"

# Initialize Notion Client
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


def generate_config(databases):
    """Generate the configuration file for databases."""
    config = {"databases": []}
    for db in databases:
        db_id = db.get("id")
        title = db.get("title", [])
        label = title[0].get("plain_text", "Untitled") if title else "Untitled"

        config["databases"].append({
            "label": label,
            "id": db_id,
            "templates": []  
        })
    return config

def write_config(config):
    """Write the configuration to the config.json file."""
    try:
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)
        print(f"Configuration written to {CONFIG_FILE}")
    except Exception as e:
        print(f"Error writing configuration file: {e}")
        sys.exit(1)


def main():
    print("Fetching shared databases...")
    databases = fetch_shared_databases()
    if not databases:
        print("No shared databases found.")
        sys.exit(0)

    print(f"Found {len(databases)} databases. Generating configuration...")
    config = generate_config(databases)
    write_config(config)


if __name__ == "__main__":
    main()