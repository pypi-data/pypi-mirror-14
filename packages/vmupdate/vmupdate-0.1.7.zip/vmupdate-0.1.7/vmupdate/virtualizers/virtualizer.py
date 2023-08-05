from abc import ABCMeta, abstractmethod


class Virtualizer:
    __metaclass__ = ABCMeta

    @abstractmethod
    def list_vms(self):
        pass

    @abstractmethod
    def start_vm(self, uid):
        pass

    @abstractmethod
    def stop_vm(self, uid):
        pass

    @abstractmethod
    def get_vm_status(self, uid):
        pass

    @abstractmethod
    def get_vm_os(self, uid):
        pass

    @abstractmethod
    def get_ssh_info(self, uid, ssh_port):
        pass

    @abstractmethod
    def enable_ssh(self, uid, host_port, guest_port):
        pass
