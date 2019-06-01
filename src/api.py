from flask import Flask
from src.controller.simple_page import simple_page
from src.controller.UserController import user_controller

app = Flask(__name__)
app.register_blueprint(simple_page)
app.register_blueprint(user_controller)

if __name__ == "__main__":
    app.run(debug=True)
