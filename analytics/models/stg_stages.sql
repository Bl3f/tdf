SELECT *
FROM {{ source('lake', 'stages') }} AS stages
LEFT JOIN {{ source('lake', 'stages_info') }} AS stages_info ON stages.stage_id = stages_info.stage