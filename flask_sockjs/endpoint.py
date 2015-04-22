# -*- coding: utf-8 -*-

import uuid
from observable import Observable
from twisted.internet.protocol import Factory, Protocol

class EndpointFactory(Factory):
    def __init__(self, endpoint):
        self.endpoint = endpoint

class EndpointProtocol(Protocol):
    def connectionMade(self):
        self.factory.endpoint.transports.add(self.transport)
        self.factory.endpoint.trigger('connection', self.transport)

    def dataReceived(self, data):
        self.factory.endpoint.trigger('data', self.transport, data)

    def connectionLost(self, reason):
        value = None
        if reason and reason.value:
            value = reason.value

        self.factory.endpoint.transports.remove(self.transport)
        self.factory.endpoint.trigger('close', self.transport, value)

class Transports(dict):
    def __init__(self, *args, **kwargs):
        super(Transports, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.values()

    def add(self, transport):
        transport.id = str(uuid.uuid4())
        self[transport.id] = transport

    def remove(self, transport):
        if transport.id in self:
            del self[transport.id]

class Endpoint(Observable):
    def __init__(self, name):
        self.name = name
        self.transports = Transports()
