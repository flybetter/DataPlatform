from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return "hello world"

    from .house import houses as house_blueprint
    app.register_blueprint(house_blueprint)

    return app


if __name__ == '__main__':
    create_app()





