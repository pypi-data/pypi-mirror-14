# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.registry import RegistryManager
from .controllers import PyramidException
from anyblok_pyramid import set_callable, get_callable
from .anyblok import AnyBlokZopeTransactionExtension


class HandlerException(PyramidException):
    """ Simple exception for handler """


@set_callable
def get_registry(request):
    settings = {
        'sa.session.extension': AnyBlokZopeTransactionExtension,
    }
    return RegistryManager.get(request.session['database'], **settings)


class Handler:
    """ Base class for all the pyramid handler. """

    def init_controller(self, request):
        """ Get an instance of the controller

        :param request: http request get from pyramid
        :rtype: instance of Pyramid controller
        :exception: HandlerException
        """
        registry = get_callable('get_registry')(request)
        registry.System.Cache.clear_invalidate_cache()
        if self.namespace not in registry.loaded_controllers:
            raise HandlerException(
                "Unknow controller %r" % self.namespace)

        self.controller = registry.loaded_controllers[self.namespace](
            request)

    def call_controller(self, *args, **kwargs):
        """ call the controller function and return the result """
        return getattr(self.controller, self.function)(*args, **kwargs)


class HandlerHTTP(Handler):
    """ Handler for all PyramidHTTP controllers """

    def __init__(self, namespace, view):
        """ Initialize the handler

        :param namespace: registry nae of the controller
        :param view: route name of the view
        """
        self.namespace = namespace
        self.view = view

    def wrap_view(self, request):
        """ Call and return the result of wanted controller

        :param request: http request got from pyramid
        """
        self.init_controller(request)

        args = []
        kwargs = {}
        if request.method in ('POST', 'PUT', 'DELETE'):
            kwargs.update(dict(request.params))
        else:
            args.extend(list(request.params))

        self.function = self.controller.get_function_from_view(self.view)
        return self.call_controller(*args, **kwargs)


class HandlerRPC(Handler):
    """ Handler for all PyramidRPC controllers """

    def __init__(self, namespace, method):
        """ Initialize the handler

        :param namespace: registry nae of the controller
        :param method: rpc method name of the controller
        """
        self.namespace = namespace
        self.method = method

    def wrap_view(self, request, *args, **kwargs):
        """ Call and return the result of wanted controller

        :param request: http request got from pyramid
        :param \*args: list of argument for rpc method
        :param \*\*kwargs: list of positional argument for rpc method
        """
        self.init_controller(request)
        self.function = self.controller.get_function_from_method(self.method)
        return self.call_controller(*args, **kwargs)
