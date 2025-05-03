from flask import Flask
from app.routes import pages, chat

def create_app():
    app = Flask(__name__)
    app.register_blueprint(pages.bp)
    app.register_blueprint(chat.bp)
    return app