from flask import Flask
from multiprocessing import Queue


# sql_queue = Queue()


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return "hello world"

    from .house import houses as house_blueprint
    from .house import houses_v1 as houses_v1_blueprint
    app.register_blueprint(house_blueprint)
    app.register_blueprint(houses_v1_blueprint)
    app.config['SECRET_KEY'] = '365house'
    return app


if __name__ == '__main__':
    create_app()
