import re
from io import StringIO

import pandas as pd
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, UploadFile, File, Query, Path
from fastapi.middleware.cors import CORSMiddleware

from app.utils import dataclass_to_camelcase_dict

load_dotenv('./.env.dev')


def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application with SSVC evaluation endpoints.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    # Apply db migrations.
    from database.db import Db
    from database.migration_manager import MigrationManager

    migration_manager = MigrationManager(Db(), 'database/migrations')
    migration_manager.migrate()

    app = FastAPI(
        title="SSVC Evaluation API",
        description="""
        API for evaluating Common Vulnerabilities and Exposures (CVEs) using the 
        Stakeholder-Specific Vulnerability Categorization (SSVC) methodology.
        """,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1}  # This hides the schemas section
    )

    # noinspection PyTypeChecker
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:4300'],
        allow_methods=['*'],
        allow_headers=['*'],
    )

    @app.get(
        '/ssvc/evaluate/{cve_id}',
        summary="Evaluate single CVE",
        description="""
        Evaluates a single CVE using the SSVC methodology.
        The CVE ID must follow the format: CVE-YYYY-NNNNNNN, GO-YYYY-NNNNNNN, 
        HSEC-YYYY-NNNNNNN, or PYSEC-YYYY-NNNNNNN.
        """
    )
    def query(
            cve_id: str = Path(..., example="CVE-2024-12345", description="The CVE identifier to evaluate"),
            reevaluate: bool = Query(False, description="Force re-evaluation even if results exist")
    ):
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

    @app.get(
        '/ssvc/bulk-evaluate',
        summary="List bulk evaluation tasks",
        description="Retrieves a list of all bulk evaluation tasks and their current status."
    )
    async def list_bulk_evaluate_tasks():
        from app.ssvc_task_service import SsvcTaskService
        service = SsvcTaskService()
        return dataclass_to_camelcase_dict(service.list())

    @app.get(
        '/ssvc/bulk-evaluate/{task_id}',
        summary="Get bulk evaluation task status",
        description="Retrieves the status and results of a specific bulk evaluation task."
    )
    async def get_bulk_evaluate_task(
            task_id: str = Path(..., description="The unique identifier of the bulk evaluation task")
    ):
        from app.ssvc_task_service import SsvcTaskService
        service = SsvcTaskService()

        task = service.get(task_id)
        if task is None:
            raise HTTPException(404, 'Task not found.')

        return dataclass_to_camelcase_dict(task)

    @app.post(
        '/ssvc/bulk-evaluate',
        summary="Submit bulk evaluation task",
        description="""
        Submits a CSV file containing CVE IDs for bulk evaluation.
        The CSV file must contain exactly one column with CVE IDs.
        """
    )
    async def bulk_evaluate(
            file: UploadFile = File(..., description="CSV file containing CVE IDs"),
            reevaluate: bool = Query(False, description="Force re-evaluation of existing results")
    ):
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
