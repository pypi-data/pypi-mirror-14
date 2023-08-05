from setuptools import setup, find_packages

__author__ = 'Ignacio Molina Cuquerella'
__email__ = 'imolina@centeropenmiddleware.com'

setup(
    name = 'RDFCrawler',
    version = '1.4.4',
    author = 'Ignacio Molina Cuquerella',
    author_email = 'imolina@centeropenmiddleware.com',
    description = 'A RESTful services for Python that explores and replicates '
                  'a RDF topology.',
    keywords = ['rdf', 'crawler', 'replication'],
    url = 'https://github.com/ignaciomolina/RDFCrawler',
    download_url = 'https://github.com/ignaciomolina/RDFCrawler/tarball/1.4.4',
    packages = find_packages(),
    scripts= ['rdf_service.py', 'rdf_crawler.py'],
    requires=['flask', 'rdflib']
)
