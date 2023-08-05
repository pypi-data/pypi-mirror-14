from setuptools import setup, find_packages

setup(
    name='django-force-logout',

    url="https://chris-lamb.co.uk/projects/django-force-logout",
    version='3.0.0',
    description="Framework to be able to forcibly log users out of Django projects",

    author="Chris Lamb",
    author_email='chris@chris-lamb.co.uk',
    license="BSD",

    packages=find_packages(),

    install_requires=(
        'Django>=1.8',
    ),
)
