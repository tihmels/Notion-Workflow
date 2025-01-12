from client import create_new_page
from utils import load_configuration, validate_database_or_template, convert_to_uuid


def main():
    try:
        import argparse
        parser = argparse.ArgumentParser(description="Notion Page and Template Workflow")
        parser.add_argument("command", choices=["page", "template"], help="The command to execute (page or template).")
        parser.add_argument("--label", required=True, help="The label of the database or template to use.")
        parser.add_argument("--title", help="The title of the new page (optional).")
        parser.add_argument("--open", action="store_true", help="Open the created page after creation.")

        args = parser.parse_args()

        # Load the configuration
        config = load_configuration()

        if args.command == "page":
            # Fetch the database configuration
            db_config = validate_database_or_template(args.label, config, is_template=False)
            if not db_config or not db_config.get("id"):
                raise ValueError(f"Invalid database configuration for label: {args.label}")
            create_new_page(
                db_config=db_config,
                title=args.title or "Untitled",
                template_id=None,
                open_page=args.open,
            )
        elif args.command == "template":
            # Fetch the template configuration
            template_config = validate_database_or_template(args.label, config, is_template=True)
            if not template_config or not template_config.get("template_id"):
                raise ValueError(f"Invalid template configuration for label: {args.label}")
            create_new_page(
                db_config={"id": None},  # Templates are independent of databases
                title=args.title or "Untitled",
                template_id=convert_to_uuid(template_config["template_id"]),
                open_page=args.open,
            )

    except Exception as e:
        import sys
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()