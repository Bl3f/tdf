WITH stages_starts AS (
  SELECT stage_id, point
  FROM {{ ref("stg_stages_gpx") }}
  WHERE index = 0
),

stages_ends AS (
  SELECT stage_id, MAX_BY(point, index) AS point
  FROM {{ ref("stg_stages_gpx") }}
  GROUP BY stage_id
),

joined AS (
  SELECT
    r.*,
    ss.point AS start_point,
    se.point AS end_point
  FROM {{ ref("stg_race") }} r
  LEFT JOIN stages_starts ss ON r.stage_id = ss.stage_id
  LEFT JOIN stages_ends se ON r.stage_id = se.stage_id
),

distances AS (
  SELECT
    *,
    ST_DISTANCE(point, start_point) AS start_distance,
    ST_DISTANCE(point, end_point) AS end_distance
  FROM joined
),

times AS (
  SELECT
    rider_slug,
    stage_id,
    MIN_BY(time, start_distance) AS start_time,
    MIN_BY(time, end_distance) AS end_time
  FROM distances
  GROUP BY rider_slug, stage_id
)

SELECT
  CONCAT(r.rider_slug, '-', r.stage_id) AS id,
  r.rider_slug,
  r.stage_id,
  MAX(t.end_time - t.start_time) AS duration,
  ARRAY_AGG(TO_JSON(STRUCT(r.time - t.start_time AS t, r.point AS coordinates, r.heartrate AS heartrate)) ORDER BY r.time - t.start_time ASC) AS points,
  ST_MAKELINE(ARRAY_AGG(IF(MOD(CAST(r.time - t.start_time AS INT64), 3) = 0, r.point, NULL) IGNORE NULLS ORDER BY r.time - t.start_time ASC)) AS line
FROM {{ ref("stg_race") }} r
LEFT JOIN times t ON r.rider_slug = t.rider_slug AND r.stage_id = t.stage_id
WHERE
  r.time >= t.start_time AND time <= t.end_time
GROUP BY id, r.rider_slug, r.stage_id
