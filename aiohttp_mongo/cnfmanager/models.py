class NotValidDocument(Exception):
    def __init__(self, message):
        self.message = message


class Configuration():
    """
    Object Mapper for configuration document.

    To query simply write:
    config = await Configuration(db).query(tenant=tenant, integration_type=integration_type)

    To insert:
    result = await Configuration(self.db, document=document).insert()

    To update:
    config = await Configuration(db).query(tenant=tenant, integration_type=integration_type)
    config = await config.update(new_config)
    """
    __slots__ = ['db', 'tenant', 'integration_type', 'configuration', '_id']

    def __init__(self, db, document=None):
        self.db = db
        if document:
            self.fill(document)
        else:
            self._id = None
            self.tenant = None
            self.integration_type = None
            self.configuration = None

    def fill(self, doc):
        self._id = doc.get('_id')
        self.tenant = doc.get('tenant')
        self.integration_type = doc.get('integration_type')
        self.configuration = doc.get('configuration')
        self.validate()
        return self

    def validate(self):
        if (self.tenant and self.integration_type and self.configuration):
            return
        raise NotValidDocument('Document is not valid.')

    async def insert(self):
        result = await self.db.configurations.insert_one(self.to_dict())
        return result

    async def query(self, tenant=None, integration_type=None):
        document = await self.db.configurations.find_one(
            {'tenant': tenant, 'integration_type':integration_type}
        )
        if not document:
            return

        self.fill(document)
        return self

    async def update(self, new_config):
        self.merge(new_config)
        result = await self.db.configurations.update_one(
            {'tenant': self.tenant, 'integration_type':self.integration_type},
            {'$set': {'configuration': self.configuration}}
        )
        return self

    def merge(self, new_config):
        self.configuration = {**self.configuration, **new_config}

    def to_dict(self):
        return {
            'tenant': self.tenant,
            'integration_type': self.integration_type,
            'configuration': self.configuration
        }

    def __repr__(self):
        return "<Configuration tenant={0} integration_type={1}".format(
            self.tenant, self.integration_type
        )