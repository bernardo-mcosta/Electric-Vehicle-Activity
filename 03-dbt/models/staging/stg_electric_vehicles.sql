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
        -- Identification
        {{ dbt_utils.generate_surrogate_key(['vin_1_10', 'transaction_date']) }} as transaction_id,
        vin_1_10,
        dol_vehicle_id,

        -- Vehicle information
        electric_vehicle_type,
        make,
        model,
        model_year,
        vehicle_primary_use,
        electric_range,
        odometer_reading,
        odometer_code,

        -- Dates
        cast(transaction_date as datetime) as transaction_date,
        transaction_year,
        cast(date_of_vehicle_sale as datetime) as sale_date,

        -- Transaction information
        transaction_type,
        new_or_used_vehicle,
        sale_price,
        base_msrp,
        county,
        city,
        state_of_residence,
        zip,
        legislative_district,
    from source
)

select * from renamed

-- dbt build --select stg_electric_vehicles.sql --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 1000

{% endif %}