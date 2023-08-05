from abc import ABCMeta, abstractmethod


class Shell:
    __metaclass__ = ABCMeta

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def run(self, args):
        return self.channel.run(args)

    def close(self):
        if self.channel:
            self.channel.close()

    @abstractmethod
    def command_exists(self, command):
        pass

    @abstractmethod
    def run_as_elevated(self, args, password):
        pass
