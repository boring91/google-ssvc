import os
from typing import Optional, Tuple, Union
import logging
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool

logging.basicConfig(level=logging.INFO)


class Db:
    # Initialize a connection pool
    _pool = psycopg2.pool.SimpleConnectionPool(
        1, 20,  # Min and max connections in the pool
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

    def __enter__(self):
        # Get a connection from the pool
        self._conn = self._pool.getconn()
        self._cur = self._conn.cursor(cursor_factory=RealDictCursor)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._cur.close()
        # Return the connection back to the pool
        self._pool.putconn(self._conn)

    def execute(self,
                query: str,
                data: Optional[Union[Tuple, list]] = None) -> None:
        data = data or ()
        try:
            logging.info(f"Executing query: {query} with data: {data}")
            self._cur.execute(query, data)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            logging.error(f"Error executing query: {e}")
            raise

    def first(self,
              query: str,
              data: Optional[Union[Tuple, list]] = None) -> Optional[dict]:
        data = data or ()
        try:
            logging.info(f"Fetching first result for query: {query} with data: {data}")
            self._cur.execute(query, data)
            result = self._cur.fetchone()
            return dict(result) if result else None
        except Exception as e:
            logging.error(f"Error fetching first result: {e}")
            raise

    def query(self, query: str,
              data: Optional[Union[Tuple, list]] = None,
              index_column: Optional[str] = 'id') -> pd.DataFrame:
        data = data or ()
        try:
            logging.info(f"Fetching query: {query} with data: {data}")
            self._cur.execute(query, data)
            results = self._cur.fetchall()
            df = pd.DataFrame(results)

            if index_column and index_column in df.columns:
                df = df.set_index(index_column)

            return df
        except Exception as e:
            logging.error(f"Error executing query and fetching results: {e}")
            raise

    # Transaction management methods
    def begin(self):
        """Start a transaction."""
        self._conn.autocommit = False
        logging.info("Transaction started")

    def commit(self):
        """Commit the current transaction."""
        try:
            self._conn.commit()
            logging.info("Transaction committed")
        except Exception as e:
            self._conn.rollback()
            logging.error(f"Error during commit: {e}")
            raise

    def rollback(self):
        """Rollback the current transaction."""
        try:
            self._conn.rollback()
            logging.info("Transaction rolled back")
        except Exception as e:
            logging.error(f"Error during rollback: {e}")
            raise
