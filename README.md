# Notion Page Creation Workflow for Alfred

This repository contains a Python-based Alfred workflow that interacts with the Notion API to create new pages in specified databases. It supports multiple templates for each database, allowing users to dynamically select and apply a specific template while creating pages.

---

## Features

- **Create Pages in Notion Databases**: Create new pages in configured Notion databases using Alfred.
- **Template Support**: Select from multiple preconfigured templates for a database.
- **Customizable Configuration**: Easily configure databases and templates using a JSON file.
- **Open in Notion**: Automatically open the newly created page in the Notion desktop app or browser.

---

## Setup Instructions

### Prerequisites

- **Python**: Ensure Python 3.7 or higher is installed.
- **Notion Integration Token**: Generate an integration token from the [Notion Developers](https://www.notion.so/my-integrations) page.
- **Alfred**: Install Alfred (with Powerpack) for running workflows.

---

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/notion-alfred-workflow.git
   cd notion-alfred-workflow

	2.	Set Up a Virtual Environment:

python3 -m venv venv
source venv/bin/activate


	3.	Install Dependencies:

pip install -r requirements.txt


	4.	Configure the Notion Token:
Set your Notion API token as an environment variable:

export NOTION_TOKEN="your-notion-token"


	5.	Fetch Databases:
Run the setup script to fetch your shared Notion databases and generate a config.json file:

python setup.py

The script will output the databases shared with the integration. Edit config.json to add templates if necessary.

	6.	Install the Alfred Workflow:
	•	Open the Alfred Preferences.
	•	Import the .alfredworkflow file in the repository.

Configuration

The config.json file stores database and template configurations. It includes the following structure:

{
    "databases": [
        {
            "label": "Clients",
            "id": "d361c895-965a-4506-a2a9-cf9f38b28409",
            "templates": [
                {
                    "label": "Client Onboarding",
                    "id": "template-id-1"
                },
                {
                    "label": "Client Follow-up",
                    "id": "template-id-2"
                }
            ]
        },
        {
            "label": "Projects",
            "id": "7f84a64e-70f7-4b75-90cd-2d253f5ead1f",
            "templates": []
        }
    ]
}

You can manually add template IDs under the templates array for each database.

Usage
	1.	Trigger the Workflow:
	•	Open Alfred and type notion.
	•	Select a database from the list.
	2.	Optional: Specify a Template:
	•	After selecting a database, choose a template (if templates are configured).
	3.	Page Creation:
	•	The workflow creates a new page in the selected database using the template.
	•	The page is automatically opened in the Notion app or browser.

Files in This Repository

Python Scripts
	•	main.py: Main script for creating pages.
	•	setup.py: Fetches shared Notion databases and generates the configuration file.
	•	client.py: Contains functions to interact with the Notion API.
	•	utils.py: Helper functions for configuration and schema handling.

Configuration
	•	config.json: Stores database and template configurations.

Alfred Workflow
	•	info.plist: Alfred workflow configuration file.
	•	icon.png: Icon for the Alfred workflow.

Limitations
	•	No API Support for Templates: Since Notion API does not support fetching templates directly, template IDs must be manually configured in config.json.
	•	Environment Variable Dependency: The NOTION_TOKEN environment variable must be set before using the workflow.

Troubleshooting
	•	Missing config.json: Ensure setup.py is executed to fetch shared databases.
	•	Template Errors: Verify the template IDs in config.json are valid.
	•	API Errors: Check that the Notion integration is properly shared with the target databases.

Contributions

Feel free to submit issues, suggestions, or pull requests to enhance this workflow. Contributions are welcome!

License

This project is licensed under the MIT License. See the LICENSE file for more details.