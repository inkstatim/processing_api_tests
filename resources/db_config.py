import os

db_processing_config = {
    'host': os.getenv('PG_DB_IP'),
    'port': os.getenv('PG_DB_PORT'),
    'user': 'processing',
    'password': os.getenv('PG_DB_PASSWORD'),
    'dbname': 'processing'
}
