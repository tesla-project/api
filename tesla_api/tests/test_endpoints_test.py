
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

def test_test_no_cert(base_api_url, app, client):
    """ Check entrypoint test/no_cert """

    response = client.get(base_api_url+str("test/no_cert"))

    response_json = response.get_json()
    assert(int(response_json['status_code']) == 0)


def test_test_any_module(base_api_url, app, client_with_certificate_ks):
    """ Check entrypoint test/any_module """

    response = client_with_certificate_ks.get(base_api_url+str("test/any_module"))
    
    response_json = response.get_json()
    assert(int(response_json['status_code']) == 0)


def test_test_any_module_inject(base_api_url, app, client_with_certificate_ks):
    """ Check entrypoint test/any_module_inject """

    response = client_with_certificate_ks.get(base_api_url+str("test/any_module_inject"))

    response_json = response.get_json()
    assert(int(response_json['status_code']) == 0)


def test_test_instrument(base_api_url, app, client_with_certificate_ks):
    """ Check entrypoint test/instrument """

    response = client_with_certificate_ks.get(base_api_url+str("test/instrument"))

    response_json = response.get_json()
    assert(int(response_json['status_code']) == 0)


def test_test_instrument_fail(base_api_url, app, client_with_certificate_tip):
    """ Check entrypoint test/instrument with fails """

    response = client_with_certificate_tip.get(base_api_url+str("test/instrument"))

    response_json = response.get_json()
    assert(int(response_json['status_code']) == 54)


def test_test_instrument_inject(base_api_url, app, client_with_certificate_ks):
    """ Check entrypoint test/instrument_inject """

    response = client_with_certificate_ks.get(base_api_url+str("test/instrument_inject"))

    response_json = response.get_json()
    assert(int(response_json['status_code']) == 0)


def test_test_list_mods(base_api_url, app, client_with_certificate_ks):
    """ Check entrypoint test/list_mods """

    response = client_with_certificate_ks.get(base_api_url+str("test/list_mods"))

    response_json = response.get_json()
    assert(int(response_json['status_code']) == 0)


def test_test_list_mods_inject(base_api_url, app, client_with_certificate_ks):
    """ Check entrypoint test/list_mods """

    response = client_with_certificate_ks.get(base_api_url+str("test/list_mods_inject"))

    response_json = response.get_json()
    assert(int(response_json['status_code']) == 0)


def test_test_tep(base_api_url, app, client_with_certificate_tep):
    """ Check entrypoint test/tep """

    response = client_with_certificate_tep.get(base_api_url+str("test/tep"))

    response_json = response.get_json()
    assert(int(response_json['status_code']) == 0)


def test_test_tep_inject(base_api_url, app, client_with_certificate_tep):
    """ Check entrypoint test/tep_inject """

    response = client_with_certificate_tep.get(base_api_url+str("test/tep_inject"))

    response_json = response.get_json()
    assert(int(response_json['status_code']) == 0)
