{{
    config(
        materialized='view'
    )
}}

with 

source as (

    select * from {{ source('staging', 'electric_vehicles_data') }}

),

renamed as (

    select
        -- Transaction information
         {{ dbt_utils.generate_surrogate_key(['vin_1_10', 'transaction_date']) }} as transaction_id,   
        cast(transaction_date as datetime) as transaction_date,
        transaction_year,
        cast(date_of_vehicle_sale as datetime) as sale_date,
        transaction_type,
        sale_price,
        new_or_used_vehicle,
        odometer_reading,
        odometer_code,

        -- Vehicle information
        vin_1_10 as vin,
        dol_vehicle_id,
        electric_vehicle_type,
        make,
        model,
        model_year,
        vehicle_primary_use,
        electric_range,
        base_msrp,

        -- Location information
        {{ dbt_utils.generate_surrogate_key(['zip', 'city', 'state_of_residence']) }} as location_id,   
        county,
        city,
        state_of_residence,
        zip,
        legislative_district,

    from source
)

select * from renamed