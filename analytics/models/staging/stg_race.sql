SELECT
    rider_slug,
    LPAD(CAST(stage_id AS STRING), 2, '0') AS stage_id,
    activity_id,
    updated_at,
    time,
    latitude,
    longitude,
    ST_GEOGPOINT(longitude, latitude) AS point,
    altitude,
    temp,
    watts,
    moving,
    velocity_smooth,
    grade_smooth,
    cadence,
    distance,
    heartrate
FROM {{ source('lake', 'race') }}
WHERE
    latitude BETWEEN -180 AND 180
    AND longitude BETWEEN -90  AND 90