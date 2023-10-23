WITH stages_starts AS (
  SELECT stage_id, index, latitude, longitude
  FROM {{ ref("stg_stages_gpx") }}
  WHERE index = 0
),

stages_ends AS (
  SELECT stage_id, arg_max(latitude, index) AS latitude, arg_max(longitude, index) AS longitude
  FROM {{ ref("stg_stages_gpx") }}
  GROUP BY stage_id
),

joined AS (
  SELECT
    r.*,
    ss.latitude as start_latitude,
    ss.longitude as start_longitude,
    se.latitude as end_latitude,
    se.longitude as end_longitude
  FROM {{ ref("stg_race") }} r
  LEFT JOIN stages_starts ss ON r.stage_id = ss.stage_id
  LEFT JOIN stages_ends se ON r.stage_id = se.stage_id
),

-- const R = 6371e3; // metres
-- const φ1 = lat1 * Math.PI/180; // φ, λ in radians
-- const φ2 = lat2 * Math.PI/180;
-- const Δφ = (lat2-lat1) * Math.PI/180;
-- const Δλ = (lon2-lon1) * Math.PI/180;

-- const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
--           Math.cos(φ1) * Math.cos(φ2) *
--           Math.sin(Δλ/2) * Math.sin(Δλ/2);
-- const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

-- const d = R * c; // in metres

haversine_start AS (
    {{
        haversine(
            'joined',
            'start_latitude',
            'start_longitude',
            'latitude',
            'longitude',
        )
    }}
),

haversine_end AS (
    {{
        haversine(
            'joined',
            'end_latitude',
            'end_longitude',
            'latitude',
            'longitude',
        )
    }}
),

start_time AS (
  SELECT
    rider_slug, stage_id, arg_min(haversine_start.time, d) AS min_time
  FROM haversine_start
  GROUP BY rider_slug, stage_id
),

end_time AS (
  SELECT
    rider_slug, stage_id, arg_min(haversine_end.time, d) AS max_time
  FROM haversine_end
  GROUP BY rider_slug, stage_id
),

times AS (
  SELECT s.*, e.max_time, e.max_time - s.min_time  AS duration
  FROM start_time s
  LEFT JOIN end_time e ON s.rider_slug = e.rider_slug AND s.stage_id = e.stage_id
  ORDER BY s.rider_slug, s.stage_id
)

SELECT
  r.rider_slug,
  r.stage_id,
  r.time,
  r.latitude::DECIMAL(8,6) AS latitude,
  r.longitude::DECIMAL(8,6) AS longitude,
  t.min_time,
  t.max_time
FROM {{ ref("stg_race") }} r
LEFT JOIN times t ON r.rider_slug = t.rider_slug AND r.stage_id = t.stage_id
WHERE
  time >= t.min_time AND time <= t.max_time
  AND r.latitude BETWEEN -180 AND 180
  AND r.longitude BETWEEN -90  AND 90
ORDER BY r.rider_slug, r.stage_id, r.time
LIMIT 100