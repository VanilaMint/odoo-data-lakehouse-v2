import os

from dlt.sources.sql_database import sql_database


def get_odoo_source():
    """
    Returns a DLT source for extracting data from an Odoo database.
    The source is configured using environment variables for the database connection.
    """
    db_host = os.getenv("ODOO_DB_HOST", "localhost")
    db_port = os.getenv("ODOO_DB_PORT", "5432")
    db_name = os.getenv("ODOO_DB_NAME", "odoo_db")
    db_user = os.getenv("ODOO_DB_USER", "odoo")
    db_password = os.getenv("ODOO_DB_PASSWORD", "odoo")

    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return sql_database(
        credentials=connection_string,
        schema="public"
    )

def configure_iceberg_environment():
    nessie_host = os.getenv("NESSIE_HOST", "localhost")
    nessie_port = os.getenv("NESSIE_PORT", "19120")
    
    minio_host = os.getenv("MINIO_HOST", "localhost")
    minio_port = os.getenv("MINIO_PORT", "9000")
    minio_user = os.getenv("MINIO_USER", "admin")
    minio_password = os.getenv("MINIO_PASSWORD", "password")
    minio_bucket = os.getenv("MINIO_BUCKET", "warehouse")
    
    minio_endpoint = f"http://{minio_host}:{minio_port}"
    s3_warehouse_path = f"s3://{minio_bucket}"

    # --- 1. DLT Filesystem Configuration ---
    os.environ["DESTINATION__FILESYSTEM__BUCKET_URL"] = s3_warehouse_path
    os.environ["DESTINATION__FILESYSTEM__CREDENTIALS__ENDPOINT_URL"] = minio_endpoint
    os.environ["DESTINATION__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID"] = minio_user
    os.environ["DESTINATION__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY"] = minio_password


    os.environ["ICEBERG_CATALOG__ICEBERG_CATALOG_NAME"] = "default"
    os.environ["ICEBERG_CATALOG__ICEBERG_CATALOG_TYPE"] = "rest"

    os.environ["PYICEBERG_CATALOG__DEFAULT__TYPE"] = "rest"
    os.environ["PYICEBERG_CATALOG__DEFAULT__URI"] = f"http://{nessie_host}:{nessie_port}/iceberg"
    os.environ["PYICEBERG_CATALOG__DEFAULT__WAREHOUSE"] = s3_warehouse_path
    os.environ["PYICEBERG_CATALOG__DEFAULT__PY_IO_IMPL"] = "pyiceberg.io.fsspec.FsspecFileIO"
    os.environ["PYICEBERG_CATALOG__DEFAULT__S3__ENDPOINT"] = minio_endpoint
    os.environ["PYICEBERG_CATALOG__DEFAULT__S3__ACCESS_KEY_ID"] = minio_user
    os.environ["PYICEBERG_CATALOG__DEFAULT__S3__SECRET_ACCESS_KEY"] = minio_password
    os.environ["PYICEBERG_CATALOG__DEFAULT__S3__REGION"] = "us-east-1"
    os.environ["PYICEBERG_CATALOG__DEFAULT__S3__PATH_STYLE_ACCESS"] = "true"
    
    return "filesystem"