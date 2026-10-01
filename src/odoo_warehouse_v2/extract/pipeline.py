from datetime import datetime, timedelta, timezone

import dlt

from odoo_warehouse_v2.extract.connections import configure_iceberg_environment
from odoo_warehouse_v2.extract.models import get_modeled_odoo_source


def run_odoo_pipeline(simulated_processing_hour: str):
    """
    Orchestrates the extraction of Odoo data for a specific hour, pushes a SQL 
    window filter to Postgres, and overwrites that hour's partition in Iceberg.
    """

    processing_time = datetime.now(timezone.utc)
    

    start_time_aware = datetime.fromisoformat(simulated_processing_hour.replace("Z", "+00:00"))
    start_time = start_time_aware.replace(tzinfo=None)
    end_time = start_time + timedelta(hours=1)
    

    destination_name = configure_iceberg_environment()
    

    pipeline = dlt.pipeline(
        pipeline_name="odoo_to_iceberg",
        destination=destination_name,
        dataset_name="raw_odoo"
    )
    

    source = get_modeled_odoo_source(
        processing_time=processing_time,
        simulated_processing_hour=simulated_processing_hour
    )
    

    for resource in source.resources.values():
        resource.apply_hints(
            incremental=dlt.sources.incremental(
                "write_date", 
                initial_value=start_time, 
                end_value=end_time
            )
        )
    
    info = pipeline.run(source, 
                        write_disposition="replace",
                        table_format="iceberg")
    
    return info