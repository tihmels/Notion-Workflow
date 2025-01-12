import json
import os
import re
import logging

DATABASES_FILE = "databases.json"
TEMPLATES_FILE = "templates.json"
UNSUPPORTED_PROPERTIES = {"rollup", "created_by", "created_time", "last_edited_by", "last_edited_time"}


def filter_supported_properties(properties, schema):
    """Filter out unsupported and computed properties."""
    return {
        name: value
        for name, value in properties.items()
        if schema.get(name, {}).get("type") not in UNSUPPORTED_PROPERTIES
    }


def load_configuration():
    """Load configuration files."""
    if not os.path.exists(DATABASES_FILE) or not os.path.exists(TEMPLATES_FILE):
        raise FileNotFoundError(f"Configuration files '{DATABASES_FILE}' or '{TEMPLATES_FILE}' not found.")
    try:
        with open(DATABASES_FILE, "r") as db_file:
            databases = json.load(db_file)
        with open(TEMPLATES_FILE, "r") as tmpl_file:
            templates = json.load(tmpl_file)

        return {"databases": databases["databases"], "templates": templates["templates"]}
    except json.JSONDecodeError as e:
        raise ValueError(f"Error loading configuration: Invalid JSON format. {e}")


def validate_database_or_template(label, config, is_template=False):
    """Validate and retrieve database or template."""
    try:
        if is_template:
            for template in config["templates"]:
                if template["label"].lower() == label.lower():
                    return {"template_id": template["id"]}
            raise ValueError(f"No template found with label '{label}'.")
        else:
            for db in config["databases"]:
                if db["label"].lower() == label.lower():
                    return db
            raise ValueError(f"No database found with label '{label}'.")
    except KeyError as e:
        raise ValueError(f"Configuration is missing expected keys: {e}")


def convert_to_uuid(page_id):
    """Convert page ID to UUID format."""
    if re.match(r"^[a-f0-9]{32}$", page_id):
        return f"{page_id[:8]}-{page_id[8:12]}-{page_id[12:16]}-{page_id[16:20]}-{page_id[20:]}"
    elif re.match(r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$", page_id):
        return page_id
    raise ValueError(f"Invalid page ID format: {page_id}")


def get_template_children(template_id, notion_client):
    """Retrieve children (blocks) of a template page."""
    try:
        response = notion_client.blocks.children.list(block_id=template_id)
        children = response.get("results", [])
        # Filter out unsupported block types
        supported_children = [
            block for block in children if block["type"] not in {"child_page"}
        ]
        return supported_children
    except Exception as e:
        raise ValueError(f"Error retrieving template children: {e}")


def get_database_schema(database_id, notion_client):
    """Retrieve the schema of a Notion database."""
    try:
        response = notion_client.databases.retrieve(database_id=database_id)
        return response.get("properties", {})
    except Exception as e:
        raise ValueError(f"Error retrieving database schema: {e}")