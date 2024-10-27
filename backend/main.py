from flask import Flask
from markupsafe import escape
from dotenv import load_dotenv

from database.db import Db
from database.migration_manager import MigrationManager
from ssvc_score_evaluator import SsvcScoreEvaluator
from utils import dataclass_to_camelcase_dict

load_dotenv()

# Apply database migrations
migration_manager = MigrationManager(Db(), 'database/migrations')
migration_manager.migrate()

app = Flask(__name__)

ssvc = SsvcScoreEvaluator()


@app.route('/query/<string:cve_id>')
def query(cve_id: str):
    result = ssvc.evaluate(escape(cve_id))
    return dataclass_to_camelcase_dict(result)
