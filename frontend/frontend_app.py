from flask import Flask, render_template


class FrontendApp:
    """This class handles the front end"""

    def __init__(self):
        """This code initializes everything"""
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        """This code sets up routes"""
        self.app.route('/', methods=['GET'])(self.home)

    @staticmethod
    def home():
        """This code just handles the front end"""
        return render_template("index.html")

    def run(self):
        """This starts the server"""
        self.app.run(host="0.0.0.0", port=5001, debug=True)


if __name__ == '__main__':
    my_app = FrontendApp()
    my_app.run()
