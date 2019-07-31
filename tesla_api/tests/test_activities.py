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

import json, datetime

def test_activity_add_activity(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint activities/add_activity """

    # activity exists
    data = json.dumps({"vle_id": 1, "activity_type": "quiz", "activity_id": "1", "description": "test description", "conf": ""})
    response = client_with_certificate_tip.post(base_api_url+str("activities"), data=data, content_type='application/json')
    response_json = response.get_json()

    assert (response.status_code == 400)
    assert (int(response_json['activity_id']) == 1)
    assert (int(response_json['status_code']) == 13)
    assert (response_json['activity_type'] == "quiz")

    # new activity, not exists
    random_number = str(datetime.datetime.now())
    random_type = "test_type_"+str(random_number)
    data = json.dumps({"vle_id": 1, "activity_type": str(random_type), "activity_id": str(random_number), "description": "test description", "conf": ""})
    response = client_with_certificate_tip.post(base_api_url+str("activities"), data=data, content_type='application/json')
    response_json = response.get_json()

    assert (response.status_code == 200)
    assert (str(response_json['activity_id']) == str(random_number))
    assert (int(response_json['status_code']) == 0)
    assert (response_json['activity_type'] == str(random_type))


def test_activity_get_activity(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint activities/get_activity """

    # new activity, not exists
    random_number = str(datetime.datetime.now())
    random_type = "test_type_"+str(random_number)
    data = json.dumps({"vle_id": 1, "activity_type": str(random_type), "activity_id": str(random_number), "description": "test description", "conf": ""})
    response = client_with_certificate_tip.post(base_api_url+str("activities"), data=data, content_type='application/json')
    response_json = response.get_json()

    assert (response.status_code == 200)
    assert (str(response_json['activity_id']) == str(random_number))
    assert (int(response_json['status_code']) == 0)
    assert (response_json['activity_type'] == str(random_type))

    data = json.dumps({"vle_id": 1, "activity_type": str(random_type), "activity_id": str(random_number), "description": "test description", "conf": ""})
    vle_id = 1
    activity_type = random_type
    activity_id = random_number
    response = client_with_certificate_tip.get(base_api_url+str("activities")+"/"+str(vle_id)+"/"+str(activity_type)+"/"+str(activity_id), data=data, content_type='application/json')
    response_json = response.get_json()

    assert (response.status_code == 200)
    assert (str(response_json['activity_id']) == str(random_number))
    assert (int(response_json['status_code']) == 0)
    assert (response_json['activity_type'] == str(random_type))
    assert (response_json['activity_id'] == str(random_number))

    # check no exist activity
    random_number = str(datetime.datetime.now())
    random_type = "NO_EXIST_test_type_"+str(random_number)
    activity_type = random_type
    activity_id = random_number

    response = client_with_certificate_tip.get(base_api_url+str("activities")+"/"+str(vle_id)+"/"+str(activity_type)+"/"+str(activity_id), data=data, content_type='application/json')

    assert (response.status_code == 404)


def test_activity_update_activity(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint activities/update_activity """

    # new activity, not exists
    random_number = str(datetime.datetime.now())
    random_type = "test_type_"+str(random_number)
    data = json.dumps({"vle_id": 1, "activity_type": str(random_type), "activity_id": str(random_number), "description": "test description", "conf": ""})
    response = client_with_certificate_tip.post(base_api_url+str("activities"), data=data, content_type='application/json')
    response_json = response.get_json()

    assert (response.status_code == 200)
    assert (str(response_json['activity_id']) == str(random_number))
    assert (int(response_json['status_code']) == 0)
    assert (response_json['activity_type'] == str(random_type))

    data = json.dumps({"vle_id": 1, "activity_type": str(random_type), "activity_id": str(random_number), "description": "test description CHANGED", "conf": {"key": "CHANGED_CONFIG"}})
    vle_id = 1
    activity_type = random_type
    activity_id = random_number
    response = client_with_certificate_tip.put(base_api_url+str("activities")+"/"+str(vle_id)+"/"+str(activity_type)+"/"+str(activity_id), data=data, content_type='application/json')
    response_json = response.get_json()

    assert (response.status_code == 200)
    assert (str(response_json['activity_id']) == str(random_number))
    assert (int(response_json['status_code']) == 0)
    assert (response_json['activity_type'] == str(random_type))
    assert (response_json['conf'] == {"key": "CHANGED_CONFIG"})
    assert (response_json['description'] == "test description CHANGED")


def test_activity_delete_activity(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint activities/delete """

    # new activity, not exists
    random_number = str(datetime.datetime.now())
    random_type = "test_type_"+str(random_number)
    data = json.dumps({"vle_id": 1, "activity_type": str(random_type), "activity_id": str(random_number), "description": "test description", "conf": ""})
    response = client_with_certificate_tip.post(base_api_url+str("activities"), data=data, content_type='application/json')
    response_json = response.get_json()

    assert (response.status_code == 200)
    assert (str(response_json['activity_id']) == str(random_number))
    assert (int(response_json['status_code']) == 0)
    assert (response_json['activity_type'] == str(random_type))

    data = json.dumps({"vle_id": 1, "activity_type": str(random_type), "activity_id": str(random_number), "description": "test description CHANGED", "conf": {"key": "CHANGED_CONFIG"}})
    vle_id = 1
    activity_type = random_type
    activity_id = random_number
    response = client_with_certificate_tip.delete(base_api_url+str("activities")+"/"+str(vle_id)+"/"+str(activity_type)+"/"+str(activity_id), data=data, content_type='application/json')
    response_json = response.get_json()

    assert (response.status_code == 501)
    assert (int(response_json['status_code']) == 0)


def test_activity_get_activity_instruments(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint activities/activity/instruments """

    # new activity, not exists
    random_number = str(datetime.datetime.now())
    random_type = "test_type_"+str(random_number)
    data = json.dumps({"vle_id": 1, "activity_type": str(random_type), "activity_id": str(random_number), "description": "test description", "conf": ""})
    response = client_with_certificate_tip.post(base_api_url+str("activities"), data=data, content_type='application/json')
    response_json = response.get_json()

    assert (response.status_code == 200)
    assert (str(response_json['activity_id']) == str(random_number))
    assert (int(response_json['status_code']) == 0)
    assert (response_json['activity_type'] == str(random_type))

    data = json.dumps({"vle_id": 1, "activity_type": str(random_type), "activity_id": str(random_number), "description": "test description CHANGED", "conf": {"key": "CHANGED_CONFIG"}})
    vle_id = 1
    activity_type = random_type
    activity_id = random_number
    response = client_with_certificate_tip.get(base_api_url+str("activities")+"/"+str(vle_id)+"/"+str(activity_type)+"/"+str(activity_id)+"/instruments", content_type='application/json')
    response_json = response.get_json()

    assert (response.status_code == 200)
    assert (int(response_json['status_code']) == 0)
    assert (len(response_json['instruments']) == 0)


def test_activity_set_activity_instruments(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint activities/activity/instruments """

    # new activity, not exists
    random_number = str(datetime.datetime.now())
    random_type = "test_type_"+str(random_number)
    data = json.dumps({"vle_id": 1, "activity_type": str(random_type), "activity_id": str(random_number), "description": "test description", "conf": ""})
    response = client_with_certificate_tip.post(base_api_url+str("activities"), data=data, content_type='application/json')
    response_json = response.get_json()

    assert (response.status_code == 200)
    assert (str(response_json['activity_id']) == str(random_number))
    assert (int(response_json['status_code']) == 0)
    assert (response_json['activity_type'] == str(random_type))

    instruments = []
    instruments.append({"instrument_id": 1, "required": True, "options": {"mode": "online"}, "active": True})
    instruments.append({"instrument_id": 3, "required": False, "options": {"mode": "offine"}, "active": True})

    data = json.dumps(instruments)
    vle_id = 1
    activity_type = random_type
    activity_id = random_number
    response = client_with_certificate_tip.post(base_api_url+str("activities")+"/"+str(vle_id)+"/"+str(activity_type)+"/"+str(activity_id)+"/instruments", data=data, content_type='application/json')
    response_json = response.get_json()

    assert (response.status_code == 200)
    assert (int(response_json['status_code']) == 0)

    index_instruments_ok = 0
    for instrument in instruments:
        for response_instrument in response_json['instruments']:
             if response_instrument['instrument_id'] == instrument['instrument_id'] and response_instrument['required'] == instrument['required'] and response_instrument['options'] == instrument['options'] and response_instrument['active'] == instrument['active']:
                 index_instruments_ok += 1

    assert(len(response_json['instruments']) == index_instruments_ok)
    assert(len(instruments) == (index_instruments_ok))


def test_activity_get_activity_learners(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint activities/activity/learners """

    # new activity, not exists
    random_number = str(datetime.datetime.now())
    random_type = "test_type_"+str(random_number)
    data = json.dumps({"vle_id": 1, "activity_type": str(random_type), "activity_id": str(random_number), "description": "test description", "conf": ""})
    response = client_with_certificate_tip.post(base_api_url+str("activities"), data=data, content_type='application/json')
    response_json = response.get_json()

    assert (response.status_code == 200)
    assert (str(response_json['activity_id']) == str(random_number))
    assert (int(response_json['status_code']) == 0)
    assert (response_json['activity_type'] == str(random_type))

    vle_id = 1
    activity_type = random_type
    activity_id = random_number
    response = client_with_certificate_tip.get(base_api_url+str("activities")+"/"+str(vle_id)+"/"+str(activity_type)+"/"+str(activity_id)+"/learners", content_type='application/json')

    response_json = response.get_json()

    assert (response.status_code == 501)


def test_activity_get_activity_results(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint activities/activity/results """

    # new activity, not exists
    random_number = str(datetime.datetime.now())
    random_type = "test_type_"+str(random_number)
    data = json.dumps({"vle_id": 1, "activity_type": str(random_type), "activity_id": str(random_number), "description": "test description", "conf": ""})
    response = client_with_certificate_tip.post(base_api_url+str("activities"), data=data, content_type='application/json')
    response_json = response.get_json()

    assert (response.status_code == 200)
    assert (str(response_json['activity_id']) == str(random_number))
    assert (int(response_json['status_code']) == 0)
    assert (response_json['activity_type'] == str(random_type))

    vle_id = 1
    activity_type = random_type
    activity_id = random_number
    response = client_with_certificate_tip.get(base_api_url+str("activities")+"/"+str(vle_id)+"/"+str(activity_type)+"/"+str(activity_id)+"/results", content_type='application/json')

    response_json = response.get_json()

    assert (response.status_code == 200)
    assert (len(response_json['items']) == 0)
