{% macro haversine(table, start_latitude, start_longitude, latitude, longitude) -%}

SELECT
    {{ table }}.*,
    6371 * pow(10, 3) as R,
    {{ latitude }} * pi() /180 as phi1,
    {{ start_latitude }} * pi() /180 as phi2,
    ({{ start_latitude }} - {{ latitude }}) * pi() / 180 deltaphi,
    ({{ start_longitude }} - {{ longitude }}) * pi() / 180 deltalambda,
    sin(deltaphi / 2) * sin(deltaphi / 2) + cos(phi1) * cos(phi2) * sin(deltalambda / 2) * sin(deltalambda /2) as a,
    2 * atan2(sqrt(a), sqrt(1 - a)) as c,
    R * c as d
FROM {{ table }}

{%- endmacro %}