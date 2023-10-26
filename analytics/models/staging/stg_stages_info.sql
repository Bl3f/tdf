WITH stages_gpx AS (
    SELECT
        stage_id,
        ST_MAKELINE(ARRAY_AGG(point ORDER BY index ASC)) AS path
    FROM {{ ref('stg_stages_gpx') }}
    GROUP BY stage_id
)

SELECT
    LPAD(CAST(stage AS STRING), 2, '0') AS stage,
    date,
    start_label,
    end_label,
    g.path
FROM {{ source('lake', 'stages_info') }} i
LEFT JOIN stages_gpx g ON LPAD(CAST(i.stage AS STRING), 2, '0') = g.stage_id