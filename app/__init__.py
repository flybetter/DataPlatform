from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return "hello world"

    from .newhouse import newhouses as newhouse_blueprint
    from .secondhouse import secondhouses as secondhouse_blueprint
    app.register_blueprint(newhouse_blueprint)
    app.register_blueprint(secondhouse_blueprint)
    return app


if __name__ == '__main__':
    create_app()
