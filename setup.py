from setuptools import find_packages, setup

setup(
    name='schedule_lib',
    packages=find_packages(include=['event_lib','calendar_lib']),
    version='0.1.0',
    description='events and calendar library',
    author='Me',
    install_requires=['DateTime','typing','dataclasses','google-api-python-client','google-auth-oauthlib','google-auth'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==8.3.3'],
    test_suite='tests',
)