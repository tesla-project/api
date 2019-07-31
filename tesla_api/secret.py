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

import os
from OpenSSL import crypto
from tesla_api import logger, tesla_db, utils

AUTHORIZED_CLIENTS = ['tep', 'rt']


def get_instrument_from_cert(request):

    cert = request.environ.get('HTTP_X_SSL_CERT', None)

    if cert is None:
        return None

    cert = cert + '\n'
    cert = cert.replace('\n\t', '\n')

    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

    subject = cert.get_subject().CN.upper()

    acronym = subject.split('-')[0]

    return tesla_db.instruments.get_instrument_by_acronym(acronym)


def get_module_from_cert(request):

    cert = request.environ.get('HTTP_X_SSL_CERT', None)

    if bool(int(os.getenv('ALLOW_DEBUG_HEADER_CN', 0))):
        logger.warning('ALLOW_DEBUG_HEADER_CN enabled. Disable in production environment.')
        return utils.get_cert_module_debug(cert)

    return utils.get_cert_module(cert)


def validate_client_cert(cert, authorized=AUTHORIZED_CLIENTS):
    cert = cert + '\n'
    cert = cert.replace('\n\t', '\n')

    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

    # logging.info('cert info: ' + str(cert))

    subject = cert.get_subject()

    # logging.info('subject: ' + str(subject))

    issued_to = subject.CN.lower()

    # logging.info('issued_to: ' + str(issued_to))

    if isinstance(authorized, str):
        is_valid = issued_to == authorized
    else:
        is_valid = any([issued_to.startswith(client) for client in authorized])

    if not is_valid:
        # Check if is an instrument
        logger.warning("Certificate validation failed: got {} compared to {}".format(issued_to, authorized))

    return is_valid


def get_secret(secret_name, default=None):
    secret_filename = os.path.join('/run/secret/', secret_name)

    if os.path.isfile(secret_filename):
        with open(secret_filename, 'r') as content_file:
            content = content_file.read()
            return content
    else:
        return os.getenv(secret_name, default)
