from fabric.api import local
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
    local('docker-compose run docs make dirhtml')


def run_unit_tests():
    """Builds the dev image and runs the unit tests.
    """
    local('docker-compose run --rm dev nosetests --with-coverage tests/')


def run_robot_tests():
    """Run the robot test suites in robot/suites/* and put the report in robot/reports directory.
    """
    local("docker-compose up -d db")
    time.sleep(1)  # Sleeping to allow time for database to come online.
    local("docker-compose up -d server")
    time.sleep(2)  # Sleeping to allow server to migrate the database and import the fixtures.
    command = 'docker-compose run --rm robot pybot -o {} -l {} -r {} -N "{}" suites/* '.format(
        'report/output.xml',
        'report/log.html',
        'report/index.html',
        'Cinder Data')
    local(command)
    local("docker-compose stop")
    local("docker-compose rm -f")
