SELECT
    rider_slug,
    stage_id,
    activity_id,
    updated_at,
    time,
    latitude,
    longitude,
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