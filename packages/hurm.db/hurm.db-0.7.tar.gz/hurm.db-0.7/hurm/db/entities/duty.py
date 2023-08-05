# -*- coding: utf-8 -*-
# :Project:   hurm -- Duty class, mapped to table duties
# :Created:   sab 02 gen 2016 15:33:23 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from . import AbstractBase


class Duty(AbstractBase):
    def __init__(self, **kwargs):
        payloads = kwargs.pop('payloads', None)
        if payloads:
            self._update_payloads(payloads)
        super().__init__(**kwargs)

    def update(self, data, **kwargs):
        payloads = data.pop('payloads', None)
        if payloads:
            self._update_payloads(payloads)

        return super().update(data, **kwargs)

    def _update_payloads(self, payloads):
        from .dutypayload import DutyPayload

        for payload in payloads:
            for existing in self.payloads:
                if existing.idactivitypayload == payload['idactivitypayload']:
                    existing.value = payload['value']
                    break
            else:
                self.payloads.append(
                    DutyPayload(idactivitypayload=payload['idactivitypayload'],
                                value=payload['value']))
