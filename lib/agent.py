#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# checkmk_jetbrains_licensevault - Jetbrains LicenseVault Agent and checks
#
# Copyright (C) 2025  Marius Rieder <marius.rieder@scs.ch>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from typing import Optional, Sequence
import logging
import requests
from functools import cached_property
from json import JSONDecodeError

from cmk.special_agents.v0_unstable.agent_common import (
    CannotRecover,
    SectionWriter,
    special_agent_main,
)
from cmk.special_agents.v0_unstable.argument_parsing import Args, create_default_argument_parser

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGGING = logging.getLogger('agent_jetbrains_licensevault')


class LVAPI:
    def __init__(self, url, key, timeout=None, verify_cert=True):
        self._url = url.rstrip('/')
        self._key = key
        self._verify_cert = verify_cert
        self.timeout = timeout

    @cached_property
    def _cli(self):
        sess = requests.Session()
        sess.headers.update({'Authorization': f"Automation {self._key}"})
        return sess

    def request(self, method, ressource, **kwargs):
        url = f"{self._url}/{ressource}"
        LOGGING.debug(f">> {method} {url}")
        try:
            resp = self._cli.request(method, url, verify=self._verify_cert, timeout=self.timeout, **kwargs)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as exc:
            if exc.response.status_code == 401:
                raise CannotRecover(f"Could not authenticate to {url}. Key or secret is incorrect.") from exc
            if exc.response.status_code == 403:
                raise CannotRecover(f"Not permited to access {url}.") from exc
            raise CannotRecover(f"Request error {exc.response.status_code} when trying to {method} {url}") from exc
        except requests.exceptions.ReadTimeout as exc:
            raise CannotRecover(f"Read timeout after {self.timeout}s when trying to {method} {url}") from exc
        except requests.exceptions.ConnectionError as exc:
            raise CannotRecover(f"Could not {method} {url} ({exc})") from exc
        except JSONDecodeError as exc:
            raise CannotRecover(f"Couldn't parse JSON at {url}") from exc


class AgentLicenseVault:
    '''Checkmk special Agent for JetBrains LicenseVault'''

    def run(self, args=None):
        return special_agent_main(self.parse_arguments, self.main, args)

    def parse_arguments(self, argv: Optional[Sequence[str]]) -> Args:
        parser = create_default_argument_parser(description=self.__doc__)

        parser.add_argument('-U', '--url',
                            dest='url',
                            required=True,
                            help='Base-URL of the License Vault api. (ex: https://example.lv.etbrains-ide-services.com/)')
        parser.add_argument('-k', '--key',
                            dest='key',
                            required=True,
                            help='Automation Key.')
        parser.add_argument('-t', '--timeout',
                            dest='timeout',
                            type=int,
                            required=False,
                            default=10,
                            help='HTTP connection timeout. (Default: 10)')
        parser.add_argument('--ignore-cert',
                            dest='verify_cert',
                            action='store_false',
                            help='Do not verify the SSL cert from the REST andpoint.')

        return parser.parse_args(argv)

    @cached_property
    def api(self):
        return LVAPI(self.args.url, self.args.key, timeout=self.args.timeout, verify_cert=self.args.verify_cert)

    def main(self, args: Args):
        self.args = args
        with SectionWriter('jetbrains_licensevault') as section:
            section.append_json(self.api.request('GET', 'public-api/licenses/usage'))
