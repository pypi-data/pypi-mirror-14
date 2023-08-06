# -*- coding: utf-8 -*-
from __future__ import absolute_import
import io
import json
import os

import concurrent.futures
import crochet
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.protocol import Protocol
import six
import twisted.web.client
from six.moves.urllib_parse import urlparse
from twisted.web.client import Agent, ProxyAgent
from twisted.web.client import FileBodyProducer

from . import __about__
from .common import listify_headers


DEFAULT_USER_AGENT = 'Fido/%s' % __about__.__version__

DEFAULT_CONTENT_TYPE = 'application/json'


class Response(object):
    """An HTTP response.

    :ivar code: the integer response code.
    :ivar headers: a dictionary of response headers, mapping from string keys
        to lists of string values.
    :ivar body: the response body.
    :ivar reason: the http reason phrase.
    """

    def __init__(self, code, headers, body, reason):
        self.headers = dict(headers.getAllRawHeaders())
        self.code = code
        self.body = body
        self.reason = reason

    def json(self):
        """Helper function to load a JSON response body."""
        return json.loads(self.body)


class HTTPBodyFetcher(Protocol):

    def __init__(self, response, finished):
        self.buffer = io.BytesIO()
        self.response = response
        self.finished = finished

    def dataReceived(self, data):
        self.buffer.write(data)

    def connectionLost(self, reason):
        if (reason.check(twisted.web.client.ResponseDone) or
                reason.check(twisted.web.http.PotentialDataLoss)):
            self.finished.callback(
                Response(
                    code=self.response.code,
                    headers=self.response.headers,
                    body=self.buffer.getvalue(),
                    reason=self.response.phrase,
                )
            )
        else:
            self.finished.errback(reason)


def fetch_inner(url, method, headers, body, future, timeout, connect_timeout):
    """This runs inside a separate thread and orchestrates the async IO
    work.
    """

    finished = Deferred()

    # Set an exception on the future in case of error
    def finished_errorback(error):
        try:
            error.raiseException()
        except BaseException as e:
            future.set_exception(e)
    finished.addErrback(finished_errorback)

    # Set the result on the future in case of success
    finished.addCallback(future.set_result)

    bodyProducer = None
    if body:
        bodyProducer = FileBodyProducer(io.BytesIO(body))
        # content-length needs to be removed because it was computed based on
        # body but body is now being processed by twisted FileBodyProducer
        # causing content-length to lose meaning and break the client.
        # FileBodyProducer will take care of re-computing length and re-adding
        # a new content-length header later.
        headers = dict(
            (key, value)
            for (key, value) in six.iteritems(headers)
            if key.lower() != 'content-length'
        )

    deferred = get_agent(reactor, connect_timeout).request(
        method=method,
        uri=url,
        headers=listify_headers(headers),
        bodyProducer=bodyProducer)

    # Fetch the body once we've received the headers
    def response_callback(response):
        response.deliverBody(HTTPBodyFetcher(response, finished))

    deferred.addCallback(response_callback)
    deferred.addErrback(finished.errback)

    if timeout is not None:
        # Cancel the request if we hit the timeout
        def cancel_timer(response):
            if timer.active():
                timer.cancel()
            return response
        timer = reactor.callLater(timeout, deferred.cancel)
        finished.addBoth(cancel_timer)

    return crochet.EventualResult(finished, crochet._main._reactor)


def get_agent(reactor, connect_timeout=None):
    """Return appropriate agent based on whether an http_proxy is used or not.

    :param connect_timeout: connection timeout in seconds
    :type connect_timeout: float
    :returns: :class:`twisted.web.client.ProxyAgent` when an http_proxy
        environment variable is present, :class:`twisted.web.client.Agent`
        otherwise.
    """
    # TODO: Would be nice to have https_proxy support too.
    http_proxy = os.environ.get('http_proxy')
    if http_proxy is None:
        return Agent(reactor, connectTimeout=connect_timeout)

    parse_result = urlparse(http_proxy)
    http_proxy_endpoint = TCP4ClientEndpoint(
        reactor,
        parse_result.hostname,
        parse_result.port or 80,
        timeout=connect_timeout)

    return ProxyAgent(http_proxy_endpoint)


def fetch(url, timeout=None, connect_timeout=None, method='GET',
          content_type=DEFAULT_CONTENT_TYPE, user_agent=DEFAULT_USER_AGENT,
          headers=None, body=''):
    """Make an HTTP request.

    :param url: the URL to fetch.
    :param timeout: maximum allowed request time, in seconds. Defaults to
        None which means to wait indefinitely.
    :param connect_timeout: maximum time allowed to establish a connection,
        in seconds.
    :param method: the HTTP method.
    :param headers: a dictionary mapping from string keys to lists of string
        values.  For example::

            {
                'X-Foo': ['Bar'],
                'X-Baz': ['Quux'],
            }

    :param content_type: the content type.
    :param user_agent: the user agent.
    :param body: the body of the request.

    :returns: a :py:class:`concurrent.futures.Future` that returns a
        :py:class:`Response` if the request is successful.
    """
    if isinstance(url, six.text_type):
        url = url.encode('utf-8')

    # Make a copy to avoid mutating the original value
    headers = dict(headers or {})

    # Add basic header values if absent
    if 'User-Agent' not in headers:
        headers['User-Agent'] = [user_agent]
    if 'Content-Type' not in headers:
        headers['Content-Type'] = [content_type]

    crochet.setup()
    future = concurrent.futures.Future()
    if future.set_running_or_notify_cancel():
        fetch_inner(url, method, headers, body, future, timeout,
                    connect_timeout)
    return future
