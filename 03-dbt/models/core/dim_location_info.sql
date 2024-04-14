{{ config(materialized="table") }}

with unique_locations as (
        select 
            location_id,
            county,
            city,
            state_of_residence,
            zip,
            legislative_district
        from {{ ref("stg_electric_vehicles") }}
        GROUP BY 
            location_id,
            county,
            city,
            state_of_residence,
            zip,
            legislative_district
    )

select * from unique_locations
