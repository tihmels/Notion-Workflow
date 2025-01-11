import argparse
import sys
from client import create_new_page
from utils import load_configuration, validate_database

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