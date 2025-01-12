# Notion Page Creation Workflow for Alfred

This repository provides an Alfred workflow that integrates with the Notion API, enabling users to **create pages in Notion databases quickly and efficiently**. Whether you're using templates for standardized content or creating custom pages, this workflow simplifies your Notion page creation process directly from Alfred.

---

## Key Features

- **Effortless Page Creation**: Create new pages in your Notion databases directly from Alfred.
- **Template Integration**: Use preconfigured templates to quickly generate pages with standardized content.
- **Simple Configuration**: Customize databases and templates through easily editable JSON files.

---

## Prerequisites

To use this workflow, you'll need:

- **Python**: Ensure Python 3.7 or higher is installed on your system.
- **Notion API Token**: Generate an integration token from the [Notion Developers](https://www.notion.so/my-integrations) page.
- **Alfred App**: Install Alfred with the Powerpack for running workflows.

---

## Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/notion-alfred-workflow.git
   cd notion-alfred-workflow
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Notion Token**:
   Set your Notion API token as an environment variable:
   ```bash
   export NOTION_TOKEN="your-notion-token"
   ```

5. **Fetch Databases**:
   Use the `setup.py` script to fetch shared Notion databases and create a `databases.json` configuration file:
   ```bash
   python setup.py
   ```

6. **Install the Alfred Workflow**:
   - Open Alfred Preferences.
   - Import the `.alfredworkflow` file located in this repository.

---

## Configuration

The workflow uses two configuration files: 

- **`databases.json`**: Contains information about the Notion databases available for creating pages.
- **`templates.json`**: Defines templates associated with your databases.

### Example: `databases.json`
```json
{
    "databases": [
        {
            "label": "Tasks",
            "id": "1482cd0c-ca79-4bda-9341-dea90c9dd5a3"
        },
        {
            "label": "Projects",
            "id": "7f84a64e-70f7-4b75-90cd-2d253f5ead1f"
        }
    ]
}
```

### Example: `templates.json`
```json
{
    "templates": [
        {
            "label": "Product Presentation Task",
            "id": "8b628b51afc84bdca85b0fc4bfea341c"
        },
        {
            "label": "OTQA Task",
            "id": "e050c11b3b4f49eb984e0f507599ad2a"
        }
    ]
}
```

### Editing Configuration Files
You can manually edit these files to update the database labels, IDs, or add templates as needed.

---

## Usage

### Creating a New Page
1. **Trigger the Workflow**:
   - Open Alfred and type `page`.
   - Select a database label from the options.

2. **Specify the Page Title**:
   - Provide a title for the new page after selecting the database.

3. **Page Creation**:
   - A new page is created in the selected database.
   - If you configured a template for the database, the page will inherit its structure and content.

### Creating a Page Using a Template
1. **Trigger the Workflow**:
   - Open Alfred and type `template`.
   - Select a template from the list.

2. **Specify the Page Title**:
   - Provide a title for the new page after selecting the template.

3. **Page Creation**:
   - A new page is created in the associated database using the selected template.

---

## Files in This Repository

### Python Scripts
- **`main.py`**: Core script for creating pages and templates.
- **`setup.py`**: Fetches shared Notion databases and generates `databases.json`.
- **`client.py`**: Handles interactions with the Notion API.
- **`utils.py`**: Provides helper functions for configuration and schema validation.

### Configuration Files
- **`databases.json`**: Stores database IDs and labels.
- **`templates.json`**: Stores template IDs and labels.

### Alfred Workflow
- **`icon.png`**: The icon displayed in Alfred.
- **`info.plist`**: Configuration for the Alfred workflow.

---

## Troubleshooting

- **Missing `databases.json`**:
  Ensure you’ve run `setup.py` to fetch your shared Notion databases.

- **Template Errors**:
  Verify that the template IDs in `templates.json` are correct and match those in your Notion workspace.

- **Notion Token Issues**:
  Ensure that your `NOTION_TOKEN` environment variable is set and the integration is shared with the relevant databases.

---

## Contributions

Contributions are welcome! Feel free to submit issues, feature requests, or pull requests to improve this workflow.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.