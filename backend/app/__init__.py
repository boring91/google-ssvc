import re
from io import StringIO

import pandas as pd
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.utils import dataclass_to_camelcase_dict

load_dotenv('./.env.dev')


def create_app() -> FastAPI:
    # Apply db migrations.
    from database.db import Db
    from database.migration_manager import MigrationManager

    migration_manager = MigrationManager(Db(), 'database/migrations')
    migration_manager.migrate()

    app = FastAPI()

    # noinspection PyTypeChecker
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:4300'],
        allow_methods=['*'],
        allow_headers=['*'],
    )

    # Create the endpoints.
    @app.get('/ssvc/evaluate/{cve_id}')
    def query(cve_id: str, reevaluate: bool = False):
        # Ensure that we have a valid cve_id:
        cve_id = cve_id.upper().strip()
        pattern = r'^(?:CVE|GO|HSEC|PYSEC)-\d{4}-\d{1,7}$'
        if not bool(re.match(pattern, cve_id)):
            raise HTTPException(400, detail='Invalid cve id format.')

        from ssvc.ssvc_score_evaluator import SsvcScoreEvaluator
        ssvc = SsvcScoreEvaluator()
        result = ssvc.evaluate(cve_id, reevaluate)

        if result is None:
            raise HTTPException(400, detail='Could not evaluate the cve.')

        return dataclass_to_camelcase_dict(result[1])

    @app.get('/ssvc/bulk-evaluate')
    async def list_bulk_evaluate_tasks():
        from app.ssvc_task_service import SsvcTaskService
        service = SsvcTaskService()

        return dataclass_to_camelcase_dict(service.list())

    @app.get('/ssvc/bulk-evaluate/{task_id}')
    async def get_bulk_evaluate_task(task_id: str):
        from app.ssvc_task_service import SsvcTaskService
        service = SsvcTaskService()

        task = service.get(task_id)

        if task is None:
            raise HTTPException(404, 'Task not found.')

        return dataclass_to_camelcase_dict(task)

    @app.post('/ssvc/bulk-evaluate')
    async def bulk_evaluate(file: UploadFile, reevaluate: bool = False):
        if not file.filename.endswith('.csv'):
            raise HTTPException(400, 'File must be CSV.')
        try:
            contents = await file.read()
            df = pd.read_csv(StringIO(contents.decode()), header=None)

            # Check if only one column
            if len(df.columns) != 1:
                raise HTTPException(400, 'CSV must have exactly one column.')

            from app.ssvc_task_service import SsvcTaskService
            service = SsvcTaskService()

            return {'taskId': service.submit(df, reevaluate)}

        except pd.errors.EmptyDataError:
            raise HTTPException(400, 'CSV file is empty.')
        except Exception as e:
            raise HTTPException(400, f'Invalid CSV format: {str(e)}')

    return app
