SELECT
    name,
    slug,
    bib,
    team,
    country,
    strava,
    height,
    weight,
    birthday
FROM {{ source('lake', 'riders') }}