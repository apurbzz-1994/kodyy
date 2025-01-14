from Utils import *
from Link import *

class LinksApi:
    def __init__(self, notion_key, db_id):
        self.notion_key = notion_key
        self.db_id = db_id
        self.links = []
        self.headers = {
            "Authorization": "Bearer " + self.notion_key,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.query_links_endpoint = f"https://api.notion.com/v1/databases/{self.db_id}/query"
        self.util = Utils(self.headers)

    def __create_objects_from_link_data(self, api_response):
        link_objects = []
        for each_link in api_response:
            l_properties = each_link['properties']
            l_title = l_properties['title']['title'][0]['plain_text']
            l_link = l_properties['link']['url']
            l_description = l_properties['description']['rich_text'][0]['plain_text']
            l_tags = []

            #loading tags
            tags_raw = l_properties['tags']['multi_select']

            for each_tag in tags_raw:
                l_tags.append(each_tag['name'])

            #create the link object
            l_obj = Link(l_title, l_link, l_description, l_tags)
            link_objects.append(l_obj)
        return link_objects


    def get_all_links_from_database(self):
        all_links = self.util.get_all_rows_from_database(self.query_links_endpoint, self.__create_objects_from_link_data)
        
        return all_links