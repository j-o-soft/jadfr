import os
import sys

from fabric.api import env, lcd, local, require, settings, task


# Build directory name
env.build_dir = '_build'
# Base path to the project
env.base_path = os.path.dirname(__file__)
# Base path of the django application
env.project_path = os.path.join(env.base_path, 'jadfr')
env.build_path = os.path.join(env.base_path, env.build_dir)


@task
def staging():
    env.environment = 'staging'


@task
def production():
    env.environment = 'production'


@task
def vagrant():
    env.environment = 'local'


@task
def deploy():
    require('environment')


@task
def test():
    """
    Run the tests and create a coverage report
    """
    with lcd(env.project_path):
        pytest_xml_file = os.path.join(env.build_path, 'pytest.xml')
        with settings(warn_only=True):
            # Remove old coverage results
            local('coverage erase')
            # default directory for html test coverage report files
            html_report_dir = os.path.join(env.build_path, 'htmlcov')
            coverage_file = os.path.join(env.build_path, 'coverage.xml')
            pytest_result = local('coverage run --source=\'.\' --rcfile=../coveragerc'
                                  ' -m py.test --junitxml=%s -x' % pytest_xml_file)

            local('coverage html --rcfile=../coveragerc -d %s' % html_report_dir)
            local('coverage xml --rcfile=../coveragerc -o %s' % coverage_file)
            # Remove coverage results
            local('coverage erase')

            return_code = int(pytest_result.return_code)
            if return_code > 0:
                sys.exit(return_code)
