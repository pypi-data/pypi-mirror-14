from setuptools import setup, find_packages

setup(
    name='django-lightweight-queue',

    url="https://chris-lamb.co.uk/projects/django-lightweight-queue",
    version='2.0.2',
    description="Lightweight & modular queue and cron system for Django",

    author="Chris Lamb",
    author_email='chris@chris-lamb.co.uk',
    license="BSD",

    packages=find_packages(),

    install_requires=(
        'Django>=1.8',
    ),
)
