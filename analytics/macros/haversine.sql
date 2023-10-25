{%- macro delta(start, current) -%}
    ({{ start }} - {{ current }}) * ACOS(-1) / 180
{%- endmacro -%}

{% macro haversine(table, start_latitude, start_longitude, latitude, longitude) -%}

SELECT
    {{ table }}.*,
    6371 * pow(10, 3) as R,
    {{ latitude }} * ACOS(-1) /180 as phi1,
    {{ start_latitude }} * ACOS(-1) /180 as phi2,
    delta({{ start_latitude }}, {{ latitude }}) AS deltaphi,
    ({{ start_longitude }} - {{ longitude }}) * ACOS(-1) / 180 deltalambda,
    sin(deltaphi / 2) * sin(deltaphi / 2) + cos(phi1) * cos(phi2) * sin(deltalambda / 2) * sin(deltalambda /2) as a,
    2 * atan2(sqrt(a), sqrt(1 - a)) as c,
    R * c as d
FROM {{ table }}

{%- endmacro %}