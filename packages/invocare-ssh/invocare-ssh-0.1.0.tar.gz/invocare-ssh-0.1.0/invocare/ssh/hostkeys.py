from invoke import task


@task(
    contextualized=True,
    help={
        'host': 'The host name to remove SSH keys for.',
    }
)
def ssh_hostkey_remove(ctx, host, hide=None, warn=False):
    """
    Cleans out SSH host key for given host.
    """
    config = ctx.config.get('ssh-keygen', {})
    return ctx.run(
        'ssh-keygen -R {}'.format(config.get('host', host)),
        hide=config.get('hide', hide),
        warn=config.get('warn', warn)
    )
