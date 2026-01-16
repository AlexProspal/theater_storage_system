-- Example Query 1: Items Currently in Stock
SELECT
    item_id,
    name,
    tag_code
FROM Item
WHERE item_id NOT IN (
    SELECT item_id
    FROM Checkout
);

-- Example Query 2: Count Items by Category
SELECT 
    c.name AS category,
    COUNT(i.item_id) AS item_count
FROM Category c
LEFT JOIN Item i ON i.category_id = c.category_id
GROUP BY c.name
ORDER BY item_count DESC;

-- Example Query 3: Checked-Out Items with Member and Production
SELECT
    i.name        AS item_name,
    i.tag_code    AS tag_code,
    m.name        AS member_name,
    p.title       AS production_title,
    c.checkout_date
FROM Checkout c
JOIN Item i
    ON i.item_id = c.item_id
LEFT JOIN Member m
    ON m.member_id = c.member_id
LEFT JOIN Production p
    ON p.production_id = c.production_id
ORDER BY c.checkout_date DESC, item_name;
