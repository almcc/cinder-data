from invoke import task

SOURCE_FILES = 'cinder_data/'

# @task
# def prep_docker(ctx):
#     """Pull and build the required docker containers."""
#     ctx.run('docker-compose pull')
#     ctx.run('docker-compose build')
#
#
# @task
# def stop_and_clean_docker(ctx):
#     """Stop all the containers and clean up."""
#     ctx.run('docker-compose stop')
#     ctx.run('docker-compose rm -f')
#
#
# @task
# def build_package(ctx):
#     """Build the pip packages."""
#     ctx.run('docker-compose run --rm dev python setup.py sdist')
#
#
# @task
# def build_docs(ctx):
#     """Build the html site and pdf file from the sphinx source."""
#     ctx.run('docker-compose run --rm docs bash make-docs.sh')
#
#
# @task
# def run_unit_tests(ctx):
#     """Build the dev image and runs the unit tests."""
#     long_command = 'docker-compose run --rm dev ' \
#         'nosetests --verbosity=2 -s --with-coverage --cover-package=cinder_data ' \
#         '--cover-inclusive --cover-erase --cover-branches --cover-html ' \
#         '--cover-html-dir=coverage-report/ tests/'
#     ctx.run(long_command)
#
#
# @task
# def run_robot_tests(ctx):
#     """Run the robot test suites in robot/suites/* and put the report in robot/reports directory."""
#     ctx.run('docker-compose up -d db')
#     time.sleep(5)  # Sleeping to allow time for database to come online.
#     ctx.run('docker-compose up -d server')
#     time.sleep(3)  # Sleeping to allow server to migrate the database and import the fixtures.
#     with settings(warn_only=True):
#         ctx.run('docker-compose run --rm robot bash run-tests.sh')
#     ctx.run('docker-compose stop')
#     ctx.run('docker-compose rm -f')


@task
def lint_flake8(ctx):
    print('Flake8 report:')
    ctx.run('flake8 {src}'.format(src=SOURCE_FILES))


@task
def lint_pylint(ctx):
    print('Pylint report:')
    ctx.run('pylint --rcfile=tox.ini {src}'.format(src=SOURCE_FILES))


@task(lint_flake8, lint_pylint)
def lint(ctx):
    """Run the linter tools against he source."""


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
    pass
