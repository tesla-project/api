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
from tesla_models import tep_db
import tesla_models.schemas as schemas
import tesla_models.validators as validators
from tesla_models.helpers import api_response
from tesla_models.errors import TESLA_API_STATUS_CODE
from tesla_api import logger, tesla_db, utils
from ..decorators import require_tesla_cert
from tesla_models.database.utils import ResultsPagination

api_activities = Blueprint('api_activities', __name__)

tep_sync = True

@api_activities.route('', methods=['POST'])
@require_tesla_cert()
def add_activity():
    """
        .. :quickref: Activities; Add a new activity

        Create a new activity on the system

        :reqheader Authorization: This method requires authentication based on client certificate.

        :<json int vle_id: VLE identifier in TeSLA
        :<json string activity_type: type of the activity in the VLE
        :<json string activity_id: identifier of the activity in the VLE
        :<json string description: description for the activity
        :<json JSON conf: JSON object configuration options for the activity

        :>json int status_code: indicates if the request is correctly processed or some error occurred.
        :>json string error_message: in case of error (status_code > 0) it provide a description of the error
        :>json int vle_id: VLE identifier in TeSLA
        :>json string activity_type: type of the activity in the VLE
        :>json string activity_id: identifier of the activity in the VLE
        :>json string description: description for the activity
        :>json JSON conf: JSON object configuration options for the activity


        :status 200: request processed. In this case, check the status_code in order to verify if is correct or not.
        :status 400: bad request. In this case, the request data is invalid.
        :status 401: authorization denied. There is some problem with the provided certificates
        :status 500: unexpected error processing the request

        **Response Status Codes**
            +---------+----------------------------------------------------------------------------------------------+
            |**Code** | **Description**                                                                              |
            +---------+----------------------------------------------------------------------------------------------+
            | 0       | Success!                                                                                     |
            +---------+----------------------------------------------------------------------------------------------+
            | 6       | Error persisting the data.                                                                   |
            +---------+----------------------------------------------------------------------------------------------+
            | 13      | The activity already exists.                                                                 |
            +---------+----------------------------------------------------------------------------------------------+
            | 53      | Request JSON error. It contains more data or some required fields are missing.               |
            +---------+----------------------------------------------------------------------------------------------+

    """

    valid, data, errors = validators.validate(schemas.Activity(), request)

    if not valid:
        return api_response(TESLA_API_STATUS_CODE.INVALID_JSON, errors, http_code=400)

    if tep_sync:
        activity = tep_db.sync_activity(data.vle_id, data.activity_id, data.activity_type)
    else:
        activity = tesla_db.activities.get_activity_by_def(data.vle_id, data.activity_type, data.activity_id)

    if activity is not None:
        act_json = schemas.Activity().dump(activity).data
        return api_response(TESLA_API_STATUS_CODE.DUPLICATED_ACTIVITY, act_json, http_code=400)

    if tep_sync:
        activity = tep_db.create_activity(data.vle_id, data.activity_id, data.activity_type)
        if not tesla_db.activities.update_activity_config(activity.id, data.conf):
            return api_response(TESLA_API_STATUS_CODE.ERROR_PERSISTING_DATA, http_code=400)
        if not tesla_db.activities.update_activity_description(activity.id, data.description):
            return api_response(TESLA_API_STATUS_CODE.ERROR_PERSISTING_DATA, http_code=400)
    else:
        activity = tesla_db.activities.create_activity(data.vle_id, data.activity_type, data.activity_id, data.conf, data.description)

    if activity is None:
        return api_response(TESLA_API_STATUS_CODE.ERROR_PERSISTING_DATA, http_code=400)

    activity = tesla_db.activities.get_activity(activity.id)
    act_json = schemas.Activity().dump(activity).data

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, act_json)


@api_activities.route('/<int:vle_id>/<string:activity_type>/<string:activity_id>', methods=['GET'])
@require_tesla_cert()
def get_activity(vle_id, activity_type, activity_id):
    """
        .. :quickref: Activities; Get activity information

        Get activity data

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param vle_id: VLE identifier
        :type vle_id: int
        :param activity_type: type of the activity in the VLE
        :type activity_type: string
        :param activity_id: identifier of the activity in the VLE
        :type activity_id: string

        :>json int status_code: indicates if the request is correctly processed or some error occurred.
        :>json string error_message: in case of error (status_code > 0) it provide a description of the error
        :>json int vle_id: VLE identifier in TeSLA
        :>json string activity_type: type of the activity in the VLE
        :>json string activity_id: identifier of the activity in the VLE
        :>json string description: description for the activity
        :>json JSON conf: JSON object configuration options for the activity
        :>json boolean tesla_active: this parameter is true if this activity has some TeSLA instrument active

        :status 200: request processed. In this case, check the status_code in order to verify if is correct or not.
        :status 400: some controlled error occurred during request processing.
        :status 401: authorization denied. There is some problem with the provided certificates
        :status 404: activity not found.
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

    if tep_sync:
        activity = tep_db.sync_activity(vle_id, activity_id, activity_type)
    else:
        activity = tesla_db.activities.get_activity_by_def(vle_id, activity_type, activity_id)

    if activity is None:
        return api_response(TESLA_API_STATUS_CODE.ACTIVITY_NOT_FOUND, http_code=404)

    act_json = schemas.Activity().dump(activity).data
    act_json['tesla_active'] = False

    act_instruments = tesla_db.activities.get_activity_all_instruments(activity.id)

    for instrument in act_instruments:
        if instrument.active is True:
            act_json['tesla_active'] = True
            break

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, act_json)


@api_activities.route('/<int:vle_id>/<string:activity_type>/<string:activity_id>', methods=['PUT'])
@require_tesla_cert()
def update_activity(vle_id, activity_type, activity_id):
    """
        .. :quickref: Activities; Update activity information

        Update activity data

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param vle_id: VLE identifier
        :type vle_id: int
        :param activity_type: type of the activity in the VLE
        :type activity_type: string
        :param activity_id: identifier of the activity in the VLE
        :type activity_id: string

        :<json string description: description for the activity
        :<json JSON conf: JSON object configuration options for the activity

        :>json int status_code: indicates if the request is correctly processed or some error occurred.
        :>json string error_message: in case of error (status_code > 0) it provide a description of the error
        :>json int vle_id: VLE identifier in TeSLA
        :>json string activity_type: type of the activity in the VLE
        :>json string activity_id: identifier of the activity in the VLE
        :>json string description: description for the activity
        :>json JSON conf: JSON object configuration options for the activity

        :status 200: request processed. In this case, check the status_code in order to verify if is correct or not.
        :status 400: some controlled error occurred during request processing.
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

    valid, data, errors = validators.validate(schemas.Activity(), request, partial=True)

    if not valid:
        return api_response(TESLA_API_STATUS_CODE.INVALID_JSON, errors, http_code=400)

    if tep_sync:
        activity = tep_db.sync_activity(vle_id, activity_id, activity_type)
    else:
        activity = tesla_db.activities.get_activity_by_def(vle_id, activity_type, activity_id)

    if activity is None:
        return api_response(TESLA_API_STATUS_CODE.ACTIVITY_NOT_FOUND, http_code=404)

    # Modify provided fields
    if 'conf' in request.get_json():
        if not tesla_db.activities.update_activity_config(activity.id, data.conf):
            return api_response(TESLA_API_STATUS_CODE.ERROR_PERSISTING_DATA, http_code=400)
    if 'description' in request.get_json():
        if not tesla_db.activities.update_activity_description(activity.id, data.description):
            return api_response(TESLA_API_STATUS_CODE.ERROR_PERSISTING_DATA, http_code=400)

    activity = tesla_db.activities.get_activity(activity.id)
    act_json = schemas.Activity().dump(activity).data
    return api_response(TESLA_API_STATUS_CODE.SUCCESS, act_json)


@api_activities.route('/<int:vle_id>/<string:activity_type>/<string:activity_id>', methods=['DELETE'])
@require_tesla_cert()
def delete_activity(vle_id, activity_type, activity_id):
    """
        .. :quickref: Activities; Delete an activity

        Delete an activity from the system and all their related requests and results.

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param vle_id: VLE identifier
        :type vle_id: int
        :param activity_type: type of the activity in the VLE
        :type activity_type: string
        :param activity_id: identifier of the activity in the VLE
        :type activity_id: string

        :>json int status_code: indicates if the request is correctly processed or some error occurred.
        :>json string error_message: in case of error (status_code > 0) it provide a description of the error

        :status 200: request processed. In this case, check the status_code in order to verify if is correct or not.
        :status 401: authorization denied. There is some problem with the provided certificates
        :status 404: activity not found.
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

    if tep_sync:
        activity = tep_db.sync_activity(vle_id, activity_id, activity_type)
    else:
        activity = tesla_db.activities.get_activity_by_def(vle_id, activity_type, activity_id)

    if activity is None:
        return api_response(TESLA_API_STATUS_CODE.ACTIVITY_NOT_FOUND, http_code=404)

    # TODO: Delete activity data
    if tep_sync:
        pass
    else:
        tesla_db.activities.delete_activity(activity.id)

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, http_code=501)


@api_activities.route('/<int:vle_id>/<string:activity_type>/<string:activity_id>/instruments', methods=['GET'])
@require_tesla_cert()
def get_activity_instruments(vle_id, activity_type, activity_id):
    """
        .. :quickref: Activities; Get activity instruments

        Return the list of instruments used in this activity. The list will contain all the instruments, including
        the alternative instruments.

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param vle_id: VLE identifier
        :type vle_id: int
        :param activity_type: type of the activity in the VLE
        :type activity_type: string
        :param activity_id: identifier of the activity in the VLE
        :type activity_id: string

        :>json int status_code: indicates if the request is correctly processed or some error occurred.
        :>json string error_message: in case of error (status_code > 0) it provide a description of the error
        :>json list instruments: list of active instruments for this activity

        :status 200: request processed. In this case, check the status_code in order to verify if is correct or not.
        :status 401: authorization denied. There is some problem with the provided certificates
        :status 404: activity not found.
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

    if tep_sync:
        activity = tep_db.sync_activity(vle_id, activity_id, activity_type)
    else:
        activity = tesla_db.activities.get_activity_by_def(vle_id, activity_type, activity_id)

    if activity is None:
        return api_response(TESLA_API_STATUS_CODE.ACTIVITY_NOT_FOUND, http_code=404)

    act_instruments = tesla_db.activities.get_activity_all_instruments(activity.id)

    instruments_json = schemas.ActivityInstrument(many=True).dump(act_instruments).data

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, {"instruments" : instruments_json})


@api_activities.route('/<int:vle_id>/<string:activity_type>/<string:activity_id>/instruments', methods=['POST'])
#@require_tesla_cert()
def set_activity_instruments(vle_id, activity_type, activity_id):
    """
        .. :quickref: Activities; Set activity instruments

        Set the list of instruments to be activated in a certain activity

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param vle_id: VLE identifier
        :type vle_id: int
        :param activity_type: type of the activity in the VLE
        :type activity_type: string
        :param activity_id: identifier of the activity in the VLE
        :type activity_id: string

        :<json list: list of instrument options in JSON format

        :>json int status_code: indicates if the request is correctly processed or some error occurred.
        :>json string error_message: in case of error (status_code > 0) it provide a description of the error
        :>json list instruments: list of active instruments for this activity

        :status 200: request processed. In this case, check the status_code in order to verify if is correct or not.
        :status 400: some controlled error occurred during request processing.
        :status 401: authorization denied. There is some problem with the provided certificates
        :status 404: activity not found.
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

    valid, data, errors = validators.validate(schemas.ActivityInstrument(many=True), request)

    if not valid:
        return api_response(TESLA_API_STATUS_CODE.INVALID_JSON, errors, http_code=400)

    if tep_sync:
        activity = tep_db.sync_activity(vle_id, activity_id, activity_type, data)
    else:
        activity = tesla_db.activities.get_activity_by_def(vle_id, activity_type, activity_id)

    if activity is None:
        return api_response(TESLA_API_STATUS_CODE.ACTIVITY_NOT_FOUND, http_code=404)

    if not tesla_db.activities.update_activity_instrument_config(activity.id, data):
        return api_response(TESLA_API_STATUS_CODE.ERROR_PERSISTING_DATA, http_code=400)

    act_instruments = tesla_db.activities.get_activity_all_instruments(activity.id)



    instruments_json = schemas.ActivityInstrument(many=True).dump(act_instruments).data

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, {"instruments": instruments_json})


@api_activities.route('/<int:vle_id>/<string:activity_type>/<string:activity_id>/learners', methods=['GET'])
@require_tesla_cert()
def get_activity_learners(vle_id, activity_type, activity_id):
    """
        .. :quickref: Activities; Get activity learners

        Get the list of learners of an activity

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param vle_id: VLE identifier
        :type vle_id: int
        :param activity_type: type of the activity in the VLE
        :type activity_type: string
        :param activity_id: identifier of the activity in the VLE
        :type activity_id: string

        :<json uuid tesla_id: learner TeSLA ID
        :<json string public_cert: public certificate for the learner.
        :<json string cert_alg: algorithm used to create the public certificate.

        :>json int status_code: indicates if the request is correctly processed or some error occurred.
        :>json string error_message: in case of error (status_code > 0) it provide a description of the error

        :status 200: request processed. In this case, check the status_code in order to verify if is correct or not.
        :status 401: authorization denied. There is some problem with the provided certificates
        :status 404: activity not found.
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

    if tep_sync:
        activity = tep_db.sync_activity(vle_id, activity_id, activity_type)
    else:
        activity = tesla_db.activities.get_activity_by_def(vle_id, activity_type, activity_id)

    if activity is None:
        return api_response(TESLA_API_STATUS_CODE.ACTIVITY_NOT_FOUND, http_code=404)




    return api_response(TESLA_API_STATUS_CODE.SUCCESS, http_code=501)


@api_activities.route('/<int:vle_id>/<string:activity_type>/<string:activity_id>/results', methods=['GET'])
@require_tesla_cert()
def get_activity_results(vle_id, activity_type, activity_id):
    """
        .. :quickref: Activities; Get activity results for all learners and instruments

        Get activity results for all learners and instruments

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param vle_id: VLE identifier
        :type vle_id: int
        :param activity_type: type of the activity in the VLE
        :type activity_type: string
        :param activity_id: identifier of the activity in the VLE
        :type activity_id: string

        :<json uuid tesla_id: learner TeSLA ID
        :<json string public_cert: public certificate for the learner.
        :<json string cert_alg: algorithm used to create the public certificate.

        :>json int status_code: indicates if the request is correctly processed or some error occurred.
        :>json string error_message: in case of error (status_code > 0) it provide a description of the error

        :status 200: request processed. In this case, check the status_code in order to verify if is correct or not.
        :status 401: authorization denied. There is some problem with the provided certificates
        :status 404: activity not found.
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

    if tep_sync:
        activity = tep_db.sync_activity(vle_id, activity_id, activity_type)
    else:
        activity = tesla_db.activities.get_activity_by_def(vle_id, activity_type, activity_id)

    if activity is None:
        return api_response(TESLA_API_STATUS_CODE.ACTIVITY_NOT_FOUND, http_code=404)

    learners = tesla_db.activities.get_activity_learners_with_results(activity.id, pagination=ResultsPagination(request))
    results = schemas.ActivitySummaryPagination().dump(learners).data
    for learner_result in results['items']:
        tesla_id = learner_result['tesla_id']
        summary = tesla_db.activities.get_activity_learner_summary(activity.id, tesla_id)
        summary_json = schemas.InstrumentResultsSummary(many=True).dump(summary).data
        learner_result.update({"instruments": summary_json})

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, results)


