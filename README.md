# TeSLA API
## Use with Flask app

```python
from flask import Flask
app = Flask(__name__)

# Connect with SQLAlchemy
from tesla_models import init_tesla_db
tesla_db = init_tesla_db(app)
```
