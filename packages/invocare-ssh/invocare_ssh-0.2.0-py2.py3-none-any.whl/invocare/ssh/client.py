from invocare.util import shell_escape
from invoke import task
from invoke.vendor import six


@task(
    contextualized=True,
    help={
        'host': 'The host to run the SSH command on.',
        'command': 'The command to run over SSH.',
        'user': 'The login user for SSH.',
    }
)
def ssh(ctx, host, command, hide=False, user=None, warn=False):
    """
    Runs a remote command via a local SSH invocation.
    """
    config = ctx.config.get('ssh', {})
    options = config.get('options', {})

    # Constructing the command to invoke over SSH.
    ssh_cmd = [config.get('path', 'ssh')]

    # Add SSH options to specify on the command line.
    for opt, val in config.get('options', {}).items():
        ssh_cmd.append('-o')
        ssh_cmd.append('{}={}'.format(opt, val))

    # Constructing the host to SSH to.
    user = config.get('user', user)
    host = config.get('host', host)
    if user:
        ssh_cmd.append('{}@{}'.format(user, host))
    else:
        ssh_cmd.append(host)

    # If command is a string, make a list.
    if isinstance(command, six.string_types):
        command = [command]

    # Quote and escape all elements of the SSH command.  Join individual
    # commands to be executed over SSH with ' && '.
    ssh_cmd.append('"{}"'.format(
            ' && '.join(map(shell_escape, command))
    ))

    return ctx.run(
        ' '.join(ssh_cmd),
        hide=config.get('hide', hide),
        warn=config.get('warn', warn)
    )
