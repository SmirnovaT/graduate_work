import logging

import backoff
from elasticsearch import Elasticsearch
from elastic_transport import ConnectionError

from exceptions import EmptyIndexError


@backoff.on_exception(
    backoff.expo, (ConnectionError, ConnectionRefusedError, EmptyIndexError), max_tries=1000
)
def ping_elastic(es_client):
    logging.info("Pinging Elastic")
    if es_client.ping(error_trace=False):
        logging.info("The connection is established")
        index = "movies"
        if es_client.count(index=index)["count"] == 0:
            raise EmptyIndexError(index)
        logging.info("Elastic search successfully connected")


if __name__ == "__main__":
    es_client = Elasticsearch(
        hosts="http://search:9200",
        verify_certs=False,
        request_timeout=1000,
        retry_on_timeout=True,
        max_retries=1000,
    )
    ping_elastic(es_client)
