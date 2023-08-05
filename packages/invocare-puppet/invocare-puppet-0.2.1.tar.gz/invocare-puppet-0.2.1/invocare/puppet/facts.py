import os

from invocare.ssh import ssh
from invoke import task
from invoke.vendor import six

if six.PY3:
    from invoke.vendor import yaml3 as yaml
else:
    from invoke.vendor import yaml2 as yaml


@task(
    contextualized=True,
)
def external_facts(
    ctx,
    host,
    facts,
    hide=
    facts_path='/etc/facter/facts.d',
):
    """
    Installs external facts on a host as a YAML file.
    """

    config = ctx.config.get('external_facts', {})

