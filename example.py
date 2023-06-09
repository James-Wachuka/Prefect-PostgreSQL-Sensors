from prefect import Flow, task
from prefect_postgres_sensors.sensors.postgres_sensors_copy import TableUpdatedSensor, RowCountSensor, ColumnChangeSensor, TableFragmentationSensor, DiskSpaceUsage, QueryPerformance

# Define your PostgreSQL connection parameters
conn_params = {
    "host": " ",
    "port": 5432,
    "database": " ",
    "user": " ",
    "password": " ",
}

@task
def process_data():
    print("Processing data...")

# Create a Prefect flow
with Flow("PostgreSQL Monitoring") as flow:
    last_updated_row = TableUpdatedSensor(table_name="users", conn_params=conn_params, last_updated_column="last_updated")
    row_count = RowCountSensor(table_name="users", conn_params=conn_params)
    changed_column = ColumnChangeSensor(table_name="users", column_name="name", conn_params=conn_params)
    table_fragmentation = TableFragmentationSensor(table_name="users", conn_params=conn_params)
    disk_space = DiskSpaceUsage(table_name="users", column_name="name", conn_params=conn_params)
    query_perf = QueryPerformance(table_name="users", column_name="name", conn_params=conn_params)
    process_task = process_data()


    # Connect the sensors and tasks
    last_updated_row.set_upstream(process_task)
    row_count.set_upstream(process_task)
    changed_column.set_upstream(process_task)
    table_fragmentation.set_upstream(process_task)
    disk_space.set_upstream(process_task)
    query_perf.set_upstream(process_task) 
# Run the flow
flow_result = flow.run()

# Print returned values from different flow runs
print("Table Updated Sensor Result:", flow_result.result[last_updated_row].result)
print("Row Count Sensor Result:", flow_result.result[row_count].result)
print("Column Change Sensor Result:", flow_result.result[changed_column].result)
print("Table fragmentation sensor result:", flow_result.result[table_fragmentation].result)
print("Disk Space Usage Sensor Result:", flow_result.result[disk_space].result)
print("Query Performance Sensor Result:", flow_result.result[query_perf].result)


