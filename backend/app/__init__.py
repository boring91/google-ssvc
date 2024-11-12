import re

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from markupsafe import escape

from app.utils import dataclass_to_camelcase_dict
from config import Config

load_dotenv('./.env.dev')


def create_app(config_class=Config):
    from database.db import Db
    from database.migration_manager import MigrationManager

    migration_manager = MigrationManager(Db(), 'database/migrations')
    migration_manager.migrate()

    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, resources={
        r"/*": {
            "origins": [
                "http://localhost:4300",
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    @app.route('/query/<string:cve_id>')
    def query(cve_id: str):
        # Ensure that we have a valid cve_id:
        cve_id = cve_id.upper().strip()
        pattern = r'^(?:CVE|GO|HSEC|PYSEC)-\d{4}-\d{1,7}$'
        if not bool(re.match(pattern, cve_id)):
            return jsonify({
                "type": "https://example.com/probs/bad-request",
                "title": "Bad Request",
                "status": 400,
                "detail": "Invalid cve id format.",
            }), 400

        reevaluate = request.args.get('reevaluate', False, type=bool)

        from ssvc.ssvc_score_evaluator import SsvcScoreEvaluator
        ssvc = SsvcScoreEvaluator()
        result = ssvc.evaluate(escape(cve_id), reevaluate)

        if result is None:
            return jsonify({
                "type": "https://example.com/probs/bad-request",
                "title": "Bad Request",
                "status": 400,
                "detail": "Could not evaluate the cve.",
            }), 400

        return jsonify(dataclass_to_camelcase_dict(result))

    return app
