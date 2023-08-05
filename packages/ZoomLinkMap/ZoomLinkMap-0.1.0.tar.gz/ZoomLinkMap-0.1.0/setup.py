from setuptools import setup, find_packages

setup(
    name = "ZoomLinkMap",
    version = "0.1.0",
    keywords = ('Link Map File', 'analisy'),
    description = 'a tool to analisy the link map file that is genered by clang, to analisy your app\'s content',
    license = 'MIT License',
    url = 'http://example.com',

    author = 'yishuiliunian@gmail.com',
    author_email = 'yishuiliunian@gmail.com',
    packages = find_packages(),
    package_data = {'': ['*.*']},
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
    scripts=['bin/zoomLinkMap'],
)
