from datetime import datetime

from dlt.destinations.adapters import iceberg_adapter

from odoo_warehouse_v2.extract.connections import get_odoo_source


def get_modeled_odoo_source(processing_time: datetime, simulated_processing_hour: datetime):
    """
    Imports the raw Postgres source, filters it to the 5 core tables,
    injects Airflow metadata as native datetimes, and applies Iceberg partitioning.
    """
    raw_source = get_odoo_source()
    
    modeled_source = raw_source.with_resources(
        "res_partner",
        "product_template",
        "product_product",
        "sale_order",
        "sale_order_line"
    )
    
    def inject_airflow_metadata(row):
        row["processing_time"] = processing_time
        row["simulated_processing_hour"] = simulated_processing_hour
        return row
    
    for resource in modeled_source.resources.values():
        resource.add_map(inject_airflow_metadata)
        resource.apply_hints(primary_key=["id", "write_date", "processing_time"])
        iceberg_adapter(
            resource,
            partition="simulated_processing_hour"
        )
        
    return modeled_source