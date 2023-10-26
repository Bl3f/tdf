SELECT
    *,
    ST_LENGTH(g.path) AS distance
FROM {{ ref('stg_stages_info') }}