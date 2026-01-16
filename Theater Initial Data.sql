-- ============================================
-- Categories (6)
-- ============================================
INSERT INTO Category (name, description) VALUES
    ('Costume',   'All costume garments and full outfits'),
    ('Shoes',     'All footwear for productions'),
    ('Accessory', 'Hats, belts, jewelry and other accessories'),
    ('Prop',      'Hand props and small set pieces'),
    ('Wig',       'Wigs and hairpieces'),
    ('Makeup',    'Shared makeup kits for stage use');

-- ============================================
-- Storage locations (13)
-- ============================================
INSERT INTO StorageLocation (code, description) VALUES
    ('Costume-1',  'Costume rack 1'),
    ('Costume-2',  'Costume rack 2'),
    ('Costume-3',  'Costume rack 3'),
    ('Shoes-1',    'Shoe bin 1'),
    ('Shoes-2',    'Shoe bin 2'),
    ('Accessory-1','Accessory bin 1'),
    ('Accessory-2','Accessory bin 2'),
    ('Prop-1',     'Prop shelf 1'),
    ('Prop-2',     'Prop shelf 2'),
    ('Wig-1',      'Wig storage box 1'),
    ('Wig-2',      'Wig storage box 2'),
    ('Makeup-1',   'Makeup drawer 1'),
    ('Makeup-2',   'Makeup drawer 2');

-- ============================================
-- Members (10)
-- ============================================
INSERT INTO Member (name, email, phone, role) VALUES
    ('Alex Rivera',    'alex.rivera@example.edu',   '555-111-0001', 'Student Costume Designer'),
    ('Jordan Lee',     'jordan.lee@example.edu',    '555-111-0002', 'Actor'),
    ('Taylor Kim',     'taylor.kim@example.edu',    '555-111-0003', 'Actor'),
    ('Morgan Patel',   'morgan.patel@example.edu',  '555-111-0004', 'Stage Manager'),
    ('Casey Nguyen',   'casey.nguyen@example.edu',  '555-111-0005', 'Director'),
    ('Riley Chen',     'riley.chen@example.edu',    '555-111-0006', 'Wardrobe Head'),
    ('Sam Owens',      'sam.owens@example.edu',     '555-111-0007', 'Actor'),
    ('Jamie Torres',   'jamie.torres@example.edu',  '555-111-0008', 'Actor'),
    ('Drew Martinez',  'drew.martinez@example.edu', '555-111-0009', 'Crew'),
    ('Parker Smith',   'parker.smith@example.edu',  '555-111-0010', 'Costume Shop Assistant');

-- ============================================
-- Productions (3)
-- ============================================
INSERT INTO Production (title, season, open_date, close_date) VALUES
    ('Hamlet',         'Fall 2025',   '2025-10-10', '2025-10-25'),
    ('Into the Woods', 'Spring 2026', '2026-03-05', '2026-03-20'),
    ('Chicago',        'Spring 2026', '2026-04-15', '2026-04-30');

-- ============================================
-- Items (40)
-- ============================================

-- Costumes (14)
INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('C001', 'Black Tailcoat',
        (SELECT category_id FROM Category WHERE name = 'Costume'),
        'L', 'Black', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Costume-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('C002', 'White Dress Shirt',
        (SELECT category_id FROM Category WHERE name = 'Costume'),
        'M', 'White', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Costume-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('C003', 'Red Ball Gown',
        (SELECT category_id FROM Category WHERE name = 'Costume'),
        'S', 'Red', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Costume-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('C004', 'Blue Chorus Dress',
        (SELECT category_id FROM Category WHERE name = 'Costume'),
        'M', 'Blue', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Costume-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('C005', 'Brown Trench Coat',
        (SELECT category_id FROM Category WHERE name = 'Costume'),
        'L', 'Brown', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Costume-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('C006', 'Green Peasant Skirt',
        (SELECT category_id FROM Category WHERE name = 'Costume'),
        'M', 'Green', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Costume-2'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('C007', 'Gold Vest',
        (SELECT category_id FROM Category WHERE name = 'Costume'),
        'M', 'Gold', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Costume-2'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('C008', 'Grey Suit Jacket',
        (SELECT category_id FROM Category WHERE name = 'Costume'),
        'M', 'Grey', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Costume-2'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('C009', 'Black Tuxedo Pants',
        (SELECT category_id FROM Category WHERE name = 'Costume'),
        'L', 'Black', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Costume-2'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('C010', 'Floral Summer Dress',
        (SELECT category_id FROM Category WHERE name = 'Costume'),
        'S', 'Multicolor', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Costume-2'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('C011', 'Leather Jacket',
        (SELECT category_id FROM Category WHERE name = 'Costume'),
        'M', 'Black', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Costume-3'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('C012', 'Navy Blazer',
        (SELECT category_id FROM Category WHERE name = 'Costume'),
        'M', 'Navy', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Costume-3'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('C013', 'Plaid School Skirt',
        (SELECT category_id FROM Category WHERE name = 'Costume'),
        'S', 'Plaid', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Costume-3'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('C014', 'White Lab Coat',
        (SELECT category_id FROM Category WHERE name = 'Costume'),
        'L', 'White', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Costume-3'));

-- Shoes (8)
INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('S001', 'Character Heels',
        (SELECT category_id FROM Category WHERE name = 'Shoes'),
        '7', 'Black', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Shoes-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('S002', 'Jazz Shoes',
        (SELECT category_id FROM Category WHERE name = 'Shoes'),
        '9', 'Tan', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Shoes-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('S003', 'Tap Shoes',
        (SELECT category_id FROM Category WHERE name = 'Shoes'),
        '8', 'Black', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Shoes-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('S004', 'Work Boots',
        (SELECT category_id FROM Category WHERE name = 'Shoes'),
        '10', 'Brown', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Shoes-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('S005', 'Ballet Flats',
        (SELECT category_id FROM Category WHERE name = 'Shoes'),
        '7', 'Pink', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Shoes-2'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('S006', 'Sneakers',
        (SELECT category_id FROM Category WHERE name = 'Shoes'),
        '9', 'White', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Shoes-2'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('S007', 'Knee-High Boots',
        (SELECT category_id FROM Category WHERE name = 'Shoes'),
        '8', 'Black', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Shoes-2'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('S008', 'Oxfords',
        (SELECT category_id FROM Category WHERE name = 'Shoes'),
        '9', 'Brown', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Shoes-2'));

-- Accessories (8)
INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('A001', 'Feather Boa',
        (SELECT category_id FROM Category WHERE name = 'Accessory'),
        NULL, 'Red', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Accessory-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('A002', 'Silk Scarf',
        (SELECT category_id FROM Category WHERE name = 'Accessory'),
        NULL, 'Blue', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Accessory-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('A003', 'Fake Pearl Necklace',
        (SELECT category_id FROM Category WHERE name = 'Accessory'),
        NULL, 'White', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Accessory-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('A004', 'Leather Belt',
        (SELECT category_id FROM Category WHERE name = 'Accessory'),
        'M', 'Brown', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Accessory-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('A005', 'Top Hat',
        (SELECT category_id FROM Category WHERE name = 'Accessory'),
        'M', 'Black', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Accessory-2'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('A006', 'Newsboy Cap',
        (SELECT category_id FROM Category WHERE name = 'Accessory'),
        'M', 'Grey', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Accessory-2'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('A007', 'Opera Gloves',
        (SELECT category_id FROM Category WHERE name = 'Accessory'),
        'M', 'White', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Accessory-2'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('A008', 'Suspenders',
        (SELECT category_id FROM Category WHERE name = 'Accessory'),
        'M', 'Black', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Accessory-2'));

-- Props (6)
INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('P001', 'Skull Prop',
        (SELECT category_id FROM Category WHERE name = 'Prop'),
        NULL, 'Bone', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Prop-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('P002', 'Plastic Dagger',
        (SELECT category_id FROM Category WHERE name = 'Prop'),
        NULL, 'Silver', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Prop-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('P003', 'Faux Book Stack',
        (SELECT category_id FROM Category WHERE name = 'Prop'),
        NULL, 'Brown', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Prop-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('P004', 'Lantern',
        (SELECT category_id FROM Category WHERE name = 'Prop'),
        NULL, 'Bronze', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Prop-2'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('P005', 'Walking Cane',
        (SELECT category_id FROM Category WHERE name = 'Prop'),
        NULL, 'Black', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Prop-2'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('P006', 'Toy Pistol',
        (SELECT category_id FROM Category WHERE name = 'Prop'),
        NULL, 'Black', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Prop-2'));

-- Wigs (2)
INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('W001', 'Long Curly Wig',
        (SELECT category_id FROM Category WHERE name = 'Wig'),
        'M', 'Blonde', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Wig-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('W002', 'Short Bob Wig',
        (SELECT category_id FROM Category WHERE name = 'Wig'),
        'S', 'Black', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Wig-2'));

-- Makeup (2)
INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('M001', 'Stage Foundation Palette',
        (SELECT category_id FROM Category WHERE name = 'Makeup'),
        NULL, 'Mixed', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Makeup-1'));

INSERT INTO Item (tag_code, name, category_id, size, color, notes, location_id)
VALUES ('M002', 'Bruise Wheel Palette',
        (SELECT category_id FROM Category WHERE name = 'Makeup'),
        NULL, 'Multicolor', NULL,
        (SELECT location_id FROM StorageLocation WHERE code = 'Makeup-2'));

-- ============================================
-- Item–Production links
-- ============================================
INSERT INTO ItemProduction (item_id, production_id, character_name, notes)
VALUES ((SELECT item_id FROM Item WHERE tag_code = 'C001'),
        (SELECT production_id FROM Production WHERE title = 'Hamlet'),
        'Hamlet', 'Act II formal look');

INSERT INTO ItemProduction (item_id, production_id, character_name, notes)
VALUES ((SELECT item_id FROM Item WHERE tag_code = 'C003'),
        (SELECT production_id FROM Production WHERE title = 'Hamlet'),
        'Ophelia', 'Ball scene gown');

INSERT INTO ItemProduction (item_id, production_id, character_name, notes)
VALUES ((SELECT item_id FROM Item WHERE tag_code = 'C014'),
        (SELECT production_id FROM Production WHERE title = 'Hamlet'),
        'Doctor', 'Laboratory scene');

INSERT INTO ItemProduction (item_id, production_id, character_name, notes)
VALUES ((SELECT item_id FROM Item WHERE tag_code = 'P001'),
        (SELECT production_id FROM Production WHERE title = 'Hamlet'),
        'Hamlet', 'Graveyard skull');

INSERT INTO ItemProduction (item_id, production_id, character_name, notes)
VALUES ((SELECT item_id FROM Item WHERE tag_code = 'P006'),
        (SELECT production_id FROM Production WHERE title = 'Hamlet'),
        'Laertes', 'Duel prop');

INSERT INTO ItemProduction (item_id, production_id, character_name, notes)
VALUES ((SELECT item_id FROM Item WHERE tag_code = 'C004'),
        (SELECT production_id FROM Production WHERE title = 'Into the Woods'),
        'Cinderella', 'Opening dress');

INSERT INTO ItemProduction (item_id, production_id, character_name, notes)
VALUES ((SELECT item_id FROM Item WHERE tag_code = 'C010'),
        (SELECT production_id FROM Production WHERE title = 'Into the Woods'),
        'Baker''s Wife', 'Act I costume');

INSERT INTO ItemProduction (item_id, production_id, character_name, notes)
VALUES ((SELECT item_id FROM Item WHERE tag_code = 'S001'),
        (SELECT production_id FROM Production WHERE title = 'Into the Woods'),
        'Witch', 'Character heels');

INSERT INTO ItemProduction (item_id, production_id, character_name, notes)
VALUES ((SELECT item_id FROM Item WHERE tag_code = 'A001'),
        (SELECT production_id FROM Production WHERE title = 'Into the Woods'),
        'Little Red', 'Feather boa gag');

INSERT INTO ItemProduction (item_id, production_id, character_name, notes)
VALUES ((SELECT item_id FROM Item WHERE tag_code = 'C005'),
        (SELECT production_id FROM Production WHERE title = 'Chicago'),
        'Velma', 'Rehearsal trench');

INSERT INTO ItemProduction (item_id, production_id, character_name, notes)
VALUES ((SELECT item_id FROM Item WHERE tag_code = 'C008'),
        (SELECT production_id FROM Production WHERE title = 'Chicago'),
        'Billy Flynn', 'Courtroom suit');

INSERT INTO ItemProduction (item_id, production_id, character_name, notes)
VALUES ((SELECT item_id FROM Item WHERE tag_code = 'S007'),
        (SELECT production_id FROM Production WHERE title = 'Chicago'),
        'Ensemble', 'Knee-high boots for dance');

INSERT INTO ItemProduction (item_id, production_id, character_name, notes)
VALUES ((SELECT item_id FROM Item WHERE tag_code = 'A005'),
        (SELECT production_id FROM Production WHERE title = 'Chicago'),
        'Master of Ceremonies', 'Top hat');

-- ============================================
-- Checkouts (15)
-- ============================================
INSERT INTO Checkout (item_id, member_id, production_id, checkout_date, notes)
VALUES ((SELECT item_id FROM Item   WHERE tag_code = 'C001'),
        (SELECT member_id FROM Member WHERE email = 'jordan.lee@example.edu'),
        (SELECT production_id FROM Production WHERE title = 'Hamlet'),
        CURRENT_DATE - INTERVAL '5 days',
        'Lead costume fitting');

INSERT INTO Checkout (item_id, member_id, production_id, checkout_date, notes)
VALUES ((SELECT item_id FROM Item   WHERE tag_code = 'C003'),
        (SELECT member_id FROM Member WHERE email = 'taylor.kim@example.edu'),
        (SELECT production_id FROM Production WHERE title = 'Hamlet'),
        CURRENT_DATE - INTERVAL '3 days',
        'Dress rehearsal');

INSERT INTO Checkout (item_id, member_id, production_id, checkout_date, notes)
VALUES ((SELECT item_id FROM Item   WHERE tag_code = 'C005'),
        (SELECT member_id FROM Member WHERE email = 'sam.owens@example.edu'),
        (SELECT production_id FROM Production WHERE title = 'Chicago'),
        CURRENT_DATE - INTERVAL '2 days',
        'Choreography rehearsal');

INSERT INTO Checkout (item_id, member_id, production_id, checkout_date, notes)
VALUES ((SELECT item_id FROM Item   WHERE tag_code = 'C010'),
        (SELECT member_id FROM Member WHERE email = 'morgan.patel@example.edu'),
        (SELECT production_id FROM Production WHERE title = 'Into the Woods'),
        CURRENT_DATE - INTERVAL '7 days',
        'Tech week');

INSERT INTO Checkout (item_id, member_id, production_id, checkout_date, notes)
VALUES ((SELECT item_id FROM Item   WHERE tag_code = 'C014'),
        (SELECT member_id FROM Member WHERE email = 'alex.rivera@example.edu'),
        (SELECT production_id FROM Production WHERE title = 'Hamlet'),
        CURRENT_DATE - INTERVAL '1 days',
        'Alterations in progress');

INSERT INTO Checkout (item_id, member_id, production_id, checkout_date, notes)
VALUES ((SELECT item_id FROM Item   WHERE tag_code = 'S001'),
        (SELECT member_id FROM Member WHERE email = 'jordan.lee@example.edu'),
        (SELECT production_id FROM Production WHERE title = 'Into the Woods'),
        CURRENT_DATE - INTERVAL '4 days',
        'Character shoes');

INSERT INTO Checkout (item_id, member_id, production_id, checkout_date, notes)
VALUES ((SELECT item_id FROM Item   WHERE tag_code = 'S004'),
        (SELECT member_id FROM Member WHERE email = 'drew.martinez@example.edu'),
        NULL,
        CURRENT_DATE - INTERVAL '6 days',
        'Crew boots for build');

INSERT INTO Checkout (item_id, member_id, production_id, checkout_date, notes)
VALUES ((SELECT item_id FROM Item   WHERE tag_code = 'S007'),
        (SELECT member_id FROM Member WHERE email = 'jamie.torres@example.edu'),
        (SELECT production_id FROM Production WHERE title = 'Chicago'),
        CURRENT_DATE - INTERVAL '2 days',
        'Dance rehearsal');

INSERT INTO Checkout (item_id, member_id, production_id, checkout_date, notes)
VALUES ((SELECT item_id FROM Item   WHERE tag_code = 'A002'),
        (SELECT member_id FROM Member WHERE email = 'taylor.kim@example.edu'),
        NULL,
        CURRENT_DATE - INTERVAL '8 days',
        'Pulled for headshots');

INSERT INTO Checkout (item_id, member_id, production_id, checkout_date, notes)
VALUES ((SELECT item_id FROM Item   WHERE tag_code = 'A005'),
        (SELECT member_id FROM Member WHERE email = 'casey.nguyen@example.edu'),
        (SELECT production_id FROM Production WHERE title = 'Chicago'),
        CURRENT_DATE - INTERVAL '10 days',
        'Director look test');

INSERT INTO Checkout (item_id, member_id, production_id, checkout_date, notes)
VALUES ((SELECT item_id FROM Item   WHERE tag_code = 'A007'),
        (SELECT member_id FROM Member WHERE email = 'riley.chen@example.edu'),
        NULL,
        CURRENT_DATE - INTERVAL '1 days',
        'Quick-change testing');

INSERT INTO Checkout (item_id, member_id, production_id, checkout_date, notes)
VALUES ((SELECT item_id FROM Item   WHERE tag_code = 'P001'),
        (SELECT member_id FROM Member WHERE email = 'sam.owens@example.edu'),
        (SELECT production_id FROM Production WHERE title = 'Hamlet'),
        CURRENT_DATE - INTERVAL '9 days',
        'Scene work');

INSERT INTO Checkout (item_id, member_id, production_id, checkout_date, notes)
VALUES ((SELECT item_id FROM Item   WHERE tag_code = 'P004'),
        (SELECT member_id FROM Member WHERE email = 'drew.martinez@example.edu'),
        (SELECT production_id FROM Production WHERE title = 'Into the Woods'),
        CURRENT_DATE - INTERVAL '3 days',
        'Tech rehearsal prop');

INSERT INTO Checkout (item_id, member_id, production_id, checkout_date, notes)
VALUES ((SELECT item_id FROM Item   WHERE tag_code = 'W001'),
        (SELECT member_id FROM Member WHERE email = 'jamie.torres@example.edu'),
        (SELECT production_id FROM Production WHERE title = 'Chicago'),
        CURRENT_DATE - INTERVAL '4 days',
        'Wig styling');

INSERT INTO Checkout (item_id, member_id, production_id, checkout_date, notes)
VALUES ((SELECT item_id FROM Item   WHERE tag_code = 'M001'),
        (SELECT member_id FROM Member WHERE email = 'parker.smith@example.edu'),
        NULL,
        CURRENT_DATE - INTERVAL '1 days',
        'Makeup tests');
