import os
import webbrowser
from notion_client import Client
import logging
from utils import (
    convert_to_uuid,
    get_title_property_name,
    get_template_children,
    get_database_schema,
    filter_supported_properties,
)

TOKEN = os.getenv("NOTION_TOKEN")
notion = Client(auth=TOKEN, log_level=logging.DEBUG)


def create_new_page(db_config, title, template_id=None, open_page=False):
    """Create a new page in the specified Notion database."""
    database_id = convert_to_uuid(db_config["id"])

    # Fetch template properties and children if template ID is provided
    template_properties = {}
    children = []
    if template_id:
        try:
            template_page = notion.pages.retrieve(page_id=template_id)
            template_properties = template_page.get("properties", {})
            children = get_template_children(template_id, notion)
        except Exception as e:
            logging.error(f"Failed to fetch template properties or children: {e}")

    # Dynamically fetch the title property name
    title_property_name = get_title_property_name(database_id, notion)

    # Fetch the database schema to validate properties
    try:
        schema = get_database_schema(database_id, notion)
        # Filter unsupported and computed properties
        template_properties = filter_supported_properties(template_properties, schema)
    except Exception as e:
        logging.error(f"Failed to fetch schema or filter properties: {e}")
        return

    # Map and filter properties to match the database schema
    mapped_properties = {
        title_property_name: {
            "title": [{"text": {"content": title}}]
        }
    }

    # Add additional properties from the template if applicable
    for key, value in template_properties.items():
        if key not in mapped_properties:  # Avoid overriding the title
            mapped_properties[key] = value

    try:
        # Create the page
        response = notion.pages.create(
            parent={"database_id": database_id},
            properties=mapped_properties,
            children=children,
        )
        print(f"Page created successfully: {response['url']}")

        # Open the page in the Notion app or browser if requested
        if open_page:
            notion_url = response["url"]
            notion_app_url = notion_url.replace("https://", "notion://")
            webbrowser.open(notion_app_url, new=0, autoraise=True)

    except Exception as e:
        logging.error(f"Failed to create the page: {e}")