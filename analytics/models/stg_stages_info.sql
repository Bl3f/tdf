SELECT
    stage,
    date,
    start_label,
    end_label
FROM {{ source('lake', 'stages_info') }}