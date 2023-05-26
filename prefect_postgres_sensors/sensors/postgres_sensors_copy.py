from prefect import Task
import psycopg2
from psycopg2 import sql
import time


class TableUpdatedSensor(Task):
    def __init__(self, table_name, conn_params,last_updated_column):
        self.table_name = table_name
        self.last_updated_column = last_updated_column
        self.conn_params = conn_params
        super().__init__()

    def run(self):
        conn = psycopg2.connect(**self.conn_params)
        cursor = conn.cursor()
        query = f"SELECT {self.last_updated_column} FROM {self.table_name} ORDER BY {self.last_updated_column} DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        last_updated = result[0] if result else None
        conn.close()
        return last_updated


class RowCountSensor(Task):
    def __init__(self, table_name, conn_params):
        self.table_name = table_name
        self.conn_params = conn_params
        super().__init__()

    def run(self):
        conn = psycopg2.connect(**self.conn_params)
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        count = cursor.fetchone()[0]
        conn.close()
        return count


class ColumnChangeSensor(Task):
    def __init__(self, table_name, column_name, conn_params):
        self.table_name = table_name
        self.column_name = column_name
        self.conn_params = conn_params
        super().__init__()

    def run(self):
        conn = psycopg2.connect(**self.conn_params)
        cursor = conn.cursor()
        cursor.execute(f"SELECT {self.column_name} FROM {self.table_name} LIMIT 1")
        value = cursor.fetchone()[0]
        conn.close()
        return value
    
class TableFragmentationSensor(Task):
    def __init__(self, table_name, conn_params):
        self.table_name = table_name
        self.conn_params = conn_params
        super().__init__()

    def run(self):
        conn = psycopg2.connect(**self.conn_params)
        cursor = conn.cursor()
        cursor.execute(f"SELECT pg_size_pretty(pg_total_relation_size('{self.table_name}'))")
        fragmentation_size = cursor.fetchone()[0]
        conn.close()
        return fragmentation_size
    




class DiskSpaceUsage(Task):
    def __init__(self, table_name, column_name, conn_params):
        self.table_name = table_name
        self.column_name = column_name
        self.conn_params = conn_params
        super().__init__()

    def run(self):
        conn = psycopg2.connect(**self.conn_params)
        cursor = conn.cursor()

        # Retrieve the disk space usage of the table and its indexes
        query = sql.SQL("""
            SELECT pg_size_pretty(pg_total_relation_size(%s)) AS total_size,
                   pg_size_pretty(pg_total_relation_size(pg_indexes_size(%s))) AS index_size
            FROM pg_class
            WHERE relname = %s
        """)
        cursor.execute(query, [self.table_name, self.table_name, self.table_name])
        result = cursor.fetchone()
        total_size = result[0] if result else None
        index_size = result[1] if result else None

        conn.close()
        size_index=[]
        size_index.append(total_size)
        size_index.append(index_size)
        return size_index




class QueryPerformance(Task):
    def __init__(self, table_name, column_name, conn_params):
        self.table_name = table_name
        self.column_name = column_name
        self.conn_params = conn_params
        super().__init__()

    def run(self):
        conn = psycopg2.connect(**self.conn_params)
        cursor = conn.cursor()

        # Start monitoring query performance
        start_time = time.time()

        cursor.execute(f"SELECT {self.column_name} FROM {self.table_name} LIMIT 1")
        value = cursor.fetchone()[0]

        # End monitoring query performance
        end_time = time.time()
        execution_time = end_time - start_time

        # Get additional performance metrics
        query_metrics = cursor.statusmessage

        conn.close()

        # Return value and performance metrics
        values=[]
        values.append(execution_time)
        values.append(query_metrics)
        return values