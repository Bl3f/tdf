SELECT count(distinct rider_slug)
FROM {{ source('lake', 'race') }}