import os
import webbrowser
from notion_client import Client
from utils import convert_to_uuid, get_title_property_name, get_template_children

TOKEN = os.getenv("NOTION_TOKEN")
notion = Client(auth=TOKEN)


def get_database_schema(database_id):
    """Fetch the schema of the target database."""
    try:
        response = notion.databases.retrieve(database_id=database_id)
        return response.get("properties", {})
    except Exception as e:
        raise ValueError(f"Failed to retrieve the database schema: {e}")


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
    title_property_name = get_title_property_name(database_id, notion)

    # Fetch template properties
    template_properties = {}
    if template_page_id:
        try:
            template_page = notion.pages.retrieve(page_id=template_page_id)
            template_properties = template_page.get("properties", {})
        except Exception as e:
            print(f"Failed to fetch template properties: {e}")

    # Map and filter properties to match the database schema
    mapped_properties = {
        title_property_name: {
            "title": [{"text": {"content": title}}]
        }
    }

    # Fetch template children if provided
    children = get_template_children(template_page_id, notion) if template_page_id else []

    try:
        # Create the page
        response = notion.pages.create(
            parent={"database_id": database_id},
            properties=mapped_properties,
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