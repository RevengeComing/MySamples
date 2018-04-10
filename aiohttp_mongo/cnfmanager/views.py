import sys
import json
import logging
import traceback

from aiohttp import web

from .models import Configuration, NotValidDocument

logger = logging.getLogger('config_service')

routes = web.RouteTableDef()

class BaseView(web.View):
    def error(self, msg, log_exc=False, status=500):
        data = {"status":"error", "description":msg}
        if log_exc:
            logger.exception("Unknown error happened...")
        return web.json_response(data, status=status)

    def unknown_error(self):
        return self.error(
            'An unknown error aquired, please contact system administrator.',
            log_exc=True
        )

    def json_error(self):
        return self.error('The data has to be in json format.', status=406)

    @property
    def db(self):
        return self.request.app['db']


@routes.view('/')
class HealthView(BaseView):
    async def get(self):
        return web.Response(text='Server is running...')


@routes.view('/config')
class ConfigurationView(BaseView):
    """
    These configuration documents should be placed into a document store
    with a MongoDB interface.
    """

    def not_found(self):
        return self.error("Configuration not found.", status=404)

    def not_valid_doc(self):
        return self.error('Document is not valid.', status=406)

    def need_more(self):
        return self.error('Need more data.', status=406)

    async def get(self):
        """        
        A GET request to the same endpoint with the parameters tenant and
        integration_type should return the available document with those keys,
        and an appropriate error response if none is available.
        """
        tenant = self.request.query.get('tenant')
        integration_type = self.request.query.get('integration_type')
        if not integration_type or not tenant:
            return self.need_more()

        config = await Configuration(self.db).query(tenant=tenant,
                                                    integration_type=integration_type)
        if not config:
            return self.not_found()

        return web.json_response(config.to_dict())

    async def post(self):
        """
        A sample JSON accepted as a POST request to this
        endpoint looks like this:

        {
            "tenant": "acme",
            "integration_type": "flight-information-system",
            "configuration": {
                "username": "acme_user",
                "password": "acme12345",
                "wsdl_urls": {
                    "session_url": "https://session.manager.svc",
                    "booking_url": "https://booking.manager.svc"
                }
            }
        }

        When such a JSON document is posted,
        and there is already an existing configuration with the same tenant and
        integration_type values, the existing document should be updated by
        merging the new configuration dictionary with the existing one.
        """
        try:
            document = await self.request.json()
        except json.decoder.JSONDecodeError:
            return self.json_error()
        except:
            return self.unknown_error()

        config = await Configuration(self.db).query(tenant=document.get('tenant'),
                                        integration_type=document.get('integration_type'))
        if not config:
            try:
                await Configuration(self.db, document=document).insert()

                return web.json_response(
                    {'status':'ok', 'description':'Configuration has been added succesfully.'}
                )
            except NotValidDocument:
                return self.not_valid_doc()
            except:
                return self.unknown_error()
        else:
            if document['configuration']:
                config = await config.update(document['configuration'])
            
                return web.json_response(
                    {'status':'ok', 'description':'Configuration succesfully updated.'}
                )
            else:                
                return self.error(
                    'Configuration is not allowed to be empty.',
                    status=406
                )