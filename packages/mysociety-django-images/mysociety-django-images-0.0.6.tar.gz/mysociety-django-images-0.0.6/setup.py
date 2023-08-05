from setuptools import setup, find_packages
setup(
    name = "mysociety-django-images",
    version = "0.0.6",
    packages = find_packages(),
    author = "Edmund von der Burg",
    author_email = "evdb@ecclestoad.co.uk",
    description = "Attach images to any Django model, with helpful admin",
    license = "AGPL",
    keywords = "django images",
    install_requires = [
        'Django>=1.8',
        'sorl-thumbnail',
        'Pillow',
    ]
)
