import json
import os
import re


CONFIG_FILE = "config.json"


def load_configuration():
    """Load and validate the JSON configuration file."""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Configuration file '{CONFIG_FILE}' not found.")

    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)

        if "databases" not in config or not isinstance(config["databases"], list):
            raise ValueError("Invalid configuration: No 'databases' array found.")

        return config
    except json.JSONDecodeError as e:
        raise ValueError(f"Error loading configuration: Invalid JSON format. {e}")


def validate_database(db_label, config):
    """Check if the given database label exists in the configuration."""
    for db in config["databases"]:
        if db["label"].lower() == db_label.lower():
            return db
    raise ValueError(f"No database found with label '{db_label}'.")


def convert_to_uuid(page_id):
    """Convert a page ID to UUID format if needed."""
    if re.match(r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$", page_id):
        return page_id  # Already in UUID format
    if re.match(r"^[a-f0-9]{32}$", page_id):
        return f"{page_id[:8]}-{page_id[8:12]}-{page_id[12:16]}-{page_id[16:20]}-{page_id[20:]}"
    raise ValueError(f"Invalid page ID format: '{page_id}'.")


def get_title_property_name(database_id, notion_client):
    """Retrieve the name of the title property dynamically."""
    try:
        schema = get_database_schema(database_id, notion_client)
        for property_name, property_details in schema.items():
            if property_details["type"] == "title":
                return property_name
        raise ValueError("No title property found in the database schema.")
    except Exception as e:
        raise ValueError(f"Failed to retrieve the title property: {e}")


def get_database_schema(database_id, notion_client):
    """Fetch the schema of the target database."""
    try:
        response = notion_client.databases.retrieve(database_id=database_id)
        return response.get("properties", {})
    except Exception as e:
        raise ValueError(f"Failed to retrieve the database schema: {e}")


def get_template_children(template_page_id, notion_client):
    """Fetch the content blocks (children) of the template page."""
    try:
        response = notion_client.blocks.children.list(block_id=template_page_id)
        return response.get("results", [])
    except Exception as e:
        raise ValueError(f"Failed to fetch template page children: {e}")