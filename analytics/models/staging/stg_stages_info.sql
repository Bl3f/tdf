SELECT
    LPAD(CAST(stage AS STRING), 2, '0') AS stage,
    date,
    start_label,
    end_label
FROM {{ source('lake', 'stages_info') }}