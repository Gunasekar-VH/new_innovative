from flask import Flask, render_template
from models import db, init_db
from auth import auth_bp
from admin import admin_bp
from user import user_bp


def create_app():
    app = Flask(__name__)

    # Application settings
    app.config["SECRET_KEY"] = "change-this-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)

    # Initialize database
    with app.app_context():
        init_db()

    # Home page
    @app.route("/")
    def home():
        return render_template("index.html")

    return app


# Create Flask application
app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```



app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
