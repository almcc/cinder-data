from fabric.api import local, settings
from fabric.colors import yellow
import time


def prep_docker():
    """Pull and build the required docker containers.
    """
    local('docker-compose pull')
    local('docker-compose build')


def stop_and_clean_docker():
    """Stop all the containers and clean up
    """
    local('docker-compose stop')
    local('docker-compose rm -f')


def build_package():
    """Build the pip packages
    """
    local('docker-compose run --rm dev python setup.py sdist')


def build_docs():
    """Build the html site and pdf file from the sphinx source.
    """
    local('docker-compose run --rm docs bash make-docs.sh')


def run_unit_tests():
    """Builds the dev image and runs the unit tests.
    """
    local('docker-compose build dev')
    local('docker-compose run --rm dev nosetests --verbosity=2 -s --with-coverage --cover-package=cinder_data --cover-inclusive --cover-erase  --cover-branches --cover-html --cover-html-dir=coverage-report/ tests/')


def run_robot_tests():
    """Run the robot test suites in robot/suites/* and put the report in robot/reports directory.
    """
    local("docker-compose up -d db")
    time.sleep(5)  # Sleeping to allow time for database to come online.
    local("docker-compose up -d server")
    time.sleep(3)  # Sleeping to allow server to migrate the database and import the fixtures.
    with settings(warn_only=True):
        local('docker-compose run --rm robot bash run-tests.sh')
    local("docker-compose stop")
    local("docker-compose rm -f")


def run_linter():
    """Run the linter tools against he source
    """
    local('docker-compose run --rm linter flake8 cinder_data')
    local('docker-compose run --rm linter rflint -v -r robot/')
