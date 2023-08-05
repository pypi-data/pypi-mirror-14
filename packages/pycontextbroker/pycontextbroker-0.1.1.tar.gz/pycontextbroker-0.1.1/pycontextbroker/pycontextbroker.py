import json
import logging
import requests

logger = logging.getLogger(__name__)


class ContextBrokerClient(object):

    def __init__(self, ip, port, version='v1'):
        self.cb_address = 'http://{}:{}'.format(ip, port)
        self.cb_main_api = self.cb_address + '/' + version
        self.cb_entities_api = self.cb_main_api + '/contextEntities'
        self.cb_subscription_api = self.cb_main_api + '/subscribeContext'

        try:
            requests.get(self.cb_address)
        except:
            logger.exception("Failed to initialize ContextBroker client: "
                             "connection refused, please check provided IP and PORT")

    def get_version_data(self):
        return requests.get(self.cb_address + '/version').json()

    def get_orion_version_data(self):
        orion_data = self.get_version_data().get('orion')
        if not orion_data:
            logger.exception("Failed to gather Orion Context Broker version data")
        return orion_data

    def get_version(self):
        return self.get_orion_version_data().get('version')

    def get_uptime(self):
        return self.get_orion_version_data().get('uptime')

    def create_entity(self, entity_type, entity_id, attributes=None):
        data = {
            "id": entity_id,
            "type": entity_type
        }

        if attributes:
            # [{"name": "number", "type": "integer", "value": "0"}]
            data.update({"attributes": attributes})

        return requests.post(self.cb_entities_api,
                             data=json.dumps(data),
                             headers={'Content-Type': 'application/json'}).json()

    def get_entity(self, entity_type, entity_id):
        endpoint = '/type/{}/id/{}'.format(entity_type, entity_id)
        return requests.get(self.cb_entities_api + endpoint).json()

    def get_attribute_value(self, entity_type, entity_id, attribute_name):
        if self.get_entity(entity_type, entity_id).get('contextElement') is None:
            return None
        if self.get_entity(entity_type, entity_id).get('contextElement').get('attributes') is None:
            return None
        for attribute in self.get_entity(entity_type, entity_id).get('contextElement').get('attributes'):
            if attribute['name'] == attribute_name:
                return attribute.get('value')
        return None

    def update_attribute_value(self, entity_type, entity_id, attribute_name, attribute_value):
        data = {
            "value": attribute_value
        }
        endpoint = '/type/{}/id/{}/attributes/{}'.format(entity_type, entity_id, attribute_name)
        return requests.put(self.cb_entities_api + endpoint,
                            data=json.dumps(data),
                            headers={'Content-Type': 'application/json'}).json()

    def delete_entity(self, entity_type, entity_id):
        endpoint = '/type/{}/id/{}'.format(entity_type, entity_id)
        return requests.delete(self.cb_entities_api + endpoint).json()

    def subscribe_on_attribute_change(self, entity_type, entity_id, attribute_name, subscriber_endpoint):
        subscription_data = {
            "entities": [
                {
                    "type": entity_type,
                    "isPattern": "false",
                    "id": entity_id
                }
            ],
            "attributes": [
                attribute_name
            ],
            "reference": subscriber_endpoint,
            "duration": "P1M",
            "notifyConditions": [
                {
                    "type": "ONCHANGE",
                    "condValues": [
                        attribute_name
                    ]
                }
            ],
            "throttling": "PT5S"
        }

        return requests.post(self.cb_subscription_api,
                             data=json.dumps(subscription_data),
                             headers={'Content-Type': 'application/json'}).json()