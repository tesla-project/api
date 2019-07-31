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
from tesla_models import tep_db, schemas
from tesla_models.helpers import api_response
from tesla_models.errors import TESLA_API_STATUS_CODE
from tesla_models.constants import TESLA_ENROLLMENT_PHASE
from tesla_api import tesla_db
from ..decorators import require_tesla_cert
from ..utils import get_learner_ic_info, get_learner_send_info
import json
api_learners = Blueprint('api_learners', __name__)

tep_sync = True


@api_learners.route('', methods=['POST'])
@require_tesla_cert()
def add_learner():
    """
        .. :quickref: Learners; Add a new learner

        Create a new learner on the system

        :reqheader Authorization: This method requires authentication based on client certificate.

        :<json uuid tesla_id: learner TeSLA ID
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

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, http_code=501)


@api_learners.route('/<uuid:tesla_id>', methods=['GET'])
@require_tesla_cert()
def get_learner(tesla_id):
    """
        .. :quickref: Learners; Get learner information

        Get learner data

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param tesla_id: learner TeSLA ID following RFC4122 v4 standard
        :type tesla_id: uuid

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

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, http_code=501)


@api_learners.route('/<uuid:tesla_id>', methods=['PUT'])
@require_tesla_cert()
def update_learner(tesla_id):
    """
        .. :quickref: Learners; Update learner information

        Update learner data

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param tesla_id: learner TeSLA ID following RFC4122 v4 standard
        :type tesla_id: uuid

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

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, http_code=501)


@api_learners.route('/<uuid:tesla_id>', methods=['DELETE'])
@require_tesla_cert()
def delete_learner(tesla_id):
    """
        .. :quickref: Learners; Delete a learner

        Delete a learner from the system and all their information, including requests, enrolments and results.

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param tesla_id: learner TeSLA ID following RFC4122 v4 standard
        :type tesla_id: uuid

        :<json uuid tesla_id: learner TeSLA ID
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

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, http_code=501)


@api_learners.route('/<uuid:tesla_id>/send', methods=['GET'])
@require_tesla_cert()
def get_learner_send(tesla_id):
    """
        .. :quickref: Learners; Get learner SEND information

        Get learner SEND information

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param tesla_id: learner TeSLA ID following RFC4122 v4 standard
        :type tesla_id: uuid

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
    # Get learner SEND information
    send_info = get_learner_send_info(tesla_id)

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, send_info)


@api_learners.route('/<uuid:tesla_id>/informed-consent', methods=['GET'])
@require_tesla_cert()
def get_learner_ic(tesla_id):
    """
        .. :quickref: Learners; Get learner informed consent information

        Get learner informed consent information

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param tesla_id: learner TeSLA ID following RFC4122 v4 standard
        :type tesla_id: uuid

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

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, http_code=501)


@api_learners.route('/<uuid:tesla_id>/enrolment', methods=['GET'])
@require_tesla_cert()
def get_learner_enrolment(tesla_id):
    """
        .. :quickref: Learners; Get learner enrolment information

        Get learner enrolment information

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param tesla_id: learner TeSLA ID following RFC4122 v4 standard
        :type tesla_id: uuid

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

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, http_code=501)


@api_learners.route('/<uuid:tesla_id>/instruments/<int:instrument_id>/enrolment', methods=['GET'])
@require_tesla_cert()
def get_learner_instrument_enrolment(tesla_id, instrument_id):
    """
        .. :quickref: Learners; Get learner enrolment information for an instrument

        Get learner enrolment information for an instrument

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param tesla_id: learner TeSLA ID following RFC4122 v4 standard
        :type tesla_id: uuid
        :param instrument_id: instrument identifier in TeSLA
        :type tesla_id: int

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
    tesla_id = str(tesla_id)

    # BEGIN: Synchronize data with TEP
    tep_db.sync_learner(tesla_id)
    # END: Synchronize data with TEP

    learner_enrolment = tesla_db.learners.get_learner_enrolment(tesla_id, instrument_id)
    if learner_enrolment is None:
        percentage = 0.0
        completed_enrollments = tesla_db.learners.count_learner_completed_requests(tesla_id, True, instrument_id)
        pending_enrollments = tesla_db.learners.count_learner_pending_requests(tesla_id, True, instrument_id)
        phase = TESLA_ENROLLMENT_PHASE.NOT_STARTED
        if completed_enrollments > 0 or pending_enrollments > 0:
            phase = TESLA_ENROLLMENT_PHASE.ONGOING
    else:
        percentage = learner_enrolment.percentage
        phase = TESLA_ENROLLMENT_PHASE.ONGOING
        if percentage == 1.0:
            phase = TESLA_ENROLLMENT_PHASE.COMPLETED

    pending_requests = tesla_db.learners.get_learner_pending_enrolment_requests(tesla_id, instrument_id)

    response = {
        "enrolment_phase_id": phase,
        "enrolment_completion": percentage,
        "predicted_enrolment_completion": percentage,
        "deferred_enrolments": pending_requests,
        "status_code_source": "TEP",
        "status_code_message": "OK"
    }

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, response)


@api_learners.route('/<uuid:tesla_id>/activities/<int:vle_id>/<string:activity_type>/<string:activity_id>/enrolments', methods=['GET'])
@require_tesla_cert()
def get_learner_activity_enrolments(tesla_id, vle_id, activity_type, activity_id):
    """
        .. :quickref: Learners; Get learner enrolment information for all instruments of an activity

        Get learner enrolment information for all the instruments required in an activity

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param tesla_id: learner TeSLA ID following RFC4122 v4 standard
        :type tesla_id: uuid
        :param vle_id: VLE identifier
        :type vle_id: int
        :param activity_type: type of the activity in the VLE
        :type activity_type: string
        :param activity_id: identifier of the activity in the VLE
        :type activity_id: string

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

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, http_code=501)


@api_learners.route('/<uuid:tesla_id>/activities/<int:vle_id>/<string:activity_type>/<string:activity_id>/instruments', methods=['GET'])
#@require_tesla_cert()
def get_learner_activity_instruments(tesla_id, vle_id, activity_type, activity_id):
    """
        .. :quickref: Learners; Get active instruments in a certain activity for a particular learner

        Get all instruments to activate in a certain activity for a particular learner

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param tesla_id: learner TeSLA ID following RFC4122 v4 standard
        :type tesla_id: uuid
        :param vle_id: VLE identifier
        :type vle_id: int
        :param activity_type: type of the activity in the VLE
        :type activity_type: string
        :param activity_id: identifier of the activity in the VLE
        :type activity_id: string

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

    # Get informed consent information
    ic_info = get_learner_ic_info(tesla_id)

    response = {
        'learner_found': ic_info['learner_found'],
        'agreement_status': ic_info['ic_valid'],
        'instrument_ids': [],
        'send': {}
    }

    if not ic_info['ic_valid']:
        if not ic_info['learner_found']:
            return api_response(TESLA_API_STATUS_CODE.USER_NOT_FOUND, response)
        if ic_info['ic_current_version'] is None:
            return api_response(TESLA_API_STATUS_CODE.INFORMED_CONSENT_NOT_ACCEPTED, response)
        if ic_info['rejected_date'] is not None:
            return api_response(TESLA_API_STATUS_CODE.INFORMED_CONSENT_REJECTED, response)
        return api_response(TESLA_API_STATUS_CODE.INFORMED_CONSENT_OUTDATED, response)

    # BEGIN: Synchronize data with TEP
    act_synch = tep_db.sync_activity(vle_id, activity_id, activity_type)
    # END: Synchronize data with TEP

    # Get the activity
    activity = tesla_db.activities.get_activity_by_def(vle_id, activity_type, activity_id)
    if activity is None:
        return api_response(TESLA_API_STATUS_CODE.ACTIVITY_NOT_FOUND, response)

    # Get the instruments activated for this activity
    act_instruments = tesla_db.activities.get_activity_instruments(activity.id)

    # Get learner SEND information
    send_info = get_learner_send_info(tesla_id)
    response['send'] = send_info['send']

    # Create the list of instruments
    instruments = []
    if act_instruments is not None:
        for inst in act_instruments:
            if send_info['is_send']:
                if inst.instrument_id in send_info['send']['disabled_instruments']:
                    if not inst.required:
                        if inst.alternative_instrument_id is not None and inst.alternative_instrument_id not in \
                                send_info['send']['disabled_instruments']:
                            instruments.append(inst.alternative_instrument_id)
                else:
                    instruments.append(inst.instrument_id)
            else:
                instruments.append(inst.instrument_id)

    # Create the final response
    response = {'learner_found': True,
                'agreement_status': True,
                'instrument_ids': instruments,
                'send': send_info
                }

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, response)


@api_learners.route('/<uuid:tesla_id>/activities/<int:vle_id>/<string:activity_type>/<string:activity_id>/results', methods=['GET'])
@require_tesla_cert()
def get_learner_activity_results(tesla_id, vle_id, activity_type, activity_id):
    """
        .. :quickref: Learners; Get learner summarized results for all instruments used in a certain activity

        Get learner summarized results for all instruments used in a certain activity

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param tesla_id: learner TeSLA ID following RFC4122 v4 standard
        :type tesla_id: uuid
        :param vle_id: VLE identifier
        :type vle_id: int
        :param activity_type: type of the activity in the VLE
        :type activity_type: string
        :param activity_id: identifier of the activity in the VLE
        :type activity_id: string

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

    if tep_sync:
        activity = tep_db.sync_activity(vle_id, activity_id, activity_type)
    else:
        activity = tesla_db.activities.get_activity_by_def(vle_id, activity_type, activity_id)

    if activity is None:
        return api_response(TESLA_API_STATUS_CODE.ACTIVITY_NOT_FOUND, http_code=404)

    learner_results = tesla_db.activities.get_activity_results_by_tesla_id_activity_id(tesla_id, activity.id)

    result = {}
    result['items'] = schemas.RequestResult(many=True).dump(learner_results).data

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, result)


@api_learners.route('/<uuid:tesla_id>/activities/<int:vle_id>/<string:activity_type>/<string:activity_id>/instruments/<int:instrument_id>/results', methods=['GET'])
@require_tesla_cert()
def get_learner_activity_instrument_results(tesla_id, vle_id, activity_type, activity_id, instrument_id):
    """
        .. :quickref: Learners; Get learner results for an instruments in a certain activity

        Get learner results for an instruments in a certain activity

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param tesla_id: learner TeSLA ID following RFC4122 v4 standard
        :type tesla_id: uuid
        :param vle_id: VLE identifier
        :type vle_id: int
        :param activity_type: type of the activity in the VLE
        :type activity_type: string
        :param activity_id: identifier of the activity in the VLE
        :type activity_id: string
        :param instrument_id: identifier of the instrument in TeSLA
        :type activity_id: int


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
    if tep_sync:
        activity = tep_db.sync_activity(vle_id, activity_id, activity_type)
    else:
        activity = tesla_db.activities.get_activity_by_def(vle_id, activity_type, activity_id)

    if activity is None:
        return api_response(TESLA_API_STATUS_CODE.ACTIVITY_NOT_FOUND, http_code=404)

    learner_results = tesla_db.activities.get_activity_results_by_tesla_id_activity_id_instrument_id(tesla_id, activity.id, instrument_id)

    result = {}
    result['items'] = schemas.RequestResult(many=True).dump(learner_results).data

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, result)



@api_learners.route('/<uuid:tesla_id>/activities/<int:vle_id>/<string:activity_type>/<string:activity_id>/instruments/<int:instrument_id>/audit', methods=['GET'])
@require_tesla_cert()
def get_learner_activity_instrument_audit(tesla_id, vle_id, activity_type, activity_id, instrument_id):
    """
        .. :quickref: Learners; Get learner summarized audit for an instrument in a certain activity

        Get learner summarized audit for an instrument in a certain activity

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param tesla_id: learner TeSLA ID following RFC4122 v4 standard
        :type tesla_id: uuid
        :param vle_id: VLE identifier
        :type vle_id: int
        :param activity_type: type of the activity in the VLE
        :type activity_type: string
        :param activity_id: identifier of the activity in the VLE
        :type activity_id: string
        :param instrument_id: identifier of the instrument in TeSLA
        :type activity_id: int

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

    if tep_sync:
        activity = tep_db.sync_activity(vle_id, activity_id, activity_type)
    else:
        activity = tesla_db.activities.get_activity_by_def(vle_id, activity_type, activity_id)

    if activity is None:
        return api_response(TESLA_API_STATUS_CODE.ACTIVITY_NOT_FOUND, http_code=404)

    tesla_id = str(tesla_id)

    # Verify the learner
    learner = tesla_db.learners.get_learner(tesla_id)
    if learner is None:
        return api_response(TESLA_API_STATUS_CODE.LEARNER_NOT_FOUND, http_code=404)

    # Verify the instrument
    instrument = tesla_db.instruments.get_instrument_by_id(instrument_id)
    if instrument is None:
        return api_response(TESLA_API_STATUS_CODE.INSTRUMENT_NOT_FOUND, http_code=404)

    # Check that the instrument have audit possibilities
    if instrument.id not in [1, 6]:
        return api_response(TESLA_API_STATUS_CODE.SUCCESS, http_code=405)

    audit_data = tep_db.get_activity_audit(activity.vle_id, activity.activity_type, activity.activity_id, tesla_id, instrument.id)

    for a in audit_data:
        if a['start'] is not None:
            a['start'] = str(a['start'])
        if a['finish'] is not None:
            a['finish'] = str(a['finish'])
    
    if instrument.id == 1:
        audit_data = _get_fr_audit_data(audit_data)
        if audit_data is None:
            audit_data = {
                'results': {
                    'frame_details': [],
                    'total_frames': 0,
                    'valid_frames': 0,
                    'frame_codes': [],
                    'error_frames': 0
                },
                'enrollment_user_faces': [],
                'version': 'TFR 1.0'
            }
    else:
        aux = audit_data
        audit_data = {}
        audit_data['audit_data'] = aux

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, data=audit_data)


def _get_fr_audit_data(audit_data):
    audit = None

    for a in audit_data:
        if a['finish'] is not None:
            audit = _get_audit_object(a['audit'], audit)

    return audit


def _get_audit_object(audit_string, audit=None):
    audit_obj = json.loads(audit_string)

    if audit is None:
        return audit_obj

    audit['results']['frame_details'] += audit_obj['results']['frame_details']
    audit['results']['total_frames'] += audit_obj['results']['total_frames']
    audit['results']['valid_frames'] += audit_obj['results']['valid_frames']
    audit['results']['frame_codes'] += audit_obj['results']['frame_codes']
    audit['results']['error_frames'] += audit_obj['results']['error_frames']

    return audit


@api_learners.route('/<uuid:tesla_id>/activities/<int:vle_id>/<string:activity_type>/<string:activity_id>/requests/<int:request_id>/instruments/<int:instrument_id>/audit', methods=['GET'])
@require_tesla_cert()
def get_learner_activity_request_instrument_audit(tesla_id, vle_id, activity_type, activity_id, request_id, instrument_id):
    """
        .. :quickref: Learners; Get learner summarized audit for an instrument in a certain activity

        Get learner summarized audit for an instrument in a certain activity

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param tesla_id: learner TeSLA ID following RFC4122 v4 standard
        :type tesla_id: uuid
        :param vle_id: VLE identifier
        :type vle_id: int
        :param activity_type: type of the activity in the VLE
        :type activity_type: string
        :param activity_id: identifier of the activity in the VLE
        :type activity_id: string
        :param request_id: identifier of the instrument in TeSLA
        :type request_id: int
        :param instrument_id: identifier of the instrument in TeSLA
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
            | 53      | Request JSON error. It contains more data or some required fields are missing.               |
            +---------+----------------------------------------------------------------------------------------------+

    """

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, http_code=501)

