# TODO:10 Switch fab to invoke
# https://almcc.me/blog/2018/06/03/python-invoke-with-tab-completion/

from fabric.api import local, settings
from fabric.colors import yellow
import time

def prep_docker():
    """Pull and build the required docker containers."""
    local('docker-compose pull')
    local('docker-compose build')


def stop_and_clean_docker():
    """Stop all the containers and clean up."""
    local('docker-compose stop')
    local('docker-compose rm -f')


def build_package():
    """Build the pip packages."""
    local('docker-compose run --rm dev python setup.py sdist')


def build_docs():
    """Build the html site and pdf file from the sphinx source."""
    local('docker-compose run --rm docs bash make-docs.sh')


def run_unit_tests():
    """Build the dev image and runs the unit tests."""
    long_command = 'docker-compose run --rm dev ' \
        'nosetests --verbosity=2 -s --with-coverage --cover-package=cinder_data ' \
        '--cover-inclusive --cover-erase --cover-branches --cover-html ' \
        '--cover-html-dir=coverage-report/ tests/'
    local(long_command)


def run_robot_tests():
    """Run the robot test suites in robot/suites/* and put the report in robot/reports directory."""
    local('docker-compose up -d db')
    time.sleep(5)  # Sleeping to allow time for database to come online.
    local('docker-compose up -d server')
    time.sleep(3)  # Sleeping to allow server to migrate the database and import the fixtures.
    with settings(warn_only=True):
        local('docker-compose run --rm robot bash run-tests.sh')
    local('docker-compose stop')
    local('docker-compose rm -f')


def run_linter():
    """Run the linter tools against he source."""
    local('docker-compose run --rm linter flake8 .')
    local('docker-compose run --rm linter rflint -v -r robot/')


def run_ci_targets():
    """Run the same targets that travis-ci will."""
    print(yellow('WARNING: This fab target has to be manually kept in with .travis.yml, '
                 'there is no guarantee that they are actually in sync.'))
    run_linter()
    run_unit_tests()
    build_docs()
    run_robot_tests()


def sync_venv():
    local('pip sync requirements.txt')


def update_requirements():
    local('pip-compile --upgrade --output-file requirements.txt setup.py requirements.in')
