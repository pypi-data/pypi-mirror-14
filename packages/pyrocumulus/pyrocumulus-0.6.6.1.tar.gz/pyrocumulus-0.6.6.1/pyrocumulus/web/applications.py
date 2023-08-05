# -*- coding: utf-8 -*-

# Copyright 2013-2015 Juca Crispim <juca@poraodojuca.net>

# This file is part of pyrocumulus.

# pyrocumulus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pyrocumulus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pyrocumulus.  If not, see <http://www.gnu.org/licenses/>.

from importlib import import_module
from tornado.web import Application as TornadoApplication
from tornado.web import URLSpec
from pyrocumulus.conf import settings
from pyrocumulus.utils import fqualname
from pyrocumulus.web.urlmappers import DocumentURLMapper
from pyrocumulus.web.handlers import get_rest_handler
from pyrocumulus.web.handlers import StaticFileHandler


class Application:
    def __init__(self, *models, url_prefix, auth=False, readonly=False,
                 handlerfactory=None, extra_urls=[]):
        self.models = models
        self.handlerfactory = handlerfactory or get_rest_handler
        self.url_prefix = url_prefix
        self.extra_urls = extra_urls
        self.auth = auth
        self.readonly = readonly

        self._handlers_map = self._get_handlers_map()

        self.tornado_app = None
        self.tornado_opts = getattr(settings, 'TORNADO_OPTS', {})

    @property
    def urls(self):
        """
        Returns all the url, including the extra urls passed in the
        constructor
        """
        urls = self.get_urls()
        urls += self.extra_urls
        return urls

    def get_urls(self):
        """
        Returns the urls without the extra ones.
        """
        urls = []
        for document in self.models:
            request_handler = self._handlers_map[fqualname(document)]
            mapper = DocumentURLMapper(document, request_handler,
                                       self.url_prefix)
            urls += mapper.get_urls()
        return urls

    def listen(self, *args, **kwargs):
        urls = self.urls
        if not self.tornado_app:
            self.tornado_app = TornadoApplication(urls, **self.tornado_opts)
            self.tornado_app.urls = urls
        return self.tornado_app.listen(*args, **kwargs)

    def _get_handlers_map(self):
        handlers_map = {}

        for model in self.models:
            key = fqualname(model)
            value = self.handlerfactory(model, auth=self.auth,
                                        readonly=self.readonly)
            handlers_map[key] = value
        return handlers_map


class RestApplication(Application):
    def __init__(self, *models, url_prefix='/api', auth=False,
                 readonly=False):
        super(RestApplication, self).__init__(*models, url_prefix=url_prefix,
                                              auth=auth, readonly=readonly,
                                              handlerfactory=get_rest_handler)


class StaticApplication(Application):
    def __init__(self):

        static_url = URLSpec(settings.STATIC_URL + '(.*)', StaticFileHandler,
                             dict(static_dirs=settings.STATIC_DIRS))

        super(StaticApplication, self).__init__(url_prefix='',
                                                handlerfactory=lambda: None,
                                                extra_urls=[static_url])


def get_main_application():
    """
    Returns an Application instance to be used as the main one.
    It uses all applications listed in the APPLICATIONS settings
    variable.

    Using the urls of these applications, creates a new
    `tornado.web.application.Application`
    instance with all urls foundd in the applications.
    """
    urls = []
    for app in settings.APPLICATIONS:
        urls += _get_application_urls(app)

    tornado_opts = getattr(settings, 'TORNADO_OPTS', {})
    main_app = TornadoApplication(urls, tornado_opts)
    # ouch!
    main_app.urls = urls
    return main_app


def _get_application_urls(app_name):
    """
    Returns a list of urls to a given application name.
    It must be a fully qualified name for the application.
    """
    module_name, app_name = app_name.rsplit('.', 1)
    urls = []
    try:
        module = import_module(module_name)
        application = getattr(module, app_name)
        if application:
            urls += application.urls
    except ImportError:
        pass

    return urls
