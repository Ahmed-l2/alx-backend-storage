-- SQL script that lists bands with Glam rock as their style, ranked longevity

SELECT
    band_name,
    (IFNULL(split, 2020) - formed) AS lifespan
FROM
    metal_bands
WHERE
    style LIKE '%Glam rock%'
ORDER BY
    lifespan DESC;