{{ config(materialized='table') }}

with transaction_data as (
    select
        transaction_id,   
        sale_price,
        transaction_date,
        transaction_year,
        sale_date,
        transaction_type,
        new_or_used_vehicle,
        odometer_reading,
        odometer_code,
        vin,
        location_id,
    from
        {{ ref("stg_electric_vehicles") }}
)

select  
        td.transaction_id,   
        td.sale_price,
        td.transaction_date,
        td.transaction_year,
        td.sale_date,
        td.transaction_type,
        td.new_or_used_vehicle,
        td.odometer_reading,
        td.odometer_code,
        
        -- location info
        td.location_id,
        l.county,
        l.city,
        l.state_of_residence,
        l.zip,
        l.legislative_district,

        --vehicle info
        td.vin,
        v.electric_vehicle_type,
        v.make,
        v.model,
        v.model_year,
        v.vehicle_primary_use,
        v.electric_range,
        v.base_msrp

from transaction_data td
left join 
    {{ ref("dim_location_info") }} l ON td.location_id = l.location_id
left join 
    {{ ref("dim_vechile_info") }} v ON td.vin = v.vin