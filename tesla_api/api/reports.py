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
from tesla_models.database.utils import ReportsPagination
from datetime import timedelta
import math

api_reports = Blueprint('api_reports', __name__)

@api_reports.route('/<int:vle_id>/<string:activity_type>/<string:activity_id>', methods=['GET'])
@api_reports.route('/<int:vle_id>/<string:activity_type>/<string:activity_id>/<int:page>', methods=['GET'])
@require_tesla_cert()
def get_activity_report(vle_id, activity_type, activity_id, page = 1):
    """
        .. :quickref: Reports; Get report from an activity for all learners and instruments

        Get report of an activity results for all learners and instruments

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param vle_id: VLE identifier
        :type vle_id: int
        :param activity_type: type of the activity in the VLE
        :type activity_type: string
        :param activity_id: identifier of the activity in the VLE
        :type activity_id: string
        :param page: number of page
        :type page: integer
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
    '''
    activity = tesla_db.activities.get_activity_by_def(vle_id, activity_type, activity_id)

    if activity is None:
        return api_response(TESLA_API_STATUS_CODE.ACTIVITY_NOT_FOUND, http_code=404)

    reports = tesla_db.report.get_reports(activity.id, pagination=ReportsPagination(request))
    results = schemas.ResultViewActivityPagination().dump(reports).data

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, results)
    '''
    # Verify the activity
    activity = tesla_db.activities.get_activity_by_def(vle_id, activity_type, activity_id)
    if activity is None:
        return api_response(TESLA_API_STATUS_CODE.ACTIVITY_NOT_FOUND, http_code=404)

    # Get filter parameters from request query parameters
    max_per_page = 20
    instrument_ids = None

    # Get the list of instruments that have some request for this activity
    activity_instruments = tesla_db.reports.get_activity_instruments_with_requests(activity.id)

    # Get activity statistics for involved instruments
    context_statistics = {}
    for instrument in activity_instruments:
        context_statistics[instrument.id] = {}
        context_statistics[instrument.id]['histogram'] = tesla_db.statistics.verification_activity_results_histogram(
            activity.id, instrument.id)
        context_statistics[instrument.id]['thresholds'] = schemas.InstrumentThreshold().dump(tesla_db.instruments.get_instrument_thresholds(
            instrument.id)).data

    # Get a paginated list of learners that will be in the response
    learners = tesla_db.reports.get_activity_learners_with_results(activity.id, page=page, max_per_page=max_per_page, instrument_ids=instrument_ids)

    # Get the data for each learner
    results = schemas.ActivitySummaryPagination().dump(learners).data
    for learner_result in results['items']:
        tesla_id = learner_result['tesla_id']
        summary = tesla_db.activities.get_activity_learner_summary(activity.id, tesla_id)
        summary_json = schemas.LearnerInstrumentResults(many=True).dump(summary).data

        # Build indexed data to make easier the results visualization
        indexed_info = {}
        for inst in summary_json:
            indexed_info[inst['instrument_id']] = inst

        # Update the learner data on the paginated view
        learner_result.update({"instruments": indexed_info})

        # Add learner level statistics
        learner_result.update({"stats": _get_learner_instrument_stats(learner_result, context_statistics)})

    # Build the paginated iterator as a list, since items type is JSON.
    results['iter_pages'] = [p for p in learners.iter_pages(left_edge=1, left_current=2, right_current=3, right_edge=1)]

    act_json = schemas.Activity().dump(activity).data
    return_data = {
        'results': results,
        'activity': act_json,
        'instruments': schemas.Instrument(many=True).dump(activity_instruments).data
    }

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, return_data)
    #return render_template('activity_report.html', pagination=results, endpoint='reports.activity_report', view=view, object=activity, instruments=activity_instruments)


@api_reports.route('/<int:vle_id>/<string:activity_type>/<string:activity_id>/<uuid:tesla_id>', methods=['GET'])
@require_tesla_cert()
def get_activity_learner_report(vle_id, activity_type, activity_id, tesla_id):
    """
        .. :quickref: Reports; Get report results for an activity and learner

        Get report results for an activity and learner

        :reqheader Authorization: This method requires authentication based on client certificate.

        :param vle_id: VLE identifier
        :type vle_id: int
        :param activity_type: type of the activity in the VLE
        :type activity_type: string
        :param activity_id: identifier of the activity in the VLE
        :type activity_id: string
        :param tesla_id: identifier of Learner
        :type tesla_id: guid

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
            | 3       | Activity not found                                                                           |
            +---------+----------------------------------------------------------------------------------------------+
            | 6       | Error persisting the data                                                                    |
            +---------+----------------------------------------------------------------------------------------------+
            | 16      | Learner not found                                                                            |
            +---------+----------------------------------------------------------------------------------------------+
            | 53      | Request JSON error. It contains more data or some required fields are missing.               |
            +---------+----------------------------------------------------------------------------------------------+

    """

    activity = tesla_db.activities.get_activity_by_def(vle_id, activity_type, activity_id)

    if activity is None:
        return api_response(TESLA_API_STATUS_CODE.ACTIVITY_NOT_FOUND, http_code=404)

    learner = tesla_db.learners.get_learner(tesla_id)
    
    if learner is None:
        return api_response(TESLA_API_STATUS_CODE.LEARNER_NOT_FOUND, http_code=404)


    # Get the list of instruments that have some request for this activity
    activity_instruments = tesla_db.reports.get_activity_instruments_with_requests(activity.id)

    # Get activity statistics for involved instruments
    context_statistics = {}
    for instrument in activity_instruments:
        context_statistics[instrument.id] = {}
        context_statistics[instrument.id][
            'histogram'] = tesla_db.statistics.verification_activity_results_histogram(activity.id, instrument.id)
        context_statistics[instrument.id]['thresholds'] = schemas.InstrumentThreshold().dump(tesla_db.instruments.get_instrument_thresholds(
            instrument.id)).data
        context_statistics[instrument.id]['temporal'] = _get_temporal_results(tesla_db.reports.get_activity_learner_temporal_results(activity.id, tesla_id, instrument.id))
        context_statistics[instrument.id]['aronym'] = instrument.acronym

    summary = tesla_db.activities.get_activity_learner_summary(activity.id, tesla_id)
    summary_json = schemas.LearnerInstrumentResults(many=True).dump(summary).data

    # Build indexed data to make easier the results visualization
    indexed_info = {}
    for inst in summary_json:
        indexed_info[inst['instrument_id']] = inst

    # Update the learner data on the paginated view
    learner_result = {
        "tesla_id": tesla_id,
        "instruments": indexed_info,
        "failed_requests": _get_temporal_results(
            tesla_db.reports.get_activity_learner_temporal_failed_requests(activity.id, tesla_id), break_far_samples=False)
    }

    # Add learner level statistics
    learner_result.update({"stats": _get_learner_instrument_stats(learner_result, context_statistics)})

    act_json = schemas.Activity().dump(activity).data
    result = {
        'learner': learner_result,
        'object': act_json,
        'instruments': schemas.Instrument(many=True).dump(activity_instruments).data,
        'context_statistics': context_statistics,
        'tesla_id': str(tesla_id)
    }

    return api_response(TESLA_API_STATUS_CODE.SUCCESS, result)


def _get_temporal_results(data, break_far_samples=True):

    max_gap_seconds = 240

    res_struct = {
        'date': [],
        'value': [],
        'error': []
    }

    last_date = None
    for point in data:
        if break_far_samples and (last_date is None or (point.date-last_date).total_seconds()>max_gap_seconds):
            res_struct['date'].append((point.date - timedelta(0,1)).__str__())
            res_struct['value'].append('NaN')
            res_struct['error'].append('')
        last_date = point.date
        res_struct['date'].append(point.date.__str__())
        res_struct['value'].append(round(float(point.value)*100))
        res_struct['error'].append(str(point.value))
    if break_far_samples and last_date is not None:
        res_struct['date'].append((last_date + timedelta(0, 1)).__str__())
        res_struct['value'].append('NaN')
        res_struct['error'].append('')

    return res_struct


def _get_learner_instrument_stats(learner_result, context_statistics):

    learner_stats = {}
    learner_stats['instruments'] = {}
    auth_levels = []
    content_levels = []
    security_levels = []
    for instrument_id in context_statistics.keys():
        # Initialize the instrument statistics
        level = 0.0
        prob_learner = 0.0
        prob_context = 0.0
        h_prob_learner = 1.0
        h_prob_context = 1.0
        confidence = 0.0
        histogram = []
        result_bean = None

        # TODO: Put polarity in instrument fields
        instrument_polarity = 1
        if instrument_id in [2, 3, 6]:
            instrument_polarity = -1

        # TODO: Put properties in instrument fields
        if instrument_id in [1, 3, 5]:
            is_auth = True
            is_content = False
            is_security = False
            var_summary = 'average'
        elif instrument_id in [7]:
            is_auth = True
            is_content = True
            is_security = False
            var_summary = 'min'
        elif instrument_id in [2, 3]:
            is_auth = False
            is_content = False
            is_security = True
            var_summary = 'max'
        elif instrument_id in [6]:
            is_auth = False
            is_content = True
            is_security = False
            var_summary = 'max'
        else:
            is_auth = False
            is_content = False
            is_security = False
            var_summary = 'average'

        # If learner have data for this instrument, update the statistics
        if instrument_id in learner_result['instruments']:
            context_hist = context_statistics[instrument_id]['histogram']
            histogram = tesla_db.statistics.get_learner_instrument_valid_results_histogram(learner_result['tesla_id'],
                                                                                           instrument_id)

            confidence = learner_result['instruments'][instrument_id]['valid'] / (learner_result['instruments'][instrument_id]['valid'] + learner_result['instruments'][instrument_id]['failed'] + 0.00000001)

            if confidence < 0.5:
                level = 2
            else:
                # Compute a final level
                if learner_result['instruments'][instrument_id][var_summary] < 1.0:
                    result_bean = math.floor(learner_result['instruments'][instrument_id][var_summary]*10.0)
                else:
                    result_bean = 9

                if result_bean == 0:
                    prob_learner = (histogram[result_bean] + 0.5 * histogram[result_bean + 1]) / (sum(histogram) + 0.00000001)
                    prob_context = (context_hist[result_bean] + 0.5 * context_hist[result_bean + 1]) / (sum(context_hist) + 0.00000001)
                    if instrument_polarity > 0:
                        h_prob_learner = sum(histogram[1:10]) / (sum(histogram) + 0.00000001)
                        h_prob_context = sum(context_hist[1:10]) / (sum(context_hist) + 0.00000001)
                    else:
                        h_prob_learner = 0.0
                        h_prob_context = 0.0
                elif result_bean == 9:
                    prob_learner = (histogram[result_bean] + 0.5 * histogram[result_bean - 1]) / (sum(histogram) + 0.00000001)
                    prob_context = (context_hist[result_bean] + 0.5 * context_hist[result_bean - 1]) / (sum(context_hist) + 0.00000001)
                    if instrument_polarity > 0:
                        h_prob_learner = 0.0
                        h_prob_context = 0.0
                    else:
                        h_prob_learner = sum(histogram[0:9]) / (sum(histogram) + 0.00000001)
                        h_prob_context = sum(context_hist[0:9]) / (sum(context_hist) + 0.00000001)

                else:
                    prob_learner = (0.5 * histogram[result_bean - 1] + histogram[result_bean] + 0.5 * histogram[result_bean + 1]) / (sum(histogram) + 0.00000001)
                    prob_context = (0.5 * context_hist[result_bean - 1] + context_hist[result_bean] + 0.5 * context_hist[result_bean + 1]) / (sum(context_hist) + 0.00000001)
                    if instrument_polarity > 0:
                        h_prob_learner = sum(histogram[result_bean + 1:10]) / (sum(histogram) + 0.00000001)
                        h_prob_context = sum(context_hist[result_bean+1:10]) / (sum(context_hist) + 0.00000001)
                    else:
                        h_prob_learner = sum(histogram[0:result_bean]) / (sum(histogram) + 0.00000001)
                        h_prob_context = sum(context_hist[0:result_bean]) / (sum(context_hist) + 0.00000001)

                # Get instrument thresholds
                thresholds = context_statistics[instrument_id]['thresholds']

                # Build final recomendation
                if thresholds is not None:
                    if (instrument_polarity > 0 and learner_result['instruments'][instrument_id][var_summary] > thresholds['medium']) or \
                            (instrument_polarity < 0 and (1.0 - learner_result['instruments'][instrument_id][var_summary]) > thresholds['medium']):
                        # If the mean value is in the green side, assume that is the learner
                        level = 3
                    else:
                        # Compare with the context
                        if h_prob_learner > 0.75:
                            # If the obtained value is not usual at all for this learner, assume that is not the learner
                            level = 1
                        elif h_prob_context < 0.5:
                            # If the value is larger than the contextual value, put in warning
                            level = 2
                        else:
                            # Otherwise put in danger
                            level = 1
                else:
                    # Compare with the context
                    if h_prob_learner < 0.4 and h_prob_context < 0.4:
                        level = 3
                    elif h_prob_learner > 0.75:
                        # If the obtained value is not usual at all for this learner, assume that is not the learner
                        level = 1
                    elif h_prob_context < 0.5:
                        # If the value is larger than the contextual value, put in warning
                        level = 2
                    else:
                        # Otherwise put in danger
                        level = 1


        thresholds_json = schemas.InstrumentThreshold().dump(context_statistics[instrument_id]['thresholds']).data
        # Store the instrument statistics
        learner_stats['instruments'][instrument_id] = {
            'prob_learner': prob_learner,
            'prob_context': prob_context,
            'h_prob_learner': h_prob_learner,
            'h_prob_context': h_prob_context,
            'confidence': confidence,
            'level': level,
            'instrument_polarity': instrument_polarity,
            'histogram': histogram,
            'result_bean': result_bean,
            'thresholds': thresholds_json
        }

        # Store the level
        if is_auth:
            auth_levels.append(level)
        if is_content:
            content_levels.append(level)
        if is_security:
            security_levels.append(level)

    # Compute a final levels
    if len(auth_levels) > 0:
        positive = 3 in auth_levels
        negative = 1 in auth_levels

        if positive and negative:
            auth_level = 2
        elif not positive and negative:
            auth_level = 1
        elif positive and not negative:
            auth_level = 3
        else:
            auth_level = math.floor(sum(auth_levels) / len(auth_levels))
    else:
        auth_level = 0

    if len(content_levels) > 0:
        positive = 3 in content_levels
        negative = 1 in content_levels

        if positive and negative:
            content_level = 2
        elif not positive and negative:
            content_level = 1
        elif positive and not negative:
            content_level = 3
        else:
            content_level = math.floor(sum(content_levels) / len(content_levels))
    else:
        content_level = 0

    if len(security_levels) > 0:
        positive = 3 in security_levels
        negative = 1 in security_levels

        if positive and negative:
            security_level = 2
        elif not positive and negative:
            security_level = 1
        elif positive and not negative:
            security_level = 3
        else:
            security_level = math.floor(sum(security_levels) / len(security_levels))
    else:
        security_level = 0

    learner_stats['levels']= {
        'auth': auth_level,
        'content': content_level,
        'security': security_level
    }

    return learner_stats