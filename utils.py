import os
import re
import logging
from notion_client import Client

UNSUPPORTED_PROPERTIES = {
    "rollup",
    "created_by",
    "created_time",
    "last_edited_by",
    "last_edited_time",
}


def filter_supported_properties(properties, schema):
    """
    Filter out unsupported or computed properties so they can be merged
    into a new page. Properties with types in UNSUPPORTED_PROPERTIES
    are excluded.
    """
    filtered = {}
    for name, value in properties.items():
        prop_type = schema.get(name, {}).get("type")
        if prop_type not in UNSUPPORTED_PROPERTIES:
            filtered[name] = value
    return filtered


def convert_to_uuid(page_id):
    """
    Convert a 32-character hex string into a Notion-friendly UUID format
    if necessary. If the ID is already in UUID format, return as is.
    Raises ValueError if the format is invalid.

    Examples:
      - "c8fab04474104b93b9d42c7c4c9fd982" -> "c8fab044-7410-4b93-b9d4-2c7c4c9fd982"
    """
    # 32 hex chars
    if re.match(r"^[a-f0-9]{32}$", page_id):
        return (
            f"{page_id[:8]}-{page_id[8:12]}-{page_id[12:16]}-"
            f"{page_id[16:20]}-{page_id[20:]}"
        )
    # Already in UUID format
    elif re.match(r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$", page_id):
        return page_id

    raise ValueError(f"Invalid page ID format: {page_id}")


def get_template_children(template_id, notion_client):
    """
    Retrieve the child blocks of a template page from Notion. 
    Filters out unsupported block types (like 'child_page') 
    to avoid errors when duplicating content.

    :param template_id: The UUID of the template page.
    :param notion_client: An instantiated notion_client.Client.
    :return: A list of supported block objects.
    """
    try:
        response = notion_client.blocks.children.list(block_id=template_id)
        children = response.get("results", [])
        # Filter out blocks of unsupported types
        supported_children = [
            block for block in children if block["type"] not in {"child_page"}
        ]
        return supported_children
    except Exception as e:
        raise ValueError(f"Error retrieving template children: {e}") from e


def get_database_schema(database_id, notion_client):
    """
    Retrieve the properties (schema) of a Notion database. 
    This schema can be used to determine what properties
    can be copied over from a template or how a title property
    should be set.

    :param database_id: The UUID of the Notion database.
    :param notion_client: An instantiated notion_client.Client.
    :return: A dictionary of database properties.
    """
    try:
        response = notion_client.databases.retrieve(database_id=database_id)
        return response.get("properties", {})
    except Exception as e:
        raise ValueError(f"Error retrieving database schema: {e}") from e