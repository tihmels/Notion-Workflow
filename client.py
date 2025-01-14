import os
import webbrowser
import logging
from notion_client import Client
from utils import get_template_children, filter_supported_properties, get_database_schema

TOKEN = os.getenv("NOTION_TOKEN")
if not TOKEN:
    raise EnvironmentError("NOTION_TOKEN environment variable is not set.")
notion = Client(auth=TOKEN, log_level=logging.DEBUG)

def create_new_page(db_config, title, template_id=None, open_page=False):
    """Create a new page in the specified Notion database or from a template."""
    database_id = db_config.get("id")
    children = []
    properties = {}

    try:
        # 1) If a template is provided, fetch children & properties
        if template_id:
            template_page = notion.pages.retrieve(page_id=template_id)
            template_parent = template_page.get("parent", {})

            # Derive the database_id from the template’s parent
            if template_parent.get("type") == "database_id":
                database_id = template_parent.get("database_id")
            else:
                raise ValueError("Template is not associated with a database.")

            # Fetch the children from the template
            children = get_template_children(template_id, notion)

            # Optionally merge the template's existing properties
            if database_id:
                schema = get_database_schema(database_id, notion)
                properties.update(
                    filter_supported_properties(
                        template_page.get("properties", {}), schema
                    )
                )

        # 2) If creating within a database, set the page title property
        if database_id:
            schema = get_database_schema(database_id, notion)
            title_property = next(
                (key for key, value in schema.items() if value.get("type") == "title"),
                None
            )
            if not title_property:
                raise KeyError("The database does not have a title property.")
            properties[title_property] = {"title": [{"text": {"content": title}}]}

        # 3) Define the parent for the page creation
        if not database_id:
            raise ValueError("Cannot determine the parent database for the new page.")
        parent = {"database_id": database_id}

        # 4) Create the new page
        response = notion.pages.create(
            parent=parent,
            properties=properties,
            children=children,
        )
        print(f"Page created successfully: {response['url']}")

        # 5) Optionally open the page
        if open_page:
            notion_url = response["url"]
            notion_app_url = notion_url.replace("https://", "notion://")
            webbrowser.open(notion_app_url, new=0, autoraise=True)

    except Exception as e:
        logging.error(f"Failed to create the page: {e}")
        raise