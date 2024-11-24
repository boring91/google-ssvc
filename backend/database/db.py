import os
from typing import Optional, Tuple, Union
import logging
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

    # Initialize a connection pool
    _pool = psycopg2.pool.SimpleConnectionPool(
        1, 20,  # Min and max connections in the pool
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

    def __init__(self):
        """Initialize the database connection manager with a logger."""
        self._logger = logging.getLogger(self.__class__.__name__)

    def __enter__(self):
        """
        Context manager entry point. Acquires a connection from the pool.

        Returns:
            Db: The database connection manager instance.
        """
        self._conn = self._pool.getconn()
        self._cur = self._conn.cursor(cursor_factory=RealDictCursor)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Context manager exit point. Closes the cursor and returns the connection to the pool.

        Args:
            exc_type: Exception type if an exception occurred
            exc_value: Exception value if an exception occurred
            traceback: Traceback if an exception occurred
        """
        self._cur.close()
        self._pool.putconn(self._conn)

    def execute(self,
                query: str,
                data: Optional[Union[Tuple, list]] = None) -> None:
        """
        Execute a SQL query with optional parameters.

        Args:
            query: SQL query string with optional placeholders
            data: Parameters to substitute into the query (default: None)

        Raises:
            Exception: If query execution fails

        Examples:
            >>> db.execute("UPDATE users SET active = %s WHERE id = %s", (True, 1))
        """
        data = data or ()
        try:
            self._logger.info(f"Executing query: {query} with data: {data}")
            self._cur.execute(query, data)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            self._logger.error(f"Error executing query: {e}")
            raise

    def first(self,
              query: str,
              data: Optional[Union[Tuple, list]] = None) -> Optional[dict]:
        """
        Execute a query and return the first result as a dictionary.

        Args:
            query: SQL query string with optional placeholders
            data: Parameters to substitute into the query (default: None)

        Returns:
            Optional[dict]: First row as a dictionary or None if no results

        Raises:
            Exception: If query execution fails

        Examples:
            >>> user = db.first("SELECT * FROM users WHERE id = %s", (1,))
            >>> if user:
            >>>     print(user['name'])
        """
        data = data or ()
        try:
            self._logger.info(f"Fetching first result for query: {query} with data: {data}")
            self._cur.execute(query, data)
            result = self._cur.fetchone()
            return dict(result) if result else None
        except Exception as e:
            self._logger.error(f"Error fetching first result: {e}")
            raise

    def query(self,
              query: str,
              data: Optional[Union[Tuple, list]] = None,
              index_column: Optional[str] = 'id') -> pd.DataFrame:
        """
        Execute a query and return all results as a pandas DataFrame.

        Args:
            query: SQL query string with optional placeholders
            data: Parameters to substitute into the query (default: None)
            index_column: Column to use as DataFrame index (default: 'id')

        Returns:
            pd.DataFrame: Query results as a pandas DataFrame

        Raises:
            Exception: If query execution fails

        Examples:
            >>> df = db.query("SELECT * FROM users WHERE active = %s", (True,))
            >>> active_users = len(df)
        """
        data = data or ()
        try:
            self._logger.info(f"Fetching query: {query} with data: {data}")
            self._cur.execute(query, data)
            results = self._cur.fetchall()
            df = pd.DataFrame(results)

            if index_column and index_column in df.columns:
                df = df.set_index(index_column)

            return df
        except Exception as e:
            self._logger.error(f"Error executing query and fetching results: {e}")
            raise

    def begin(self):
        """
        Start a transaction by disabling autocommit.

        Examples:
            >>> db.begin()
            >>> try:
            >>>     db.execute("INSERT INTO users (name) VALUES (%s)", ("Alice",))
            >>>     db.execute("UPDATE counts SET user_count = user_count + 1")
            >>>     db.commit()
            >>> except:
            >>>     db.rollback()
        """
        self._conn.autocommit = False
        self._logger.info("Transaction started")

    def commit(self):
        """
        Commit the current transaction.

        Raises:
            Exception: If commit fails

        Examples:
            >>> db.begin()
            >>> db.execute("INSERT INTO users (name) VALUES (%s)", ("Alice",))
            >>> db.commit()
        """
        try:
            self._conn.commit()
            self._logger.info("Transaction committed")
        except Exception as e:
            self._conn.rollback()
            self._logger.error(f"Error during commit: {e}")
            raise

    def rollback(self):
        """
        Rollback the current transaction.

        Raises:
            Exception: If rollback fails

        Examples:
            >>> db.begin()
            >>> try:
            >>>     db.execute("BAD SQL")
            >>> except:
            >>>     db.rollback()
        """
        try:
            self._conn.rollback()
            self._logger.info("Transaction rolled back")
        except Exception as e:
            self._logger.error(f"Error during rollback: {e}")
            raise
