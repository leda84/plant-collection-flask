from flask import Flask;
from config import Config
from .site.routes import site
from .api.routes import api
from .authentication.routes import auth

app = Flask(__name__)
# Registering blueprint for routes
app.register_blueprint(site)
app.register_blueprint(api)
app.register_blueprint(auth)

app.config.from_object(Config)