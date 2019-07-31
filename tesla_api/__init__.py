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

from tesla_flask import app, logger, tesla_db, cache

# Define the API Base
api_base = '/api/v1'

# Add learners api
from tesla_api.api.learners import api_learners
app.register_blueprint(api_learners, url_prefix=api_base + '/learners')

# Add activities api
from tesla_api.api.activities import api_activities
app.register_blueprint(api_activities, url_prefix=api_base + '/activities')

# Add instruments api
from tesla_api.api.instruments import api_instruments
app.register_blueprint(api_instruments, url_prefix=api_base + '/instruments')

# Add requests api
from tesla_api.api.requests import api_requests
app.register_blueprint(api_requests, url_prefix=api_base + '/requests')

# Add requests api
from tesla_api.api.reports import api_reports
app.register_blueprint(api_reports, url_prefix=api_base + '/reports')


# Add requests api
from tesla_api.api.test import api_test
app.register_blueprint(api_test, url_prefix=api_base + '/test')
