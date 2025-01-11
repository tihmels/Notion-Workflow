import argparse
import json
import os
import re
import sys
import logging
import webbrowser
from notion_client import Client

CONFIG_FILE = "config.json"

# Initialize Notion Client
TOKEN = os.getenv("NOTION_TOKEN")
notion = Client(auth=TOKEN, log_level=logging.DEBUG)


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


def get_database_schema(database_id):
    """Fetch the schema of the target database."""
    try:
        response = notion.databases.retrieve(database_id=database_id)
        return response.get("properties", {})
    except Exception as e:
        raise ValueError(f"Failed to retrieve the database schema: {e}")


def get_title_property_name(database_id):
    """Retrieve the name of the title property dynamically."""
    try:
        schema = get_database_schema(database_id)
        for property_name, property_details in schema.items():
            if property_details["type"] == "title":
                return property_name
        raise ValueError("No title property found in the database schema.")
    except Exception as e:
        raise ValueError(f"Failed to retrieve the title property: {e}")


def map_template_to_database_properties(template_properties, database_schema):
    """Map template properties to the database schema."""
    mapped_properties = {}
    for prop_name, prop_details in template_properties.items():
        if prop_name in database_schema:
            schema_type = database_schema[prop_name]["type"]
            if schema_type in prop_details:
                mapped_properties[prop_name] = {schema_type: prop_details[schema_type]}
    return mapped_properties


def filter_valid_properties(properties, schema):
    """Filter and validate properties to match the database schema."""
    valid_properties = {}
    for prop_name, prop_schema in schema.items():
        if prop_schema["type"] in ["last_edited_time", "created_time", "rollup", "formula"]:
            continue  # Skip computed properties

        if prop_name in properties:
            prop_value = properties[prop_name]
            if prop_schema["type"] in prop_value:
                valid_properties[prop_name] = prop_value
    return valid_properties


def get_template_children(template_page_id):
    """Fetch the content blocks (children) of the template page."""
    try:
        response = notion.blocks.children.list(block_id=template_page_id)
        return response.get("results", [])
    except Exception as e:
        raise ValueError(f"Failed to fetch template page children: {e}")


def create_new_page(db_config, title, open_page=False):
    """Create a new page in the specified Notion database."""
    database_id = convert_to_uuid(db_config["id"])
    template_page_id = db_config.get("template")

    # Convert template page ID if provided
    if template_page_id:
        template_page_id = convert_to_uuid(template_page_id)

    # Get the database schema
    database_schema = get_database_schema(database_id)

    # Dynamically fetch the title property name
    title_property_name = get_title_property_name(database_id)

    # Fetch template properties
    template_properties = {}
    if template_page_id:
        try:
            template_page = notion.pages.retrieve(page_id=template_page_id)
            template_properties = template_page.get("properties", {})
        except Exception as e:
            print(f"Failed to fetch template properties: {e}")

    # Map and filter properties to match the database schema
    mapped_properties = map_template_to_database_properties(template_properties, database_schema)
    valid_properties = filter_valid_properties(mapped_properties, database_schema)

    # Add the dynamically identified title property
    valid_properties[title_property_name] = {
        "title": [
            {
                "text": {
                    "content": title
                }
            }
        ]
    }

    # Fetch template children if provided
    children = get_template_children(template_page_id) if template_page_id else []

    try:
        # Debugging: Print properties and children
        print("Properties being sent to Notion API:", valid_properties)
        print("Children being sent to Notion API:", children)

        # Create the page
        response = notion.pages.create(
            parent={"database_id": database_id},
            properties=valid_properties,
            children=children
        )
        print(f"Page created successfully: {response['url']}")

        # Open the page in the Notion app or browser if requested
        if open_page:
            notion_url = response["url"]
            notion_app_url = notion_url.replace("https://", "notion://")
            print(f"Opening page: {notion_app_url}")
            webbrowser.open(notion_app_url, new=0, autoraise=True)

    except Exception as e:
        raise ValueError(f"Failed to create the page: {e}")


def main():
    try:
        # Parse command-line arguments
        parser = argparse.ArgumentParser(description="Create a new page in a Notion database.")
        parser.add_argument("--db", required=True, help="The label of the database to use.")
        parser.add_argument("--title", required=True, help="The title of the new page.")
        parser.add_argument("--open", action="store_true", help="Open the created page after creation.")
        args = parser.parse_args()

        # Load configuration
        config = load_configuration()

        # Validate database label
        db_config = validate_database(args.db, config)

        # Create the page
        create_new_page(db_config, args.title, open_page=args.open)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()