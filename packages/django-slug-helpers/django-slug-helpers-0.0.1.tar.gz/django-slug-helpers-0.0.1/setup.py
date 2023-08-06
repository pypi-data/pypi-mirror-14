from setuptools import setup, find_packages
setup(
    name = "django-slug-helpers",
    version = "0.0.1",
    packages = find_packages(),
    author = "Mark Longair",
    author_email = "mark-pypi@longair.net",
    description = "A simple model for redirecting from old slugs",
    license = "AGPL",
    keywords = "django images",
    install_requires = [
        'Django>=1.8',
    ]
)
