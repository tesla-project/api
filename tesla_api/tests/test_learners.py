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

import json

def test_learner_add_learner(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint learners/add_learner """

    data = json.dumps({"tesla_id": "9cd125c3-badb-4aa7-b694-321e0d76858f", "public_cert": "PUBLIC_CERT", "cert_alg": "RSA"})

    response = client_with_certificate_tip.post(base_api_url+str("learners"), data=data)

    #response_json = response.get_json()
    assert(response.status_code == 501)


def test_learner_get_learner(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint learners/get_learner """

    tesla_id =  "9cd125c3-badb-4aa7-b694-321e0d76858f"
    response = client_with_certificate_tip.get(base_api_url+str("learners")+"/"+str(tesla_id))

    #response_json = response.get_json()
    assert(response.status_code == 501)


def test_learner_get_learner_fail(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint learners/add_learner_fail """

    tesla_id =  "TESLA_FAKE_ID"

    response = client_with_certificate_tip.get(base_api_url+str("learners")+"/"+str(tesla_id))

    #response_json = response.get_json()
    assert(response.status_code == 404)


def test_learner_put_learner(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint learners/put_learner """

    tesla_id = "9cd125c3-badb-4aa7-b694-321e0d76858f"
    data = json.dumps({"tesla_id": "9cd125c3-badb-4aa7-b694-321e0d76858f", "public_cert": "PUBLIC_CERT", "cert_alg": "RSA"})

    response = client_with_certificate_tip.put(base_api_url+str("learners")+"/"+str(tesla_id), data=data)

    #response_json = response.get_json()
    assert(response.status_code == 501)


def test_learner_delete_learner(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint learners/delete_learner """

    tesla_id =  "9cd125c3-badb-4aa7-b694-321e0d76858f"
    data = json.dumps({"tesla_id": "9cd125c3-badb-4aa7-b694-321e0d76858f", "public_cert": "PUBLIC_CERT", "cert_alg": "RSA"})

    response = client_with_certificate_tip.delete(base_api_url+str("learners")+"/"+str(tesla_id))

    #response_json = response.get_json()
    assert(response.status_code == 501)


def test_learner_get_learner_send(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint learners/get_learner_send """

    tesla_id =  "9cd125c3-badb-4aa7-b694-321e0d76858f"
    response = client_with_certificate_tip.get(base_api_url+str("learners")+"/"+str(tesla_id)+"/send")

    assert(response.status_code == 501)


def test_learner_get_learner_send(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint learners/informed-consent """

    tesla_id =  "9cd125c3-badb-4aa7-b694-321e0d76858f"
    response = client_with_certificate_tip.get(base_api_url+str("learners")+"/"+str(tesla_id)+"/informed-consent")

    assert(response.status_code == 501)


def test_learner_get_learner_enrolment(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint learners/enrolment """

    tesla_id =  "9cd125c3-badb-4aa7-b694-321e0d76858f"
    response = client_with_certificate_tip.get(base_api_url+str("learners")+"/"+str(tesla_id)+"/enrolment")

    assert(response.status_code == 501)


def test_learner_get_learner_instrument_enrolment(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint learners/instrument/enrolment """

    tesla_id =  "9cd125c3-badb-4aa7-b694-321e0d76858f"
    instrument_id = "1"
    response = client_with_certificate_tip.get(base_api_url+str("learners")+"/"+str(tesla_id)+"/instruments/"+str(instrument_id)+"/enrolment")

    assert(response.status_code == 200)

    # todo make test with add learner when it will be possible


def test_learner_get_learner_activity_enrolments(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint learners/activities/enrolment """

    tesla_id =  "9cd125c3-badb-4aa7-b694-321e0d76858f"
    vle_id = "1"
    activity_type = "quiz"
    activity_id = "1"

    response = client_with_certificate_tip.get(base_api_url+str("learners")+"/"+str(tesla_id)+"/activities/"+str(vle_id)+"/"+str(activity_type)+"/"+str(activity_id)+"/enrolments")

    assert(response.status_code == 501)


def test_learner_get_learner_activity_instruments(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint learners/activities/insrtuments"""

    tesla_id =  "9cd125c3-badb-4aa7-b694-321e0d76858f"
    vle_id = "1"
    activity_type = "quiz"
    activity_id = "1"

    response = client_with_certificate_tip.get(base_api_url+str("learners")+"/"+str(tesla_id)+"/activities/"+str(vle_id)+"/"+str(activity_type)+"/"+str(activity_id)+"/instruments")
    response_json = response.get_json()


    assert(response.status_code == 200)
    assert(response_json['learner_found'] == False)
    assert(response_json['instrument_ids'] == [])
    assert(response_json['send'] == {})
    '''
    response = {'learner_found': True,
                'agreement_status': True,
                'instrument_ids': instruments,
                'send': send_info
                }
    '''


def test_learner_get_learner_activity_results(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint learners/activities/results """

    tesla_id =  "9cd125c3-badb-4aa7-b694-321e0d76858f"
    vle_id = "1"
    activity_type = "quiz"
    activity_id = "1"

    response = client_with_certificate_tip.get(base_api_url+str("learners")+"/"+str(tesla_id)+"/activities/"+str(vle_id)+"/"+str(activity_type)+"/"+str(activity_id)+"/results")

    assert(response.status_code == 501)


def test_learner_get_learner_activity_results(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint learners/activities/instruments/results """

    tesla_id =  "9cd125c3-badb-4aa7-b694-321e0d76858f"
    vle_id = "1"
    activity_type = "quiz"
    activity_id = "1"
    instrument_id = "1"

    response = client_with_certificate_tip.get(base_api_url+str("learners")+"/"+str(tesla_id)+"/activities/"+str(vle_id)+"/"+str(activity_type)+"/"+str(activity_id)+"/instruments/"+str(instrument_id)+"/results")

    assert(response.status_code == 501)


def test_learner_get_learner_activity_instrument_audit(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint learners/activities/instrument/audit """

    tesla_id =  "9cd125c3-badb-4aa7-b694-321e0d76858f"
    vle_id = "1"
    activity_type = "quiz"
    activity_id = "1"
    instrument_id = "1"

    response = client_with_certificate_tip.get(base_api_url+str("learners")+"/"+str(tesla_id)+"/activities/"+str(vle_id)+"/"+str(activity_type)+"/"+str(activity_id)+"/instruments/"+str(instrument_id)+"/audit")

    assert(response.status_code == 501)


def test_learner_get_learner_activity_request_instrument_audit(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint learners/activities/requests/instrument/audit """

    tesla_id =  "9cd125c3-badb-4aa7-b694-321e0d76858f"
    vle_id = "1"
    activity_type = "quiz"
    activity_id = "1"
    instrument_id = "1"
    request_id = "1"

    response = client_with_certificate_tip.get(base_api_url+str("learners")+"/"+str(tesla_id)+"/activities/"+str(vle_id)+"/"+str(activity_type)+"/"+str(activity_id)+"/requests/"+str(request_id)+"/instruments/"+str(instrument_id)+"/audit")

    assert(response.status_code == 501)
