from setuptools import setup, find_packages
setup(
    name = "django-file-archive",
    version = "0.0.2",
    packages = find_packages(),
    author = "Edmund von der Burg",
    author_email = "evdb@ecclestoad.co.uk",
    description = "Simple facility for uploading files in the Django admin",
    license = "AGPL",
    keywords = "django upload",
    install_requires = [
        'Django>=1.8',
    ]
)
