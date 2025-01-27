# kodyy
A Notion Database powered Static Site Generator

## Introduction
I use this as a quality-of-life tool to render the pages of my portfolio website. While it's primarily tailored to meet my needs (with some flexibility for customization, as I'll discuss here), I'm making it open-source in case others find it useful. 

### Features
- Manage your website content directly in Notion databases and render HTML pages with the content using a single command.
- Translates each database entry into homepage tiles, with detailed content from each entry displayed on dedicated "read more" pages.
- Assign categories to entries and enable filtering by category.
- Define unique categories as standalone page blocks for better content organization.
- Sort entries chronologically by year.

## How to run
1. Clone this repository in your machine or download the project files via `Code > Download ZIP`. It is recommended to use a Python virtual environment (like [venv](https://docs.python.org/3/library/venv.html)) so that all modules and dependencies can be housed neatly in one place.

2. Open your terminal and `cd` to the repository directory and use `pip` to install dependencies:

    ```
    pip install -r requirements.txt
    ```
3. Create a `.env` file in the `site_generator_scripts` folder. A  `.env.example` file has been provided for you. 

4. In the `.env` file, `NOTION_SECRET` is your Internal Integration Secret. To generate this, create an Internal Integration from your Notion account here: [Your Notion Interations Dashboard](https://www.notion.so/profile/integrations). More information about how to set this up can be found here - [Install via internal integration token](https://www.notion.com/help/add-and-manage-connections-with-the-api#install-from-a-developer)

5. Run the following commands to execute the `db_create_helper.py` script wihin the `site_generator_scripts` folder to generate each database in Notion with the correct schema. The script takes the parent page ID as a parameter. The page identifier is the 32 character code that can be found at the end of a Notion page URL.

    For creating the `Site Pages` database:

        ```
        python3 db_create_helper.py pages enter_pageid_here
        ```
    For creating the `Site Links` database:
    
        ```
        python3 db_create_helper.py links enter_pageid_here
        ```
    

6. Once the databases are created, add the database IDs to your .env file. The database identifier is the 32 character code that can be found at the end of a Notion database page url.

7. To render content, use the following command to execute the `render_template.py` script. This will render html pages in the `output` folder based on the templates and site-generation logic:
    ```
    python3 render_template.py render  
    ```
8. For ease of regeneration, to remove rendered html pages, use the command below:
    ```
    python3 render_template.py clear_output_folder  
    ```


## Site-generation logic
- For each entry in the `Site Pages` database, a tile gets rendered in the homepage with all the available properties, and an image (if cover_image is uploaded in Notion)
- If any entry has content inside, this will get rendered in a stand-alone `read more` page, and a link to this page will be rendered in the homepage tile
- To enable the `last updated date` to get rendered in the `read more` pages, open `config.py` and set `show_last_updated_date` variable to `True`
- Image captions in Notion will get added as alt text 
- For each entry in the links database, this will get rendered as part of a list of links in a section within the home page. These collection of links can be used to organise anything. I use them to keep track of miscellaneous projects