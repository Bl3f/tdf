SELECT
    *,
    ST_LENGTH(path) AS distance
FROM {{ ref('stg_stages_info') }}