import shlex

from .shell import Shell


class Posix(Shell):
    def __init__(self, channel):
        self.channel = channel

    def command_exists(self, command):
        stdin, stdout, stderr = self.run(['command', '-v', command])

        return stdout.channel.recv_exit_status() == 0

    def run_as_elevated(self, args, password):
        if isinstance(args, basestring):
            args = shlex.split(args)

        elevated_args = ['sudo', '-S']
        elevated_args.extend(args)

        stdin, stdout, stderr = self.run(elevated_args)

        stdin.write(password)
        stdin.write('\n')
        stdin.flush()

        return stdin, stdout, stderr
