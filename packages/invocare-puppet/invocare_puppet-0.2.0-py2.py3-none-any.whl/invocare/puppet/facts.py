from invoke import task


@task(
    contextualized=True,
)
def external_facts(
    facts_path='/etc/facter/facts.d',
):
    """
    """
    pass
