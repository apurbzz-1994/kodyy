import requests
class Utils:

    def __init__(self, headers):
        self.headers = headers

    
    def send_get_request_to_notion(self, endpoint_url):
        requested_response = None
        try:
            response = requests.post(endpoint_url, headers=self.headers)
            requested_response = response.json()
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
        finally:
            return requested_response
        
    
    def send_post_request_to_notion(self, endpoint_url, json_payload, success_message = None):
        requested_response = None
        try:
            response = requests.post(endpoint_url, json=json_payload, headers=self.headers)
            requested_response = response.json()
            if success_message!= None:
                print(success_message)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
        finally:
            return requested_response

        

