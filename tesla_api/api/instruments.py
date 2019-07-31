#  TeSLA API
#  Copyright (C) 2019 Universitat Oberta de Catalunya
# 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
# 
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Blueprint, jsonify
from tesla_models.helpers import api_response
from tesla_models.errors import TESLA_API_STATUS_CODE
from tesla_models import schemas
from tesla_models import tep_db
from tesla_api import logger, tesla_db
from ..decorators import require_tesla_cert

api_instruments = Blueprint('api_instruments', __name__)

tep_sync = True

@api_instruments.route('', methods=['GET'])
@require_tesla_cert()
def get_instruments():
    """
        .. :quickref: Instruments; Get the list of instruments

        Get the list of instruments

        :reqheader Authorization: This method requires authentication based on client certificate.

        :>json int status_code: indicates if the request is correctly processed or some error occurred.
        :>json string error_message: in case of error (status_code > 0) it provide a description of the error

        :status 200: request processed. In this case, check the status_code in order to verify if is correct or not.
        :status 401: authorization denied. There is some problem with the provided certificates
        :status 500: unexpected error processing the request

        **Response Status Codes**
            +---------+----------------------------------------------------------------------------------------------+
            |**Code** | **Description**                                                                              |
            +---------+----------------------------------------------------------------------------------------------+
            | 0       | Success!                                                                                     |
            +---------+----------------------------------------------------------------------------------------------+
            | 6       | Error persisting the data                                                                    |
            +---------+----------------------------------------------------------------------------------------------+
            | 53      | Request JSON error. It contains more data or some required fields are missing.               |
            +---------+----------------------------------------------------------------------------------------------+

    """
    instruments = tesla_db.instruments.get_instruments()

    if instruments is None:
        return api_response(TESLA_API_STATUS_CODE.INSTRUMENT_NOT_FOUND, http_code=404)

    instruments_json = schemas.Instrument(many=True).dump(instruments).data
    response = {}
    response['items'] = instruments_json

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, response)


@api_instruments.route('/<int:instrument_id>/thresholds', methods=['GET'])
@require_tesla_cert()
def get_instrument_thresholds(instrument_id):
    """
        .. :quickref: Instruments; Get thresholds information for an instrument

        Get thresholds information for an instrument

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param instrument_id: linstrument identifier in TeSLA
        :type instrument_id: int

        :<json string public_cert: public certificate for the learner.
        :<json string cert_alg: algorithm used to create the public certificate.

        :>json int status_code: indicates if the request is correctly processed or some error occurred.
        :>json string error_message: in case of error (status_code > 0) it provide a description of the error

        :status 200: request processed. In this case, check the status_code in order to verify if is correct or not.
        :status 401: authorization denied. There is some problem with the provided certificates
        :status 500: unexpected error processing the request

        **Response Status Codes**
            +---------+----------------------------------------------------------------------------------------------+
            |**Code** | **Description**                                                                              |
            +---------+----------------------------------------------------------------------------------------------+
            | 0       | Success!                                                                                     |
            +---------+----------------------------------------------------------------------------------------------+
            | 6       | Error persisting the data                                                                    |
            +---------+----------------------------------------------------------------------------------------------+
            | 14      | Instrument threshold not found.                                                              |
            +---------+----------------------------------------------------------------------------------------------+
            | 53      | Request JSON error. It contains more data or some required fields are missing.               |
            +---------+----------------------------------------------------------------------------------------------+

    """

    if tep_sync is True:
        tep_db.sync_instrument_thresholds()

    threshold = tesla_db.instruments.get_instrument_thresholds(instrument_id)

    if threshold is None:
        return api_response(TESLA_API_STATUS_CODE.INSTRUMENT_THRESHOLD_NOT_FOUND, http_code=404)

    threshold_json = schemas.InstrumentThreshold().dump(threshold).data

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, threshold_json)

