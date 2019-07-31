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

from tesla_api import tesla_db, cache, logger
from tesla_models import tep_db
from distutils.version import LooseVersion
from tesla_models.database.utils import decode_data
from tesla_models.models import instrument_schema
import jwt
from OpenSSL import crypto


#@cache.memoize(900)
def token_data(token):

    # Get the payload without verification
    token_data = jwt.decode(token, verify=False)

    # Get public key for learner in payload
    tesla_id = token_data['sub']

    # TODO: Remove if TEP is not deployed
    learner = tep_db.sync_learner(tesla_id)
    #learner = database.get_learner(tesla_id)

    # Get key
    payload = None
    if learner is not None:
        crypto_data = decode_data(learner.crypto_data)
        pubkey = crypto_data['key']
        payload = jwt.decode(token, pubkey, algorithms=['RS256'])

    return payload


#@cache.memoize(900)
def get_learner_ic_info(tesla_id):

    response = {'learner_found': False,
                'ic_version': None,
                'ic_current_version': None,
                'accepted_date': None,
                'rejected_date': None,
                'ic_valid': False
                }

    # Get the learner information
    # TODO: Remove if TEP is not deployed
    learner = tep_db.sync_learner(tesla_id)
    if learner is None:
        return response

    response['learner_found']= True

    # Get informed consent information
    if learner.consent_id is None:
        return response

    ic = tesla_db.learners.get_informed_consent_by_id(learner.consent_id)
    current_ic = tesla_db.learners.get_current_informed_consent()
    response['ic_version'] = ic.version
    response['accepted_date'] = learner.consent_accepted
    response['rejected_date'] = learner.consent_rejected
    response['ic_current_version'] = current_ic.version

    if learner.consent_rejected is not None:
        return response

    ic_version = LooseVersion(ic.version).version
    current_version = LooseVersion(current_ic.version).version

    if ic_version[0] == current_version[0] and ic_version[1] == current_version[1]:
        response['ic_valid'] = True

    return response


#@cache.memoize(900)
def get_learner_send_info(tesla_id):
    # TODO: Remove if TEP is not deployed
    learner = tep_db.sync_learner(tesla_id)

    send_categories = tesla_db.learners.get_send_user(tesla_id)
    disabled_instruments = set()
    options = set()

    if send_categories is None:
        send_categories = []

    for c in send_categories:
        data = decode_data(c.data)
        c.data = data
        disabled_instruments.update(data['instruments'])
        options.update(data['options'])

    return {'is_send': len(send_categories)>0,
            'send': {'options': list(options), 'disabled_instruments': list(disabled_instruments)}}


#@cache.memoize(900)
def get_cert_module(cert):

    if cert is None:
        return None

    cert = cert + '\n'
    cert = cert.replace('\n\t', '\n')

    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

    subject = cert.get_subject().CN.upper()
    acronym = subject.split('.')[0]
    print(tesla_db.db)
    instrument = tesla_db.instruments.get_instrument_by_acronym(acronym)
    is_instrument = False
    if instrument is not None:
        is_instrument = True
        instrument = instrument_schema.dump(instrument)[0]

    return {'is_instrument': is_instrument, 'acronym': acronym, 'instrument': instrument}


def get_cert_module_debug(cert):

    from flask import request

    debug_cn = request.args.get('debug_cn')
    if debug_cn:
        subject = debug_cn.upper()
        acronym = subject.split('-')[0]
        instrument = tesla_db.instruments.get_instrument_by_acronym(acronym)
        is_instrument = False
        if instrument is not None:
            is_instrument = True
            instrument = instrument_schema.dump(instrument)[0]

        return {'is_instrument': is_instrument, 'acronym': acronym, 'instrument': instrument}

    return get_cert_module(cert)


#@cache.memoize(900)
def get_learner_enrolments(tesla_id):
    # TODO: Remove if TEP is not deployed
    tep_db.sync_learner(tesla_id)

    return tesla_db.learners.get_learner_enrolments(tesla_id)
