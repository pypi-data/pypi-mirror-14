from invoke import task
from invoke.vendor import six

from invocare.ssh import ssh


@task(
    contextualized=True,
    help={
        'host': 'The host to run the Puppet agent on.',
        'debug': 'Set debug mode for Puppet agent run.',
        'environment': 'The environment to use for the Puppet agent run.',
        'noop': 'Sets noop option for Puppet agent run.',
        'user': 'The SSH login user for the Puppet agent run.',
        'test': 'Set test mode for the Puppet agent run.',
    }
)
def puppet_agent(
    ctx,
    host,
    debug=False,
    environment='production',
    hide=None,
    noop=False,
    tags=None,
    test=True,
    user=None,
    warn=False,
):
    """
    Runs the Puppet agent on the given host.
    """
    config = ctx.config.get('puppet_agent', {})

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

    tags = config.get('tags', tags)
    if tags:
        if isinstance(tags, six.string_types):
            tags = [tags]
        agent_opts.extend(['--tags', ','.join(tags)])

    if config.get('noop', noop):
        agent_opts.append('--noop')

    return ssh(
        ctx,
        host,
        'sudo puppet agent {}'.format(' '.join(agent_opts)),
        hide = config.get('hide', hide),
        user = config.get('user', user),
        warn = config.get('warn', warn)
    )
