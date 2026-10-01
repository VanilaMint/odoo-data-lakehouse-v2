import os
from dotenv import load_dotenv
from odoo_warehouse_v2.extract.pipeline import run_odoo_pipeline

def run_pipeline_scratch_test():
    # 1. Enable DLT Debug Logging to see the underlying SQL and Iceberg requests
    os.environ["DLT_RUNTIME__LOG_LEVEL"] = "DEBUG"
    
    print("1. Loading environment variables...")
    load_dotenv(".env.dev")
    
    # 2. Set the Airflow execution hour (must be ISO format with Z for UTC)
    # The pipeline will calculate the window from 06:00:00 to 07:00:00
    target_hour = "2026-09-29T06:00:00Z"
    
    print(f"2. Executing pipeline for window: {target_hour}...")
    
    # 3. Run the pipeline orchestrator
    info = run_odoo_pipeline(simulated_processing_hour=target_hour)
    
    print("\n--- Pipeline Execution Summary ---")
    print(info)

if __name__ == "__main__":
    run_pipeline_scratch_test()