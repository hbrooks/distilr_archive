from uuid import uuid4
import unittest

import requests

AMAZON_ENTITY_ID = "a3862aec-cd0b-4c1a-8eb6-9ecee158324f"

def build_integration_test_case(backend_url):
    class TestBasicFlow(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
            cls.url_prefix = backend_url

        def can_create_timeline(self):
            r = requests.post(
                url=self.url_prefix+'/timelines',
                json={
                    "q": "Donald Trump",
                }
            )
            self.assertEqual(r.status_code, 200)
            response_body = r.json()
            self.assertTrue('timelineId' in response_body)
            self.assertTrue(response_body['timelineId'] != None)

        def test_flow(self):
            # self.can_search()
            self.can_create_timeline()

    return TestBasicFlow
        

if __name__ == '__main__':
    test_class = build_integration_test_case('http://localhost:6001')
    unittest.main()