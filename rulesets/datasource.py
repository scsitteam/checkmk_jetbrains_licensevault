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

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    migrate_to_password,
    Password,
    SingleChoice,
    SingleChoiceElement,
    String,
    validators,
)
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _form_special_agents_jetbrains_licensevault() -> Dictionary:
    return Dictionary(
        title=Title('JetBrains LicenseVault Agent'),
        elements={
            'url': DictElement(
                parameter_form=String(
                    title=Title('URL of the JetBrains LicenseVault API, e.g. https://example.lv.etbrains-ide-services.com/'),
                    custom_validate=(
                        validators.Url(
                            [validators.UrlProtocol.HTTP, validators.UrlProtocol.HTTPS],
                        ),
                    ),
                    macro_support=True,
                ),
                required=True,
            ),
            'key': DictElement(
                parameter_form=Password(
                    title=Title('jetBrains IDE-Services Automation key.'),
                    migrate=migrate_to_password
                ),
                required=True,
            ),
            'ignore_cert': DictElement(
                parameter_form=SingleChoice(
                    title=Title('SSL certificate checking'),
                    elements=[
                        SingleChoiceElement(name='ignore_cert', title=Title('Ignore Cert')),
                        SingleChoiceElement(name='check_cert', title=Title('Check Cert')),
                    ],
                    prefill=DefaultValue('check_cert'),
                ),
                required=True,
            ),
        },
    )


rule_spec_jetbrains_licensevault_datasource = SpecialAgent(
    name="jetbrains_licensevault",
    title=Title('JetBrains LicenseVault Agent'),
    help_text=Help(
        'This rule selects the JetBrains LicenseVault agent. '
        'You can configure your connection settings here.'
    ),
    topic=Topic.APPLICATIONS,
    parameter_form=_form_special_agents_jetbrains_licensevault,
)
