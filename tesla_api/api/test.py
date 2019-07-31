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


api_test = Blueprint('api_test', __name__)


@api_test.route('/no_cert', methods=['GET'])
def test_no_cert():
    return api_response(TESLA_API_STATUS_CODE.SUCCESS)


@api_test.route('/any_module', methods=['GET'])
@require_tesla_cert()
def test_any_module():
    return api_response(TESLA_API_STATUS_CODE.SUCCESS)


@api_test.route('/any_module_inject', methods=['GET'])
@require_tesla_cert(inject_module=True)
def test_any_module_inject(module):
    return api_response(TESLA_API_STATUS_CODE.SUCCESS, data=module)


@api_test.route('/instrument', methods=['GET'])
@require_tesla_cert(allowed_modules='INSTRUMENT')
def test_any_instrument():
    return api_response(TESLA_API_STATUS_CODE.SUCCESS)


@api_test.route('/instrument_inject', methods=['GET'])
@require_tesla_cert(allowed_modules='INSTRUMENT', inject_module=True)
def test_any_instrument_inject(module):
    return api_response(TESLA_API_STATUS_CODE.SUCCESS, data=module)


@api_test.route('/list_mods', methods=['GET'])
@require_tesla_cert(allowed_modules=['INSTRUMENT', 'TEP'])
def test_list_modules():
    return api_response(TESLA_API_STATUS_CODE.SUCCESS)


@api_test.route('/list_mods_inject', methods=['GET'])
@require_tesla_cert(allowed_modules=['INSTRUMENT', 'TEP'], inject_module=True)
def test_list_modules_inject(module):
    return api_response(TESLA_API_STATUS_CODE.SUCCESS, data=module)


@api_test.route('/tep', methods=['GET'])
@require_tesla_cert(allowed_modules='TEP')
def test_tep():
    return api_response(TESLA_API_STATUS_CODE.SUCCESS)


@api_test.route('/tep_inject', methods=['GET'])
@require_tesla_cert(allowed_modules='TEP', inject_module=True)
def test_tep_inject(module):
    return api_response(TESLA_API_STATUS_CODE.SUCCESS, data=module)

