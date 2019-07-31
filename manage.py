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

import sys
import os

from click import echo

from tesla_api import app

@app.cli.command('urlmap')
def urlmap():
    """Prints out all routes"""
    echo("{:50s} {:40s} {}".format('Endpoint', 'Methods', 'Route'))
    for route in app.url_map.iter_rules():
        methods = ','.join(route.methods)
        echo("{:50s} {:40s} {}".format(route.endpoint, methods, route))


@app.cli.command('ipython')
def ipython():
    """Runs a ipython shell in the app context."""
    try:
        import IPython
    except ImportError:
        echo("IPython not found. Install with: 'pip install ipython'")
        return
    from flask.globals import _app_ctx_stack
    app = _app_ctx_stack.top.app
    banner = 'Python %s on %s\nIPython: %s\nApp: %s%s\nInstance: %s\n' % (
        sys.version,
        sys.platform,
        IPython.__version__,
        app.import_name,
        app.debug and ' [debug]' or '',
        app.instance_path,
    )

    ctx = {}

    # Support the regular Python interpreter startup script if someone
    # is using it.
    startup = os.environ.get('PYTHONSTARTUP')
    if startup and os.path.isfile(startup):
        with open(startup, 'r') as f:
            eval(compile(f.read(), startup, 'exec'), ctx)

    ctx.update(app.make_shell_context())

    IPython.embed(banner1=banner, user_ns=ctx)


@app.cli.command('run_https')
def run_https():
    #cert = 'cert/flask/cert.pem'
    #key = 'cert/flask/key.pem'
    #ctx = (cert, key)

    #app.run(ssl_context=ctx)
    app.run(ssl_context='adhoc', port=8443, debug=True)
