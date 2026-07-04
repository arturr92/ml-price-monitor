from flask import Flask
from dotenv import load_dotenv
from routes.dashboard import dashboard_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = __import__('os').getenv("SECRET_KEY", "dev-secret-key")

# Registrar blueprints
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(debug=True)
