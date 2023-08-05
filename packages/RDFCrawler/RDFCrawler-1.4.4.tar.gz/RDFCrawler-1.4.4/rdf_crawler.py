import logging
import time
from sys import stdin
from threading import RLock

from rdflib import ConjunctiveGraph, URIRef

__author__ = 'Ignacio Molina Cuquerella'
__email__ = 'imolina@centeropenmiddleware.com'


class RDFCrawler:

    logger = logging.getLogger(__name__)

    def __init__(self, uri, domains=set()):
        """

        :param uri: root URI to start crawling .
        :param domains: list of permits domains to crawl.
        """
        self.root = uri
        self.graph_route = 'graph_store_%s' % hash(self.root)
        self.graph = ConjunctiveGraph('Sleepycat')
        self.graph.open(self.graph_route, create=True)
        self._filter_domains = domains
        self._filter_domains.add(uri)
        self.last_process_time = 0.0
        self.last_update = 0.0
        self.lock = RLock()

    def filter_uris(self, uri_list):

        """
        :param uri_list: list of URIs to be filtered.
        :return: filtered list of URIs.
        """
        return [uri for uri in uri_list for match in self._filter_domains
                if match in str(uri)]

    def _has_context(self, subject):
        """

        :param subject: the URIRef or URI to check if it has current context.
        :return: True if subject has a current context.
        """
        return len(self.graph.get_context(self._get_context_id(subject))) > 1

    @staticmethod
    def _get_context_id(subject):
        """

        :param subject: URIRef or URI from which the get context id.
        :return: context id of the resource.
        Example:
            subject -> http://www.example.org/#fragment
            context_id -> http://www.example.org/
        """
        return str(subject).split('#')[0]

    def start(self):
        """
            start method for crawling.
        """
        self.lock.acquire(True)

        # Erase old graph
        for t in self.graph:
            self.graph.remove(t)

        # Crawl for data
        logging.info('Start crawling: %s' % self.root)
        start_time = time.time()
        self._crawl([self.root])
        end_time = time.time()

        self.last_update = end_time
        self.last_process_time = end_time - start_time
        logging.info('Crawling complete after: %s seconds with %s predicates.'
                     % (self.last_process_time, len(self.graph)))

        self.lock.release()

    def _crawl(self, uri_list):
        """
        Recursive method that crawl RDF objects
        :param uri_list: list of URIs to crawl
        """
        if len(uri_list) > 0:

            for uri in uri_list:
                try:

                    # A few considerations about parsing params.
                    #   publicID = uri due to redirection issues
                    #   Format = None due to default params use 'XML'
                    self.graph.parse(uri, publicID=uri, format=None)
                    logging.info('[OK]: %s' % uri)
                except Exception as e:
                    logging.info('[Error]: %s: %s' % (uri, e))

            # Check that there are context that remains without parsing
            objects = set([self._get_context_id(o)
                           for o in set(self.graph.objects(None, None))
                           if isinstance(o, URIRef) and
                           not self._has_context(o)])

            self._crawl(self.filter_uris(objects))


if __name__ == '__main__':

    print('What URI want to crawl?')
    uri_name = stdin.readline().strip()

    filter_domains = set()
    filter_domains.add(uri_name)

    loop = True
    while loop:
        print('Do you want to crawl only in that domain or want to add some '
              'other? (<domain>/continue)')
        response = stdin.readline().strip()
        if 'continue' in response:
            loop = False
        else:
            filter_domains.add(response)
    crawler = RDFCrawler(uri_name, filter_domains)

    crawler.start()

    print('Graph size: %s' % len(crawler.graph))

    graph = crawler.graph

    out = False
    while not out:

        print('Your query is about a URI or an endpoint? (uri/endpoint)')
        endpoint = 'endpoint' in stdin.readline().strip()

        if endpoint:
            print('Which endpoint do you want? (exit to stop)')
            uri_name = stdin.readline().strip()
            if 'exit' not in uri_name:
                for (s, p, o) in graph.get_context(uri_name):
                    print(s, p, o)
            else:
                out = True
        else:
            print('Which URI do you want to know? (exit to stop)')
            uri_name = stdin.readline().strip()

            if 'exit' not in uri_name:
                print('Do you want to know that URI as subject or as object?'
                      ' (subject/object)')
                location = stdin.readline().strip()

                if 'object' in location:

                    for (s, p, o) in graph.triples((None, None,
                                                    URIRef(uri_name))):
                        print(s, p, o)

                elif 'subject' in location:

                    for (s, p, o) in graph.triples((URIRef(uri_name), None,
                                                    None)):
                        print(s, p, o)
                else:
                    print('Pardon?')
            else:
                out = True
