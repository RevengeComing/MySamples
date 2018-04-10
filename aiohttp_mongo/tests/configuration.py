from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web

from twylacfg.app import create_app

class ConfigurationTestCase(AioHTTPTestCase):
    not_valid_config_1 = {
        "tenant":"test_tenant1",
        "configuration": {
            "username": "test_user",
            "password": "test_pass",
            "wsdl_urls": {
                "session_url": "https://session.manager.svc",
                "booking_url": "https://booking.manager.svc"
            }
        }
    }
    not_valid_config_2 = {
        "tenant":"test_tenant2",
        "integration_type": "test-information-type2",
        "configuration": {}
    }
    not_valid_config_3 = {
        "integration_type": "test-information-type3",
        "configuration": {
            "username": "test_user",
            "password": "test_pass"
        }
    }

    ok_data = {
        "tenant":"test_tenant",
        "integration_type": "test-information-type",
        "configuration": {
            "username": "test_user",
            "password": "test_pass",
            "wsdl_urls": {
                "session_url": "https://session.manager.svc",
                "booking_url": "https://booking.manager.svc"
            }
        }
    }

    update_ok_data = {
        "tenant":"test_tenant",
        "integration_type": "test-information-type",
        "configuration": {
            "username": "test_user******",
            "password": "test_pass",
            "wsdl_urls": {
                "session_url": "https://session.manager.svc",
                "booking_url": "https://booking.manager.svc"
            },
            "something": "something!"
        }
    }

    async def get_application(self):
        app = create_app()
        return app

    @unittest_run_loop
    async def test_get_health(self):
        resp = await self.client.request("GET", "/")
        self.assertEqual(resp.status, 200)
        text = await resp.text()
        self.assertEqual(text, 'Server is running...')

    @unittest_run_loop
    async def test_configuration_creation(self):
        await self.app['db'].drop_collection('configurations')

        #######################################
        # To create the config document for first time:
        resp = await self.client.request("POST", "/config", json=self.ok_data)
        self.assertEqual(resp.status, 200)

        resp_json = await resp.json()
        self.assertEqual(resp_json['description'], 'Configuration has been added succesfully.')
        self.assertEqual(resp_json['status'], 'ok')

        #######################################
        # To update config file:
        resp = await self.client.request("POST", "/config", json=self.update_ok_data)
        self.assertEqual(resp.status, 200)

        resp_json = await resp.json()
        self.assertEqual(resp_json['description'], 'Configuration succesfully updated.')
        self.assertEqual(resp_json['status'], 'ok')

        #######################################
        # To create/update a config document with application/x-www-form-urlencoded format:
        resp = await self.client.request("POST", "/config", data=self.ok_data)
        self.assertEqual(resp.status, 406)

        resp_json = await resp.json()
        self.assertEqual(resp_json['description'], 'The data has to be in json format.')
        self.assertEqual(resp_json['status'], 'error')

        #######################################
        # To create/update a config document with unvalid values (1):
        resp = await self.client.request("POST", "/config", json=self.not_valid_config_1)
        self.assertEqual(resp.status, 406)

        resp_json = await resp.json()
        self.assertEqual(resp_json['description'], 'Document is not valid.')
        self.assertEqual(resp_json['status'], 'error')

        #######################################
        # To create/update a config document with unvalid values (2):
        resp = await self.client.request("POST", "/config", json=self.not_valid_config_2)
        self.assertEqual(resp.status, 406)

        resp_json = await resp.json()
        self.assertEqual(resp_json['description'], 'Document is not valid.')
        self.assertEqual(resp_json['status'], 'error')

        #######################################
        # To create/update a config document with unvalid values (3):
        resp = await self.client.request("POST", "/config", json=self.not_valid_config_3)
        self.assertEqual(resp.status, 406)

        resp_json = await resp.json()
        self.assertEqual(resp_json['description'], 'Document is not valid.')
        self.assertEqual(resp_json['status'], 'error')

    @unittest_run_loop
    async def test_configurations_get(self):
        #######################################
        # To get the config after update:
        resp = await self.client.request("GET", "/config",
            params={'tenant':'test_tenant', 'integration_type':'test-information-type'})
        self.assertEqual(resp.status, 200)
        resp_json = await resp.json()
        self.assertEqual(resp_json, self.update_ok_data)

        #######################################
        # To get a not exist config :
        resp = await self.client.request("GET", "/config",
            params={'tenant':'test_tenant!@#', 'integration_type':'test-information-type!@#'})
        self.assertEqual(resp.status, 404)
        
        resp_json = await resp.json()
        self.assertEqual(resp_json['description'], 'Configuration not found.')
        self.assertEqual(resp_json['status'], 'error')

        #######################################
        # To get with unvalid data:
        resp = await self.client.request("GET", "/config",
            params={'integration_type':'test-information-type!@#'})
        self.assertEqual(resp.status, 406)
        
        resp_json = await resp.json()
        self.assertEqual(resp_json['description'], 'Need more data.')
        self.assertEqual(resp_json['status'], 'error')

        #######################################
        # To get with unvalid data:
        resp = await self.client.request("GET", "/config",
            params={'tenant':'test_tenant!@#'})
        self.assertEqual(resp.status, 406)
        
        resp_json = await resp.json()
        self.assertEqual(resp_json['description'], 'Need more data.')
        self.assertEqual(resp_json['status'], 'error')
