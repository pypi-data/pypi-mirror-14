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
# along with pyrocumulus. If not, see <http://www.gnu.org/licenses/>.

from tornado import gen
from tornado.web import HTTPError
from pyrocumulus.auth import AccessToken


class AuthMixin:
    @gen.coroutine
    def prepare(self):
        """ Verifies if the token has enougth perms. If it has,
        continues normal super() preprare
        """
        self.token = self._get_token()
        yield self.check_perms(self.token)
        ret = yield super().prepare()
        del self.params['api_key']
        return ret

    @gen.coroutine
    def check_perms(self, token):
        """ Check token's permissions on self.model
        """
        needed_perms = {'get': 'r', 'put': 'w', 'delete': 'w', 'post': 'w'}

        try:
            access_token = yield AccessToken.get_by_token(token)
        except AccessToken.DoesNotExist:
            raise HTTPError(401, 'bad api_key')

        uri = self.request.headers.get('Referer', '')
        domain = self._get_domain(uri)
        reqmethod = self.request.method.lower()

        if reqmethod == 'options':
            return

        needed_perm = needed_perms[reqmethod]
        domains = access_token.domains
        has_domain_permission = not (not domain in domains
                                     and domains.count(domains) > 0)

        perms = yield access_token.get_perms(self.model)
        # :/
        if 'rw' in perms:
            if not 'r' in perms:
                perms.add('r')
            if not 'w' in perms:
                perms.add('w')

        if not needed_perm in perms or not has_domain_permission:
            raise HTTPError(401)

    def _get_token(self):
        try:
            token = self.request.arguments.get('api_key', [])[0]
        except IndexError:
            raise HTTPError(500, 'api_key param is required')

        token = token.decode()
        return token

    def _get_domain(self, uri):
        if not uri.startswith('http'):
            return uri

        try:
            domain = uri.split('http://')[1].split('/')[0]
        except IndexError:
            domain = uri.split('https://')[1].split('/')[0]

        return domain


class ReadOnlyMixin:
    def post(self, operation):
        raise HTTPError(405)

    def put(self, operation):
        raise HTTPError(405)

    def delete(self, operation):
        raise HTTPError(405)
