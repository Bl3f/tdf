SELECT
    stage_id,
    index,
    latitude,
    longitude,
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
