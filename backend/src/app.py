from flask import Flask, jsonify
from flask_cors import CORS
from src.config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG, CORS_ORIGINS
from src.routes.logs import logs_bp
from src.routes.alerts import alerts_bp
from src.routes.stream import stream_bp

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": CORS_ORIGINS}})

    app.register_blueprint(logs_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(stream_bp)

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy'})

    return app

if __name__ == '__main__':
    app = create_app()
    print(f"🚀 API running at http://{FLASK_HOST}:{FLASK_PORT}")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
