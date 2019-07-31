"""
TeSLA function decorators
"""
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

from functools import wraps
from flask import request, jsonify
from tesla_api import secret, logger
import os


def drain_request():
    """
    Helper function that will trigger a dummy call to consume post data because
    the requests package fails to handle early "termination".
    see https://github.com/kennethreitz/requests/issues/2422 for a related issue
    """
    request.get_json(silent=True, cache=False)


def certificate_required(f):
    """
    This route decorator applies certification validation before going further.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        validated = False
        try:
            authorized_clients = secret.AUTHORIZED_CLIENTS
            skip_cert_verification = bool(int(os.environ.get('SKIP_CERT_VERIFICATION', 0)))
            if skip_cert_verification:
                logger.debug('Skiped Certificate verification')
                validated = True
                return f(*args, **kwargs)

            client_cert = request.environ.get('HTTP_X_SSL_CERT', None)

            if not client_cert or not secret.validate_client_cert(client_cert, authorized_clients):
                drain_request()
                logger.info('Invalid Certificate')
                return jsonify({'status_code': '54'}), 401  # code 54 for invalid client_cert
            validated = True
            if 'cert_cn' in kwargs.keys():
                kwargs['cert_cn'] = 'TEST'
            return f(*args, **kwargs)
        except Exception as ex:
            if not validated:
                return jsonify({'status_code': '54'}), 401  # code 54 for invalid client_cert
            else:
                raise ex

    return decorated_function


def instrument_certificate_required(f):
    """
    This route decorator applies certification validation before going further.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        validated = False
        try:
            #instrument = secret.get_instrument_from_cert(request)
            module = secret.get_module_from_cert(request)
            if module is None or not module['is_instrument']:
                drain_request()
                logger.info('Invalid Certificate')
                return jsonify({'status_code': '54'}), 401  # code 54 for invalid client_cert
            validated = True

            kwargs['instrument'] = module['instrument']
            return f(*args, **kwargs)
        except Exception as ex:
            if not validated:
                return jsonify({'status_code': '54'}), 401  # code 54 for invalid client_cert
            else:
                raise ex

    return decorated_function


def module_certificate_required(f):
    """
    This route decorator applies certification validation before going further.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        validated = False
        try:
            instrument = secret.get_instrument_from_cert(request)
            if instrument is None:
                drain_request()
                logger.info('Invalid Certificate')
                return jsonify({'status_code': '54'}), 401  # code 54 for invalid client_cert
            validated = True

            kwargs['instrument'] = instrument
            return f(*args, **kwargs)
        except Exception as ex:
            if not validated:
                return jsonify({'status_code': '54'}), 401  # code 54 for invalid client_cert
            else:
                raise ex

    return decorated_function


def require_tesla_cert(allowed_modules=None, inject_module=False):
    """Decorator which specifies that a user must have all the specified roles.
    Example::

        @app.route('/dashboard')
        @roles_required('admin', 'editor')
        def dashboard():
            return 'Dashboard'

    The current user must have both the `admin` role and `editor` role in order
    to view the page.

    :param args: The required roles.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            try:
                validated = False
                module = secret.get_module_from_cert(request)
                print(module)
                if module is None:
                    drain_request()
                    logger.info('Invalid Certificate')
                    return jsonify({'status_code': '54'}), 401  # code 54 for invalid client_cert

                if allowed_modules is not None:
                    list_allowed_modules = []
                    if not isinstance(allowed_modules, list):
                        list_allowed_modules.append(allowed_modules)
                    else:
                        list_allowed_modules += allowed_modules

                    valid_module = False
                    if module['is_instrument'] and "INSTRUMENT" in list_allowed_modules:
                        valid_module = True
                    elif module['acronym'] in list_allowed_modules:
                        valid_module = True

                    if not valid_module:
                        drain_request()
                        logger.info('Unauthorized Certificate Module')
                        return jsonify({'status_code': '54'}), 401  # code 54 for invalid client_cert

                if inject_module:
                    kwargs['module'] = module

                validated = True

                return fn(*args, **kwargs)

            except Exception as ex:
                if not validated:
                    return jsonify({'status_code': '54'}), 401  # code 54 for invalid client_cert
                else:
                    raise ex

        return decorated_view
    return wrapper