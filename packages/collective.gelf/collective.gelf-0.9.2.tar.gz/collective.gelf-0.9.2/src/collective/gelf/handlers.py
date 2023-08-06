# -*- coding: utf-8 -*-
from pygelf import GelfTcpHandler
from pygelf import GelfTlsHandler
from pygelf import GelfUdpHandler
from ZConfig.components.logger.handlers import HandlerFactory
import logging


def get_options(section):
    options = {}
    for name in section.getSectionAttributes():
        if name not in ['level', 'dateformat', 'formatter', 'custom']:
            options[name] = getattr(section, name)
    options.update(dict([('_' + x.split('=', 1)[0], x.split('=', 1)[-1])
                   for x in section.custom.split() if '=' in x]))
    return options


class GelfTcpHandlerFactory(HandlerFactory):
    def create(self):
        return GelfTcpHandler(**get_options(self.section))


class GelfUdpHandlerFactory(HandlerFactory):
    def create(self):
        return GelfUdpHandler(**get_options(self.section))


class GelfTlsHandlerFactory(HandlerFactory):
    def create(self):
        return GelfTlsHandler(**get_options(self.section))
