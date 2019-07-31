
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

import pytest
import time

from tesla_api import app as tesla_flask_app
from tesla_flask import db
from .certificates import certificates

@pytest.fixture
def app():
    tesla_flask_app.config['TESTING'] = True
    tesla_flask_app.testing = True
    app = tesla_flask_app

    yield app


@pytest.fixture
def client(app, certificate_module = None):
    client = app.test_client()

    if certificate_module is not None:
        client.environ_base = {"HTTP_X_SSL_CERT": certificates[certificate_module]}

    return client


@pytest.fixture
def client_with_certificate_tip(app):
    return client(app, "tip")


@pytest.fixture
def client_with_certificate_ks(app):
    return client(app, "ks")


@pytest.fixture
def client_with_certificate_lti(app):
    return client(app, "lti")


@pytest.fixture
def client_with_certificate_plugin(app):
    return client(app, "plugin")


@pytest.fixture
def client_with_certificate_rt(app):
    return client(app, "rt")


@pytest.fixture
def client_with_certificate_tep(app):
    return client(app, "tep")


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def base_api_url():
    return "http://localhost:5000/api/v1/"
