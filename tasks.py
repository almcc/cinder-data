from invoke import task

SOURCE_FILES = 'cinder_data/'


@task
def build_package(ctx):
    """Build the pip packages."""
    ctx.run('python setup.py sdist')


@task
def build_docs(ctx):
    """Build the html site and pdf file from the sphinx source."""
    with ctx.cd('docs/'):
        ctx.run('make html')
    print(('WARNING, did you install the cinder_data package? '
           'Source docs will not have been included if not.'))


@task
def lint_flake8(ctx):
    """Run the flake8 linter."""
    print('Flake8 report:')
    ctx.run('flake8 {src}'.format(src=SOURCE_FILES))


@task
def lint_pylint(ctx):
    """Run the pylint linter."""
    print('Pylint report:')
    ctx.run('pylint --rcfile=tox.ini {src}'.format(src=SOURCE_FILES))


@task(lint_flake8, lint_pylint)
def lint(ctx):
    """Run the linter tools against the source."""


@task
def sync_venv(ctx):
    """Sync the local pip environment with requirements.txt."""
    ctx.run('pip-sync requirements.txt')


@task
def update_requirements(ctx):
    """Update the requirements.txt to reflect the available lastest packages."""
    ctx.run('pip-compile --upgrade --output-file requirements.txt setup.py requirements.in')


@task(update_requirements, sync_venv)
def changed_requirement(ctx):
    """Update the requirements.txt file and sync the environment."""
    pass


@task
def bump_version(ctx, part, confirm=False):
    """Bump the package version."""
    if confirm:
        ctx.run('bumpversion {part}'.format(part=part))
    else:
        ctx.run('bumpversion --dry-run --allow-dirty --verbose {part}'.format(part=part))
        print('Add "--confirm" to actually perform the bump version.')
