import os
import time
import logging
from typing import Optional, Tuple, Union
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool


class Db:
    """
    A database connection manager using connection pooling for PostgreSQL.
    Provides a context manager interface and methods for common database operations.

    The class uses environment variables for database configuration:
    - DB_NAME: Database name
    - DB_USER: Database user
    - DB_PASS: Database password
    - DB_HOST: Database host
    - DB_PORT: Database port

    Examples:
        >>> with Db() as db:
        >>>     results = db.query("SELECT * FROM users WHERE active = %s", (True,))
        >>>     first_user = db.first("SELECT * FROM users LIMIT 1")
    """

    _pool = None  # Initialize as None first

    @classmethod
    def _init_pool(cls):
        """Initialize the connection pool with robust connection parameters."""
        connect_params = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASS'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'connect_timeout': 10,
            'gssencmode': 'disable',  # Disable Kerberos authentication
            'keepalives': 1,
            'keepalives_idle': 30,
            'keepalives_interval': 10,
            'keepalives_count': 5,
            'application_name': 'your_app_name'
        }

        try:
            return psycopg2.pool.SimpleConnectionPool(1, 20, **connect_params)
        except Exception as e:
            logging.error(f"Failed to initialize connection pool: {e}")
            raise

    def __init__(self):
        """Initialize the database connection manager with a logger."""
        self._logger = logging.getLogger(self.__class__.__name__)
        if Db._pool is None:
            Db._pool = self._init_pool()
        self._conn = None
        self._cur = None

    def __enter__(self):
        """
        Context manager entry point. Acquires a connection from the pool with retry logic.

        Returns:
            Db: The database connection manager instance.
        """
        retry_count = 3
        last_exception = None

        while retry_count > 0:
            try:
                self._conn = self._pool.getconn()

                # Validate connection is still alive
                with self._conn.cursor() as test_cur:
                    test_cur.execute('SELECT 1')

                self._cur = self._conn.cursor(cursor_factory=RealDictCursor)
                return self

            except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
                last_exception = e
                retry_count -= 1
                self._logger.warning(f"Connection attempt failed, retries left: {retry_count}", exc_info=True)

                # If we got a connection but it was bad, return it to the pool
                if self._conn is not None:
                    # noinspection PyBroadException
                    try:
                        self._pool.putconn(self._conn, close=True)
                    except:
                        pass

                if retry_count > 0:
                    time.sleep(1)  # Wait before retrying

        self._logger.error("Failed to establish database connection after 3 attempts")
        raise last_exception

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Context manager exit point. Closes the cursor and returns the connection to the pool.
        """
        if self._cur is not None:
            # noinspection PyBroadException
            try:
                self._cur.close()
            except:
                pass

        if self._conn is not None:
            # noinspection PyBroadException
            try:
                self._pool.putconn(self._conn)
            except:
                pass

    def _check_connection(self):
        """Verify connection is still valid"""
        try:
            with self._conn.cursor() as test_cur:
                test_cur.execute('SELECT 1')
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            # Connection is bad, try to get a new one
            self._conn = self._pool.getconn()
            self._cur = self._conn.cursor(cursor_factory=RealDictCursor)

    def execute(self, query: str, data: Optional[Union[Tuple, list]] = None) -> None:
        """
        Execute a SQL query with optional parameters.

        Args:
            query: SQL query string with optional placeholders
            data: Parameters to substitute into the query (default: None)

        Raises:
            Exception: If query execution fails
        """
        data = data or ()
        try:
            self._check_connection()
            self._logger.info(f"Executing query: {query} with data: {data}")
            self._cur.execute(query, data)
            self._conn.commit()
        except psycopg2.Error as e:
            self._conn.rollback()
            self._logger.error(f"Database error executing query: {e}")
            raise
        except Exception as e:
            self._conn.rollback()
            self._logger.error(f"Unexpected error executing query: {e}")
            raise

    def first(self, query: str, data: Optional[Union[Tuple, list]] = None) -> Optional[dict]:
        """
        Execute a query and return the first result as a dictionary.

        Args:
            query: SQL query string with optional placeholders
            data: Parameters to substitute into the query (default: None)

        Returns:
            Optional[dict]: First row as a dictionary or None if no results
        """
        data = data or ()
        try:
            self._check_connection()
            self._logger.info(f"Fetching first result for query: {query} with data: {data}")
            self._cur.execute(query, data)
            result = self._cur.fetchone()
            return dict(result) if result else None
        except Exception as e:
            self._logger.error(f"Error fetching first result: {e}")
            raise

    def query(self, query: str, data: Optional[Union[Tuple, list]] = None,
              index_column: Optional[str] = 'id') -> pd.DataFrame:
        """
        Execute a query and return all results as a pandas DataFrame.

        Args:
            query: SQL query string with optional placeholders
            data: Parameters to substitute into the query (default: None)
            index_column: Column to use as DataFrame index (default: 'id')

        Returns:
            pd.DataFrame: Query results as a pandas DataFrame
        """
        data = data or ()
        try:
            self._check_connection()
            self._logger.info(f"Fetching query: {query} with data: {data}")
            self._cur.execute(query, data)
            results = self._cur.fetchall()
            df = pd.DataFrame(results)

            if len(df) > 0 and index_column and index_column in df.columns:
                df = df.set_index(index_column)

            return df
        except Exception as e:
            self._logger.error(f"Error executing query and fetching results: {e}")
            raise

    def begin(self):
        """Start a transaction by disabling autocommit."""
        self._check_connection()
        self._conn.autocommit = False
        self._logger.info("Transaction started")

    def commit(self):
        """Commit the current transaction."""
        try:
            self._check_connection()
            self._conn.commit()
            self._logger.info("Transaction committed")
        except Exception as e:
            self._conn.rollback()
            self._logger.error(f"Error during commit: {e}")
            raise

    def rollback(self):
        """Rollback the current transaction."""
        try:
            if self._conn is not None:
                self._conn.rollback()
                self._logger.info("Transaction rolled back")
        except Exception as e:
            self._logger.error(f"Error during rollback: {e}")
            raise

    @classmethod
    def close_all_connections(cls):
        """Close all connections in the pool"""
        if cls._pool is not None:
            cls._pool.closeall()
            cls._pool = None

    @classmethod
    def cleanup_pool(cls):
        """
        Clean up the connection pool - call this in Celery task_postrun
        """
        if cls._pool is not None:
            # noinspection PyBroadException
            try:
                # Remove any stale connections
                cls._pool._connect_pool = [
                    conn for conn in cls._pool._connect_pool
                    if not conn.closed
                ]
            except:
                # If cleanup fails, close everything
                cls.close_all_connections()
