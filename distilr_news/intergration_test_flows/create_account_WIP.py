from uuid import uuid4
import unittest

import requests

AMAZON_ENTITY_ID = "a3862aec-cd0b-4c1a-8eb6-9ecee158324f"

def build_integration_test_case(backend_url):
    class TestBasicFlow(unittest.TestCase):
        

        @classmethod
        def setUpClass(cls):
            cls.url_prefix = backend_url
            cls.email = str(uuid4())+'@gmail.com'

        def can_create_account(self):
            r = requests.post(
                url=self.url_prefix+'/users',
                json={
                    'email': self.email,
                    'password': 'anything right now... the password created is always...'
                },
                verify=False,
            )
            self.assertEqual(r.status_code, 200)
            response_body = r.json()
            self.assertTrue('sessionId' in response_body)
            self.session_id = response_body['sessionId']

        def can_log_in(self):
            r = requests.post(
                url=self.url_prefix+'/users/login',
                json={
                    'email': self.email,
                    'password': 'anything right now... the password created is always...'
                },
                verify=False,
            )
            self.assertEqual(r.status_code, 200)
            response_body = r.json()
            self.assertTrue('sessionId' in response_body)
            self.session_id = response_body['sessionId']

        def can_search(self):
            r = requests.get(
                url=self.url_prefix+'/search',
                params={'q':'Amaz', 's':self.session_id},
                verify=False,
            )
            self.assertEqual(r.status_code, 200)
            response_body = r.json()
            self.assertTrue(len(response_body) >= 1)
            r = requests.get(
                url=self.url_prefix+'/search',
                params={'q':'Amazon', 's':self.session_id},
                verify=False,
            )
            response_body = r.json()
            self.assertTrue(len(response_body) >= 1)
            for result in response_body:
                if result['entityId'] == AMAZON_ENTITY_ID:
                    break
            else:
                self.fail('expected to see AMAZON_ENTITY_ID in result body')

        def can_get_timeline(self):
            r = requests.get(
                url=self.url_prefix+'/entities/{}'.format(AMAZON_ENTITY_ID),
                params={'s':self.session_id},
                verify=False,
            )
            self.assertEqual(r.status_code, 200)
            response_body = r.json()
            self.assertTrue('latestTimeline' in response_body)
            self.assertTrue(response_body['latestTimeline'] != None)

        def test_flow(self):
            self.can_create_account()
            self.can_log_in()
            self.can_search()
            self.can_get_timeline()

    return TestBasicFlow
        

if __name__ == '__main__':
    test_class = build_integration_test_case('https://localhost:6001')
    unittest.main()