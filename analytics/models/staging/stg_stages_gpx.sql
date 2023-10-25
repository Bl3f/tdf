SELECT
    stage_id,
    index,
    latitude,
    longitude,
    ST_GEOGPOINT(longitude, latitude) AS point,
    altitude,
    slope,
    dvdone,
    dvrest,
    kmdone,
    kmto,
    cpnumero,
    cptype,
    sumcategory
FROM {{ source('lake', 'stages') }} AS stages
