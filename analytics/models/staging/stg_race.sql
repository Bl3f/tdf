SELECT
    rider_slug,
    stage_id,
    activity_id,
    updated_at,
    time,
    latitude::DECIMAL(8,6),
    longitude::DECIMAL(8,6),
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