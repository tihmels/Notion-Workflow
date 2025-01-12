import os
import webbrowser
import logging
from notion_client import Client
from utils import get_template_children, filter_supported_properties, get_database_schema

TOKEN = os.getenv("NOTION_TOKEN")
if not TOKEN:
    raise EnvironmentError("NOTION_TOKEN environment variable is not set.")
notion = Client(auth=TOKEN, log_level=logging.DEBUG)


from utils import convert_to_uuid

def create_new_page(db_config, title, template_id=None, open_page=False):
    """Create a new page in the specified Notion database."""
    database_id = db_config.get("id")
    children = []
    properties = {}

    try:
        # Fetch the database schema and set properties for database pages
        if database_id:
            schema = get_database_schema(database_id, notion)
            title_property = None
            for key, value in schema.items():
                if value.get("type") == "title":
                    title_property = key
                    break

            if not title_property:
                raise KeyError("The database does not have a title property.")

            # Set the title property
            properties[title_property] = {"title": [{"text": {"content": title}}]}

        # If a template is provided, fetch its children and properties
        if template_id:
            children = get_template_children(template_id, notion)
            template_page = notion.pages.retrieve(page_id=template_id)
            if database_id:
                properties.update(
                    filter_supported_properties(template_page["properties"], schema)
                )

        # Define the parent for the page creation
        parent = {"database_id": database_id} if database_id else {"type": "page_id", "page_id": template_id}

        # Create the new page
        response = notion.pages.create(
            parent=parent,
            properties=properties,
            children=children,
        )
        print(f"Page created successfully: {response['url']}")

        # Open the page if requested
        if open_page:
            notion_url = response["url"]
            notion_app_url = notion_url.replace("https://", "notion://")
            webbrowser.open(notion_app_url, new=0, autoraise=True)

    except Exception as e:
        logging.error(f"Failed to create the page: {e}")
        raise