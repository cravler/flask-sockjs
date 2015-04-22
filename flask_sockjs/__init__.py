# -*- coding: utf-8 -*-

from observable import Observable
from flask import Blueprint, url_for
from twisted.web.resource import Resource
from txsockjs.utils import broadcast
from txsockjs.factory import SockJSResource
from .endpoint import Endpoint, EndpointProtocol, EndpointFactory

class SockJS(Observable):

    def __init__(self, twisted=None, resource=Resource(), url_prefix='ws', url_helper='ws_url_for'):
        self.app = None
        self.twisted = None
        self.resource = resource
        self.url_prefix = url_prefix
        self.url_helper = url_helper

        if twisted is not None:
            self.init_twisted(twisted)

    def init_twisted(self, twisted):
        if self.twisted is None:
            self.twisted = twisted
            twisted.add_resource(self.url_prefix, self.resource)
            twisted.on('run', self.init_app)

    def init_app(self, app):
        if self.app is None:
            self.app = app
            blueprint = Blueprint('sock_js', __name__)
            blueprint.route("/")(self.ws_url_for)
            app.register_blueprint(blueprint, url_prefix='/' + self.url_prefix)
            app.jinja_env.globals[self.url_helper] = self.ws_url_for

    def ws_url_for(self, endpoint=''):
        url = url_for('sock_js.ws_url_for', _external=True)
        return url + endpoint

    def createEndpoint(self, name, options=None):
        endpoint = Endpoint(name)
        if options is None:
            options = {'encoding': 'utf-8'}
        self.resource.putChild(name, SockJSResource(EndpointFactory.forProtocol(EndpointProtocol, endpoint), options))

        return endpoint
