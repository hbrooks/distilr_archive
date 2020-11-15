import requests
import logging


LOG = logging.getLogger(__name__)


class DistilrMicroserviceUtilities:
    
    @staticmethod
    def make_request(http_method, url, body, error_handlers):
        """
        Error handlers is a map of HTTP response code to function where
        the argument is the response.
        """

        r = requests.request(
            method=http_method,
            url=url, 
            headers={
                'content-type': 'application/json',
            },
            json=body,
            verify=False, # TODO: Remove before going live.  
        )

        response_json = r.json()

        if r.ok:
            # TODO: Make sure that the response is a JSON via the headers.
            return response_json
        else:
            response_status_code = r.status_code
            if response_status_code in error_handlers:
                return error_handlers[response_status_code](response_json)
            else:
                # TODO: Throw new exception that means we didn't expect the status code we got..
                r.raise_for_status()

    @staticmethod
    def check_health(service_url):
        r = requests.request(
            method='GET',
            url=service_url+'/healthCheck',
            verify=False,
        )
        return r.ok
        
