import shlex

from .shell import Shell


class Posix(Shell):
    def __init__(self, channel):
        self.channel = channel

    def command_exists(self, command):
        cmd = self.run(['command', '-v', command])

        return cmd.wait() == 0

    def run_as_elevated(self, args, password):
        if isinstance(args, basestring):
            args = shlex.split(args)

        elevated_args = ['sudo', '-S']
        elevated_args.extend(args)

        cmd = self.run(elevated_args)

        cmd.stdin.write(password)
        cmd.stdin.write('\n')
        cmd.stdin.flush()

        return cmd
