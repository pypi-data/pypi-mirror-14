__author__ = 'dcortes'

from repository_base import RepositoryBase
from dexma_api_v3.gateway.gateway_device import GatewayDevice
from dexma_api_v3.factory.device import Device


class RepositoryDevice(RepositoryBase):

    def __init__(self, endpoint, token):
        self.gateway = GatewayDevice(endpoint, token)

    def _validate_device(self, device_dict):
        device = Device(device_dict)
        device.validate()
        return device

    def get(self, id):
        device_dict = self.gateway.get(id)
        return self._validate_device(device_dict)

    def fetch(self, parameters=None):
        device_dict = self.gateway.fetch(parameters)
        return [self._validate_device(dev) for dev in device_dict]

    def save(self, device):
        status = self.gateway.save(device)
        return status