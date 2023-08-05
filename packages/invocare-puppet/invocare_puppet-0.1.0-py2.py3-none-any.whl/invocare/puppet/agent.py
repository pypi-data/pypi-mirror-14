from invoke import task

from invocare.ssh import ssh_run


@task(
    contextualized=True,
    help={
        'host': 'The host to run the Puppet agent on.',
        'debug': 'Set debug mode for Puppet agent run.',
        'environment': 'The environment to use for the Puppet agent run.',
        'noop': 'Sets noop option for Puppet agent run',
        'user': 'The SSH login user for the Puppet agent run',
        'test': 'Set test mode for the Puppet agent run',
    }
)
def puppet_agent(
    ctx,
    host,
    debug = False,
    environment = 'production',
    hide = None,
    noop = False,
    test = True,
    user = None,
    warn = False,
    ):
    """
    Runs the Puppet agent on the given host.
    """
    config = ctx.config.get('puppet', {})

    agent_opts = [
        '--onetime',
        '--no-daemonize',
        '--environment',
        config.get('environment', environment)
    ]

    if config.get('test', test):
        # Don't actually use `--test` option, due to the non-standard
        # error codes by default.
        agent_opts.extend([
            '--verbose',
            '--ignorecache',
            '--no-usecacheonfailure',
            '--no-splay'
        ])

    if config.get('debug', debug):
        agent_opts.append('--debug')

    if config.get('noop', noop):
        agent_opts.append('--noop')

    return ssh_run(
        ctx,
        config.get('host', host),
        'sudo puppet agent {}'.format(' '.join(agent_opts)),
        hide = config.get('hide', hide),
        user = config.get('user', user),
        warn = config.get('warn', warn)
    )
