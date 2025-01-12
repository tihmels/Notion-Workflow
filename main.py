import argparse
import sys
from client import create_new_page
from utils import load_configuration, validate_database, validate_template, convert_to_uuid


def main():
    try:
        parser = argparse.ArgumentParser(description="Create a new page in a Notion database.")
        parser.add_argument("--db", required=True, help="The label of the database to use.")
        parser.add_argument("--title", required=True, help="The title of the new page.")
        parser.add_argument("--template", help="The label of the template to use (optional).")
        parser.add_argument("--open", action="store_true", help="Open the created page after creation.")
        args = parser.parse_args()

        config = load_configuration()
        db_config = validate_database(args.db, config)

        template_id = None
        if args.template:
            template_id = validate_template(args.template, db_config)

        create_new_page(db_config, args.title, template_id=convert_to_uuid(template_id) if template_id else None, open_page=args.open)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()