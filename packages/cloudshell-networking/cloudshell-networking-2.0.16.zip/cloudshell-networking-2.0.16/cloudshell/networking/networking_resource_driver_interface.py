__author__ = 'CoYe'

from abc import ABCMeta
from abc import abstractmethod

class NetworkingResourceDriverInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_vlan(self, context, port, VLAN_Ranges, VLAN_Mode, additional_info='', qnq='', ctag=''):
        pass

    @abstractmethod
    def remove_vlan(self, context, port, VLAN_Ranges, VLAN_Mode, additional_info='', qnq='', ctag=''):
        pass

    @abstractmethod
    def send_custom_command(self, context, command):
        pass

    @abstractmethod
    def send_custom_config_command(self, context, command):
        pass

    @abstractmethod
    def save(self, context, folder_path, configuration_type):
        pass

    @abstractmethod
    def restore(self, context, path, restore_method):
        pass

    @abstractmethod
    def get_inventory(self, context):
        pass

    @abstractmethod
    def load_firmware(self, context, remote_host, file_path):
        pass

    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def apply_connectivity_changes(self, context, json):
        pass
