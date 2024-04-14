{{ config(materialized="table") }}

with
    unique_vehicles as (
        select 
            vin,
            make,
            model,
            model_year,
            electric_vehicle_type,
            electric_range,
            vehicle_primary_use,
            base_msrp,
        from {{ ref("stg_electric_vehicles") }}
        group by 
            vin, 
            make,
            model,
            model_year,
            electric_vehicle_type,
            electric_range,
            vehicle_primary_use,
            base_msrp
    )

select 
*
from unique_vehicles
