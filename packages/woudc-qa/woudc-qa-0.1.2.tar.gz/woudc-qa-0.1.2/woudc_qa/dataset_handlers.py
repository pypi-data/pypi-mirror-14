# =================================================================
#
# Terms and Conditions of Use
#
# Unless otherwise noted, computer program source code of this
# distribution is covered under Crown Copyright, Government of
# Canada, and is distributed under the MIT License.
#
# The Canada wordmark and related graphics associated with this
# distribution are protected under trademark law and copyright law.
# No permission is granted to use them outside the parameters of
# the Government of Canada's corporate identity program. For
# more information, see
# http://www.tbs-sct.gc.ca/fip-pcim/index-eng.asp
#
# Copyright title to all 3rd party software distributed with this
# software is held by the respective copyright holders as noted in
# those files. Users are asked to read the 3rd Party Licenses
# referenced with those assets.
#
# Copyright (c) 2016 Government of Canada
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

# Dataset handlers

import logging
from woudc_qa.util import get_extcsv_value, set_extcsv_value

LOGGER = logging.getLogger(__name__)


class OzoneSondeHandler(object):
    """Handles OzoneSonde files."""

    def __init__(self, extcsv):
        """
        Init OzoneSondeHandler object

        :param extcsv: woudc_extcsv.Reader object
        """

        self._extcsv = extcsv
        # invoke transformation logic
        self.run_all_transformations()

    @property
    def extcsv(self):
        """
        :returns: extcsv object
        """

        return self._extcsv

    @extcsv.setter
    def extcsv(self, extcsv):
        """
        Set extcsv
        """
        self._extcsv = extcsv

    def run_all_transformations(self):
        """
        run transformation and update extcsv in place
        """

        # self.pump_flow_rate_uc()
        # self.response_time_uc()
        # self.pump_temperature_uc()
        self.derive_volume_mixing_ratio()

    def pump_flow_rate_uc(self):
        """
        unit conversion for pump flow rate
        sec/100 ml --> sec/ml
        AUXILIARY_DATA.PumpRate
        """
        try:
            PumpRate = \
                get_extcsv_value(self.extcsv, 'AUXILIARY_DATA', 'PumpRate')
        except Exception as err:
            msg = 'Unable to get AUXILIARY_DATA.PumpRate value. Due to: %s'\
                % str(err)
            LOGGER.error(msg)
            raise err(msg)

        try:
            PumpRate_f = float(PumpRate)
            PumpRate_f_uc = PumpRate_f / 100
        except Exception as err:
            msg = 'Invalid float: %s' % PumpRate
            LOGGER.error(msg)
            raise err(msg)

        if PumpRate_f_uc is not None:
            try:
                self.extcsv = \
                    set_extcsv_value(
                        self.extcsv,
                        'AUXILIARY_DATA',
                        'PumpRate',
                        PumpRate_f_uc
                    )
            except Exception as err:
                msg = 'Unable to set value for \
                AUXILIARY_DATA.PumpRate. Due to: %s' % str(err)
                LOGGER.error(msg)
                raise err(msg)

    def response_time_uc(self):
        """
        unit conversion for response time
        (1/e)(min) --> (1/e)(s)
        PREFLIGHT_SUMMARY.OzoneSondeResponseTime
        """

        try:
            OzoneSondeResponseTime = \
                get_extcsv_value(
                    self.extcsv,
                    'PREFLIGHT_SUMMARY',
                    'OzoneSondeResponseTime'
                )
        except Exception as err:
            msg = \
                'Unable to get PREFLIGHT_SUMMARY.OzoneSondeResponseTime \
                value. Due to: %s' % str(err)
            LOGGER.error(msg)
            raise err(msg)

        try:
            OzoneSondeResponseTime_f = float(OzoneSondeResponseTime)
            OzoneSondeResponseTime_f_uc = OzoneSondeResponseTime_f * 60
        except Exception as err:
            msg = 'Invalid float: %s' % OzoneSondeResponseTime
            LOGGER.error(msg)
            raise err(msg)

        if OzoneSondeResponseTime_f_uc is not None:
            try:
                self.extcsv = \
                    set_extcsv_value(
                        self.extcsv,
                        'PREFLIGHT_SUMMARY',
                        'OzoneSondeResponseTime',
                        OzoneSondeResponseTime_f_uc
                    )
            except Exception as err:
                msg = 'Unable to set value for \
                    PREFLIGHT_SUMMARY.OzoneSondeResponseTime. Due to: %s' \
                    % str(err)
                LOGGER.error(msg)
                raise err(msg)

    def derive_volume_mixing_ratio(self):
        """
        derive and store volume mixing ration:
        Volume mixing ratio of ozone =
        (Partial pressure of ozone *10)/atmospheric pressure (hPa)
        """

        try:
            ppO3 = get_extcsv_value(
                self.extcsv,
                'PROFILE',
                'O3PartialPressure',
                payload=True
            )
        except Exception as err:
            msg = 'Unable to get PROFILE.O3PartialPressure. Due to: %s' %\
                str(err)
            LOGGER.error(msg)
            raise err(msg)

        try:
            pressure = get_extcsv_value(
                self.extcsv,
                'PROFILE',
                'Pressure',
                payload=True
            )
        except Exception as err:
            msg = 'Unable to get PROFILE.Pressure. Due to: %s' %\
                str(err)
            LOGGER.error(msg)
            raise err(msg)

        i = 0
        vmrs = []
        for p in pressure:
            try:
                p_f = float(p)
            except Exception as err:
                msg = 'Unable to float pressure: %s. Due to: %s' %\
                    (p, str(err))
                LOGGER.error(msg)
                continue
            try:
                ppO3_f = float(ppO3[i])
            except Exception as err:
                msg = 'Unable to float ppO3: %s. Due to: %s' %\
                    (ppO3[i], str(err))
                LOGGER.error(msg)
                continue
            try:
                vmr = (ppO3_f * 10) / p_f
            except Exception as err:
                msg = 'Unable to calculate vmr with input, ppO3: %s,\
                    pressure: %s. Due to: %s.' % (ppO3_f, p_f, str(err))
                LOGGER.error(msg)
                vmr = None
            vmrs.append(vmr)
            i += 1

        # add derived values to extcsv
        self.extcsv = \
            set_extcsv_value(
                self.extcsv,
                'PROFILE',
                'derived:VMR',
                vmrs,
                mode='add'
            )


class TotalOzoneHandler(object):
    """Handles TotalOzone files."""

    def __init__(self, extcsv):
        """
        Init TotalOzoneHandler object

        :param extcsv: woudc_extcsv.Reader object
        """

        self._extcsv = extcsv
        # invoke transformation logic
        self.run_all_transformations()

    @property
    def extcsv(self):
        """
        :returns: extcsv object
        """

        return self._extcsv

    @extcsv.setter
    def extcsv(self, extcsv):
        """
        Set extcsv
        """
        self._extcsv = extcsv

    def run_all_transformations(self):
        """
        run transformation and update extcsv in place
        """
