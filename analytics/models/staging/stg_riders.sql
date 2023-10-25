SELECT
    COALESCE(strava, slug) AS slug,
    name,
    bib,
    team,
    country,
    strava,
    height,
    weight,
    birthday
FROM {{ source('lake', 'riders') }}