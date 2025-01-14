from client import create_new_page
from utils import convert_to_uuid
import argparse
import sys

def handle_page_command(page_id, title, open_page):
    db_config = {"id": page_id}
    create_new_page(
        db_config=db_config,
        title=title,
        template_id=None,
        open_page=open_page,
    )

def handle_template_command(template_id, title, open_page):
    template_uuid = convert_to_uuid(template_id)
    create_new_page(
        db_config={"id": None},
        title=title,
        template_id=template_uuid,
        open_page=open_page,
    )

def main():
    try:
        parser = argparse.ArgumentParser(description="Notion Page and Template Workflow")
        parser.add_argument("command", choices=["page", "template"], help="The command to execute (page or template).")
        parser.add_argument("--id", required=True, help="The ID of the database or template to use.")
        parser.add_argument("--title", help="The title of the new page (optional).")
        parser.add_argument("--open", action="store_true", help="Open the created page after creation.")
        args = parser.parse_args()

        if args.command == "page":
            handle_page_command(args.id, args.title or 'Untitled', args.open)

        elif args.command == "template":
            handle_template_command(args.id, args.title or 'Untitled', args.open)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()