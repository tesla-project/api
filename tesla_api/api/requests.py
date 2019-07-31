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

from flask import Blueprint, jsonify, request
from tesla_models.helpers import api_response
from tesla_models.errors import TESLA_API_STATUS_CODE
from tesla_api import logger, tesla_db
from tesla_models import tesla_storage, validators
from ..decorators import require_tesla_cert

api_requests = Blueprint('api_requests', __name__)


@api_requests.route('/<int:request_id>', methods=['GET'])
@require_tesla_cert()
def get_request(request_id):
    """
        .. :quickref: Requests; Get request data

        Get request data

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param request_id: request information
        :type request_id: int

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
            | 53      | Request JSON error. It contains more data or some required fields are missing.               |
            +---------+----------------------------------------------------------------------------------------------+

    """

    logger.debug("GET REQUEST {}".format(request_id))

    request = tesla_db.requests.get_request(request_id)

    if request is None:
        return api_response(TESLA_API_STATUS_CODE.REQUEST_NOT_FOUND)

    activity = None
    if request.activity_id is not None:
        activity = tesla_db.activities.get_activity(request.activity_id)

    request_data = tesla_storage.load_request_data(request_id)

    data = {
        "request_id": request.id,
        "tesla_id": request.tesla_id,
        "is_enrollment": request.is_enrolment,
        "data": request_data
    }

    if activity is not None:
        data["activity"] = {
            "vle_id": activity.vle_id,
            "activity_id": activity.activity_id,
            "activity_type": activity.activity_type
        }

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, data=data)


@api_requests.route('/<int:request_id>/instruments/<int:instrument_id>/status', methods=['POST'])
@require_tesla_cert(allowed_modules='INSTRUMENT', inject_module=True)
def update_request_instrument_status(request_id, instrument_id, module = None):
    """
        .. :quickref: Requests; Update request status for an instrument

        Update the value of the status and progress for the evaluation of a request by an instrument

        :reqheader Authorization: This method requires authentication based on client certificate. A valid certificate from Instrument must be provided.

        :param request_id: request identifier
        :type tesla_id: int
        :param instrument_id: instrument identifier
        :type instrument_id: int

        :<json float progress: evaluation progress percentage between 0 and 1
        :<json int status: evaluation status, where 0 is not stared, 1 is in progress, 2 finished and 3 failed.

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

    valid, valid_data, errors = validators.validate_request_status_update(request)
    if not valid:
        logger.error('Invalid JSON on [POST] /request/{}/{}/status: {}'.format(request_id, instrument_id, errors))
        return api_response(TESLA_API_STATUS_CODE.INVALID_JSON, data={'error_message': errors})

    progress = valid_data.get('progress')
    status = valid_data.get('status')

    if not tesla_db.requests.update_request_result_status(request_id, instrument_id, progress, status):
        logger.error('Error persisting request status for request={}, instrument={}, status={}, progress={}'.format(request_id,
                                                                                        instrument_id, status, progress))
        return api_response(TESLA_API_STATUS_CODE.ERROR_PERSISTING_DATA)

    return api_response(TESLA_API_STATUS_CODE.SUCCESS)


@api_requests.route('<int:request_id>/audit', methods=['POST'])
@require_tesla_cert(allowed_modules='INSTRUMENT', inject_module=True)
def update_request_audit(request_id, module = None):
    """
        .. :quickref: Requests; Update request audit_data for an instrument

        Update the value of the audit_data for the evaluation of a request by an instrument

        :reqheader Authorization: This method requires authentication based on client certificate.
            A valid certificate from Instrument must be provided.

        :param request_id: request identifier
        :type tesla_id: int
        :param instrument_id: instrument identifier
        :type instrument_id: int

        :<json audit_data progress: audit_data object

        :>json int status_code: indicates if the request is correctly processed or some error occurred.
        :>json string error_message: in case of error (status_code > 0) it provide a description of the error

        :status 200: request processed. In this case, check the status_code in order to verify if is correct or not.
        :status 401: authorization denied. There is some problem with the provided certificates
        :status 500: unexpected error processing the request

        **Response Status Codes**
            +---------+-------------------------------------------------------------------------------------------+
            |**Code** | **Description**                                                                           |
            +---------+-------------------------------------------------------------------------------------------+
            | 0       | Success!                                                                                  |
            +---------+-------------------------------------------------------------------------------------------+
            | 6       | Error persisting the data                                                                 |
            +---------+-------------------------------------------------------------------------------------------+
            | 53      | Request JSON error. It contains more data or some required fields are missing.            |
            +---------+-------------------------------------------------------------------------------------------+

    """

    valid, valid_data, errors = validators.validate_request_audit_update(request)
    if not valid:
        logger.error('Invalid JSON on [POST] /request/{}/status: {}'.format(request_id, errors))
        return api_response(TESLA_API_STATUS_CODE.INVALID_JSON, data={'error_message': errors})

    # Get the instrument ID from certificate module
    instrument_id = None
    if module is not None and module['is_instrument']:
        instrument_id = module['instrument']['id']

    ret_val = tesla_storage.save_request_audit_data(request_id=request_id, instrument_id=instrument_id,
                                         with_enrolment=valid_data['include_enrolment'],
                                         with_request=valid_data['include_request'],
                                         data=valid_data['audit_data'])

    if ret_val == 0:
        return api_response(TESLA_API_STATUS_CODE.SUCCESS)
    else:
        return api_response(TESLA_API_STATUS_CODE.ERROR_PERSISTING_DATA)


