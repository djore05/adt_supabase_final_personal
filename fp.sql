-- [Dhruv Jore - djore] Employee Table
CREATE TABLE employee (
    employee_id SERIAL PRIMARY KEY,
    employee_name VARCHAR(255) NOT NULL,
    title VARCHAR(100),
    contact_number VARCHAR(20),
    age INT,
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female', 'Other')),
    salary DECIMAL(10,2),
    joining_date DATE
);

-- [Yashkumar Burnwal - yburnwal] Customer Table
CREATE TABLE customer (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    mobile VARCHAR(20) NOT NULL,
    email VARCHAR(255)  
);

-- [Dhruv Jore - djore] Restaurant Tables
CREATE TABLE restaurant_tables (
    table_id SERIAL PRIMARY KEY,
    table_number INT UNIQUE NOT NULL,
    seating_capacity INT NOT NULL,
    availability_status VARCHAR(10) CHECK (availability_status IN ('available', 'occupied', 'reserved')) DEFAULT 'available'
);

-- [Dhruv Jore - djore] Menu Sections (e.g., Breakfast, Lunch, Dinner, Beverages, Kids, Specials)
CREATE TABLE menu_sections (
    section_id SERIAL PRIMARY KEY,
    section_name VARCHAR(100) UNIQUE NOT NULL
);

-- [Yashkumar Burnwal - yburnwal] Menu Subcategories (e.g., Alcoholic/Non-Alcoholic under Beverages)
CREATE TABLE menu_subcategories (
    subcategory_id SERIAL PRIMARY KEY,
    section_id INT,
    subcategory_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (section_id) REFERENCES menu_sections(section_id) ON DELETE CASCADE
);

-- [Yashkumar Burnwal - yburnwal] Menu Items
CREATE TABLE menu_items (
    menu_item_id SERIAL PRIMARY KEY,
    subcategory_id INT,
    item_name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    availability BOOLEAN DEFAULT TRUE,
    spice_level VARCHAR(10) CHECK (spice_level IN ('None', 'Mild', 'Medium', 'Hot', 'Extra Hot')) DEFAULT 'None',
    dietary_type VARCHAR(10) CHECK (dietary_type IN ('Veg', 'Non-Veg', 'Vegan', 'Egg')) NOT NULL,
    is_seasonal BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (subcategory_id) REFERENCES menu_subcategories(subcategory_id) ON DELETE CASCADE
);

-- [Priyanshu Laddha - prladdha] Menu Item Seasons
CREATE TABLE menu_item_seasons (
    menu_item_id INT,
    season_name VARCHAR(10) CHECK (season_name IN ('Summer', 'Winter', 'Spring', 'Fall')) NOT NULL,
    PRIMARY KEY (menu_item_id, season_name),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(menu_item_id) ON DELETE CASCADE
);

-- [Dhruv Jore - djore] Availability Timings (Breakfast / Lunch / Dinner)
CREATE TABLE availability_timings (
    menu_item_id INT PRIMARY KEY,
    available_in_breakfast BOOLEAN DEFAULT FALSE,
    available_in_lunch BOOLEAN DEFAULT FALSE,
    available_in_dinner BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(menu_item_id) ON DELETE CASCADE
);

-- [Yashkumar Burnwal - yburnwal] Orders Table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    table_id INT,
    order_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10,2) NOT NULL,
    order_status VARCHAR(10) CHECK (order_status IN ('Pending', 'Confirmed', 'Served', 'Cancelled')) DEFAULT 'Pending',
    employee_id INT,
    order_type VARCHAR(10) CHECK (order_type IN ('Online', 'Dine In', 'Take Away')) DEFAULT 'Dine In',
    payment_method VARCHAR(20) CHECK (payment_method IN ('Cash', 'Credit Card', 'Debit Card', 'Mobile Payment', 'Other')) DEFAULT 'Cash',
    FOREIGN KEY (table_id) REFERENCES restaurant_tables(table_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

-- [Priyanshu Laddha - prladdha] Order Items (Join between Orders and Menu Items)
CREATE TABLE order_items (
    order_id INT,
    menu_item_id INT,
    quantity INT NOT NULL,
    PRIMARY KEY (order_id, menu_item_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(menu_item_id) ON DELETE CASCADE
);

-- [Priyanshu Laddha - prladdha] Reservations Table
CREATE TABLE reservations (
    reservation_id SERIAL PRIMARY KEY,
    customer_id INT,
    reservation_time TIMESTAMP NOT NULL,
    number_of_guests INT NOT NULL,
    table_id INT,
    special_requests TEXT,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (table_id) REFERENCES restaurant_tables(table_id)
);

-- [Dhruv Jore - djore] Insert Employees
INSERT INTO employee (employee_name, title, contact_number, age, gender, salary, joining_date) VALUES
('Sarah Johnson', 'Restaurant Manager', '123-456-7890', 35, 'Female', 75000.00, '2020-05-01'),
('Michael Chen', 'Assistant Manager', '234-567-8901', 31, 'Male', 58000.00, '2021-06-15'),
('Jessica Patel', 'HR Coordinator', '345-678-9012', 29, 'Female', 52000.00, '2022-07-10'),
('Antonio Rossi', 'Executive Chef', '456-789-0123', 42, 'Male', 85000.00, '2018-03-20'),
('Emily Williams', 'Sous Chef', '567-890-1234', 36, 'Female', 65000.00, '2021-01-12'),
('Raj Kumar', 'Head Chef', '678-901-2345', 39, 'Male', 70000.00, '2019-09-18'),
('Sophie Laurent', 'Pastry Chef', '789-012-3456', 33, 'Female', 60000.00, '2020-04-23'),
('Thomas Martinez', 'Head Server', '890-123-4567', 28, 'Male', 45000.00, '2021-08-30'),
('Olivia Lee', 'Bartender', '901-234-5678', 26, 'Female', 40000.00, '2022-02-14'),
('David Singh', 'Server', '111-222-3333', 24, 'Male', 38000.00, '2023-01-10'),
('Emma Brown', 'Server', '222-333-4444', 27, 'Female', 37000.00, '2022-11-05'),
('Liam Wilson', 'Server', '333-444-5555', 29, 'Male', 39000.00, '2021-07-22'),
('Sophia Garcia', 'Server', '444-555-6666', 23, 'Female', 36000.00, '2023-03-18'),
('Noah Anderson', 'Server', '555-666-7777', 30, 'Male', 42000.00, '2020-10-28'),
('Ava Martin', 'Hostess', '666-777-8888', 22, 'Female', 32000.00, '2023-04-01'),
('Ethan Clark', 'Host', '777-888-9999', 21, 'Male', 32000.00, '2023-05-10');

-- [Dhruv Jore - djore] Insert Restaurant Tables
INSERT INTO restaurant_tables (table_number, seating_capacity, availability_status) VALUES
(1, 2, 'available'),
(2, 2, 'available'),
(3, 2, 'available'),
(4, 2, 'available'),
(5, 4, 'available'),
(6, 4, 'available'),
(7, 4, 'available'),
(8, 4, 'available'),
(9, 4, 'available'),
(10, 4, 'available'),
(11, 6, 'available'),
(12, 6, 'available'),
(13, 6, 'available'),
(14, 6, 'available'),
(15, 8, 'available'),
(16, 8, 'available'),
(17, 10, 'available'),
(18, 10, 'available'),
(19, 12, 'available'),
(20, 14, 'available');

-- [Dhruv Jore - djore] Insert Menu Sections
INSERT INTO menu_sections (section_name) VALUES
('Breakfast'),
('Lunch'),
('Dinner'),
('Beverages'),
('Desserts'),
('Kids Menu'),
('Seasonal Specials');

-- [Yashkumar Burnwal - yburnwal] Insert Menu Subcategories
-- Breakfast
INSERT INTO menu_subcategories (section_id, subcategory_name) VALUES
(1, 'Hot Breakfast'),
(1, 'Continental Breakfast'),
(1, 'Breakfast Specials');

-- [Yashkumar Burnwal - yburnwal] Lunch
INSERT INTO menu_subcategories (section_id, subcategory_name) VALUES
(2, 'Soups & Salads'),
(2, 'Sandwiches & Wraps'),
(2, 'Main Courses');

-- [Priyanshu Laddha - prladdha] Dinner
INSERT INTO menu_subcategories (section_id, subcategory_name) VALUES
(3, 'Appetizers'),
(3, 'Main Courses'),
(3, 'Chef Specials');

-- [Dhruv Jore - djore] Beverages
INSERT INTO menu_subcategories (section_id, subcategory_name) VALUES
(4, 'Non-Alcoholic'),
(4, 'Cocktails'),
(4, 'Wine & Beer');

-- [Dhruv Jore - djore] Desserts
INSERT INTO menu_subcategories (section_id, subcategory_name) VALUES
(5, 'Cakes & Pastries'),
(5, 'Ice Cream & Frozen Desserts'),
(5, 'Specialty Desserts');

-- [Yashkumar Burnwal - yburnwal] Kids Menu
INSERT INTO menu_subcategories (section_id, subcategory_name) VALUES
(6, 'Kids Mains'),
(6, 'Kids Sides'),
(6, 'Kids Desserts');

-- [Yashkumar Burnwal - yburnwal] Seasonal Specials
INSERT INTO menu_subcategories (section_id, subcategory_name) VALUES
(7, 'Seasonal Dishes');

-- [Priyanshu Laddha - prladdha] Breakfast Items
INSERT INTO menu_items (subcategory_id, item_name, description, price, availability, spice_level, dietary_type, is_seasonal)
VALUES
(1, 'Eggs Benedict', 'Two poached eggs on English muffin with Canadian bacon and hollandaise sauce.', 16.95, TRUE, 'Medium', 'Non-Veg', FALSE),
(1, 'Avocado Toast', 'Sourdough toast with smashed avocado, poached egg, and microgreens.', 14.50, TRUE, 'None', 'Egg', FALSE),
(2, 'Pancake Stack', 'Fluffy buttermilk pancakes with maple syrup and fresh berries.', 13.95, TRUE, 'None', 'Veg', FALSE),
(3, 'Breakfast Burrito', 'Scrambled eggs, chorizo, black beans, and cheese in a flour tortilla.', 15.95, TRUE, 'Medium', 'Non-Veg', FALSE),
(3, 'Vegan Breakfast Bowl', 'Quinoa, roasted vegetables, avocado, and plant-based protein.', 16.50, TRUE, 'Mild', 'Vegan', FALSE);

-- [Yashkumar Burnwal - yburnwal] Lunch Items
INSERT INTO menu_items (subcategory_id, item_name, description, price, availability, spice_level, dietary_type, is_seasonal)
VALUES
(4, 'Caesar Salad', 'Romaine lettuce, croutons, parmesan cheese with classic Caesar dressing.', 14.95, TRUE, 'None', 'Veg', FALSE),
(5, 'Chicken Club Sandwich', 'Grilled chicken, bacon, lettuce, tomato on toasted bread with fries.', 17.50, TRUE, 'None', 'Non-Veg', FALSE),
(6, 'Vegetable Quinoa Bowl', 'Mixed grains, roasted seasonal vegetables, tahini dressing.', 16.95, TRUE, 'Mild', 'Vegan', FALSE),
(6, 'Fish Tacos', 'Beer-battered fish, slaw, avocado, lime crema in corn tortillas.', 18.95, TRUE, 'Medium', 'Non-Veg', FALSE),
(6, 'Mushroom Risotto', 'Creamy Arborio rice with wild mushrooms and parmesan.', 19.50, TRUE, 'None', 'Veg', FALSE);

-- [Priyanshu Laddha - prladdha] Dinner Appetizers
INSERT INTO menu_items (subcategory_id, item_name, description, price, availability, spice_level, dietary_type, is_seasonal)
VALUES
(7, 'Crispy Calamari', 'Lightly battered squid rings with lemon aioli.', 16.95, TRUE, 'None', 'Non-Veg', FALSE),
(7, 'Bruschetta', 'Toasted baguette with tomato, basil, garlic, and olive oil.', 13.50, TRUE, 'None', 'Vegan', FALSE),
(7, 'Buffalo Wings', 'Crispy chicken wings tossed in house buffalo sauce.', 15.95, TRUE, 'Hot', 'Non-Veg', FALSE),
(7, 'Spinach Artichoke Dip', 'Creamy spinach and artichoke dip with tortilla chips.', 14.50, TRUE, 'None', 'Veg', FALSE);

-- [Dhruv Jore - djore] Dinner Main Courses
INSERT INTO menu_items (subcategory_id, item_name, description, price, availability, spice_level, dietary_type, is_seasonal)
VALUES
(8, 'Grilled Salmon', 'Atlantic salmon with lemon butter sauce and seasonal vegetables.', 28.95, TRUE, 'None', 'Non-Veg', FALSE),
(8, 'Ribeye Steak', '12oz aged ribeye with garlic mashed potatoes and asparagus.', 36.95, TRUE, 'None', 'Non-Veg', FALSE),
(8, 'Eggplant Parmesan', 'Breaded eggplant, marinara sauce, melted mozzarella with pasta.', 22.95, TRUE, 'Mild', 'Veg', FALSE),
(8, 'Thai Green Curry', 'Aromatic coconut curry with vegetables and jasmine rice.', 24.95, TRUE, 'Hot', 'Vegan', FALSE),
(8, 'Truffle Pasta', 'Handmade fettuccine with truffle cream sauce and wild mushrooms.', 26.50, TRUE, 'None', 'Veg', FALSE),
(8, 'Herb-Roasted Chicken', 'Half chicken with herb jus, roasted potatoes, and seasonal vegetables.', 25.95, TRUE, 'Mild', 'Non-Veg', FALSE);

-- [Yashkumar Burnwal - yburnwal] Insert Kids Mains
INSERT INTO menu_items (subcategory_id, item_name, description, price, availability, spice_level, dietary_type, is_seasonal) VALUES
(16, 'Mini Cheeseburger', 'Beef patty with cheese on a small bun with fries.', 9.95, TRUE, 'None', 'Non-Veg', FALSE),
(16, 'Chicken Tenders', 'Breaded chicken strips with honey mustard and fries.', 8.95, TRUE, 'None', 'Non-Veg', FALSE),
(16, 'Mac and Cheese', 'Creamy cheese sauce with elbow pasta.', 7.95, TRUE, 'None', 'Veg', FALSE),
(16, 'Grilled Cheese', 'Melted cheese on toasted bread with fries.', 6.95, TRUE, 'None', 'Veg', FALSE);

-- [Priyanshu Laddha - prladdha] Insert Kids Sides
INSERT INTO menu_items (subcategory_id, item_name, description, price, availability, spice_level, dietary_type, is_seasonal) VALUES
(17, 'Kids Fries', 'Small portion of crispy fries.', 3.95, TRUE, 'None', 'Veg', FALSE),
(17, 'Apple Slices', 'Fresh apple slices.', 2.95, TRUE, 'None', 'Vegan', FALSE),
(17, 'Steamed Broccoli', 'Lightly steamed broccoli florets.', 3.95, TRUE, 'None', 'Vegan', FALSE);

-- [Yashkumar Burnwal - yburnwal] Insert Kids Desserts
INSERT INTO menu_items (subcategory_id, item_name, description, price, availability, spice_level, dietary_type, is_seasonal) VALUES
(18, 'Mini Brownie', 'Small fudge brownie.', 3.95, TRUE, 'None', 'Veg', FALSE),
(18, 'Ice Cream Scoop', 'Single scoop of vanilla or chocolate ice cream.', 2.95, TRUE, 'None', 'Veg', FALSE);

-- [Yashkumar Burnwal - yburnwal] Insert Cakes & Pastries
INSERT INTO menu_items (subcategory_id, item_name, description, price, availability, spice_level, dietary_type, is_seasonal) VALUES
(13, 'Chocolate Lava Cake', 'Warm chocolate cake with molten center and vanilla ice cream.', 10.95, TRUE, 'None', 'Veg', FALSE),
(13, 'Cheesecake', 'New York style cheesecake with berry compote.', 9.95, TRUE, 'None', 'Veg', FALSE),
(13, 'Carrot Cake', 'Moist carrot cake with cream cheese frosting.', 8.95, TRUE, 'None', 'Veg', FALSE);

-- [Yashkumar Burnwal - yburnwal] Insert Ice Cream & Frozen Desserts
INSERT INTO menu_items (subcategory_id, item_name, description, price, availability, spice_level, dietary_type, is_seasonal) VALUES
(14, 'Vanilla Ice Cream', 'Classic vanilla bean ice cream.', 4.50, TRUE, 'None', 'Veg', FALSE),
(14, 'Chocolate Ice Cream', 'Rich chocolate ice cream.', 4.50, TRUE, 'None', 'Veg', FALSE),
(14, 'Strawberry Sorbet', 'Refreshing strawberry sorbet.', 5.00, TRUE, 'None', 'Vegan', FALSE);

-- [Priyanshu Laddha - prladdha] Insert Specialty Desserts
INSERT INTO menu_items (subcategory_id, item_name, description, price, availability, spice_level, dietary_type, is_seasonal) VALUES
(15, 'Tiramisu', 'Classic Italian coffee-flavored dessert.', 10.50, TRUE, 'None', 'Veg', FALSE),
(15, 'Seasonal Fruit Tart', 'Fresh fruit tart with pastry cream.', 9.00, TRUE, 'None', 'Veg', FALSE);

-- [Yashkumar Burnwal - yburnwal] Seasonal Specials Items
INSERT INTO menu_items (subcategory_id, item_name, description, price, availability, spice_level, dietary_type, is_seasonal)
VALUES
(19, 'Summer Gazpacho', 'Chilled tomato soup with cucumber and bell peppers.', 12.95, TRUE, 'Mild', 'Vegan', TRUE),
(19, 'Autumn Harvest Salad', 'Mixed greens with roasted squash, cranberries, and maple vinaigrette.', 16.95, TRUE, 'None', 'Vegan', TRUE),
(19, 'Winter Beef Stew', 'Slow-cooked beef with root vegetables and red wine sauce.', 24.95, TRUE, 'Medium', 'Non-Veg', TRUE),
(19, 'Spring Pea Risotto', 'Arborio rice with fresh peas, mint, and parmesan.', 23.95, TRUE, 'None', 'Veg', TRUE);

-- [Priyanshu Laddha - prladdha] Insert Non-Alcoholic Beverages into Menu Items
INSERT INTO menu_items (subcategory_id, item_name, description, price, availability, spice_level, dietary_type, is_seasonal) VALUES
(10, 'Fresh Orange Juice', 'Freshly squeezed orange juice.', 5.95, TRUE, 'None', 'Vegan', FALSE),
(10, 'Artisanal Lemonade', 'Handcrafted lemonade with a hint of mint.', 4.95, TRUE, 'None', 'Vegan', FALSE),
(10, 'Cold Brew Coffee', 'Slow-steeped cold brew coffee.', 5.50, TRUE, 'None', 'Vegan', FALSE),
(10, 'Sparkling Water', 'Refreshing sparkling mineral water.', 3.95, TRUE, 'None', 'Vegan', FALSE),
(10, 'Hibiscus Iced Tea', 'Hibiscus flower infused iced tea.', 4.50, TRUE, 'None', 'Vegan', FALSE),
(10, 'Strawberry Smoothie', 'Strawberry smoothie with almond milk.', 6.95, TRUE, 'None', 'Vegan', FALSE),
(10, 'Green Juice', 'Blend of kale, spinach, green apple, and cucumber.', 7.95, TRUE, 'None', 'Vegan', FALSE),
(10, 'Hot Chocolate', 'Rich hot chocolate with whipped cream.', 4.95, TRUE, 'None', 'Veg', FALSE),
(10, 'Espresso', 'Strong espresso shot.', 3.95, TRUE, 'None', 'Vegan', FALSE),
(10, 'Cappuccino', 'Espresso with steamed milk foam.', 5.50, TRUE, 'None', 'Veg', FALSE);

-- [Dhruv Jore - djore] Insert Cocktails into Menu Items
INSERT INTO menu_items (subcategory_id, item_name, description, price, availability, spice_level, dietary_type, is_seasonal) VALUES
(11, 'Classic Martini', 'Gin or vodka martini with olive garnish.', 12.95, TRUE, 'None', 'Vegan', FALSE),
(11, 'Signature Old Fashioned', 'Whiskey cocktail with bitters and orange.', 14.95, TRUE, 'None', 'Vegan', FALSE),
(11, 'Seasonal Sangria', 'Fruity wine punch with seasonal fruits.', 11.95, TRUE, 'None', 'Vegan', FALSE),
(11, 'Aperol Spritz', 'Aperol, prosecco, and soda water.', 12.95, TRUE, 'None', 'Vegan', FALSE),
(11, 'Margarita', 'Tequila, triple sec, lime juice on the rocks.', 13.95, TRUE, 'None', 'Vegan', FALSE),
(11, 'Mojito', 'White rum, mint, lime, soda.', 12.95, TRUE, 'None', 'Vegan', FALSE);

-- [Priyanshu Laddha - prladdha] Insert Wines & Beers into Menu Items
INSERT INTO menu_items (subcategory_id, item_name, description, price, availability, spice_level, dietary_type, is_seasonal) VALUES
(12, 'House Red Wine (glass)', 'Glass of our house-selected red wine.', 9.95, TRUE, 'None', 'Vegan', FALSE),
(12, 'House White Wine (glass)', 'Glass of our house-selected white wine.', 9.95, TRUE, 'None', 'Vegan', FALSE),
(12, 'Craft IPA', 'Locally brewed India Pale Ale.', 7.95, TRUE, 'None', 'Vegan', FALSE),
(12, 'Craft Lager', 'Locally brewed crisp lager.', 6.95, TRUE, 'None', 'Vegan', FALSE);

-- [Priyanshu Laddha - prladdha] Mapping Menu Items to Seasons
INSERT INTO menu_item_seasons (menu_item_id, season_name) VALUES
(25, 'Summer'),
(26, 'Fall'),
(27, 'Winter'),
(28, 'Spring');

-- [Dhruv Jore - djore] Availability Timings for Items
-- Breakfast Items (IDs: 1 to 5)
INSERT INTO availability_timings (menu_item_id, available_in_breakfast, available_in_lunch, available_in_dinner)
VALUES
(1, TRUE, FALSE, FALSE),
(2, TRUE, FALSE, FALSE),
(3, TRUE, FALSE, FALSE),
(4, TRUE, FALSE, FALSE),
(5, TRUE, TRUE, FALSE);

-- [Dhruv Jore - djore] Lunch Items (IDs: 6 to 10)
INSERT INTO availability_timings (menu_item_id, available_in_breakfast, available_in_lunch, available_in_dinner)
VALUES
(6, FALSE, TRUE, TRUE),
(7, FALSE, TRUE, TRUE),
(8, FALSE, TRUE, TRUE),
(9, FALSE, TRUE, TRUE),
(10, FALSE, TRUE, TRUE);

-- [Dhruv Jore - djore] Dinner Appetizers (IDs: 11 to 14)
INSERT INTO availability_timings (menu_item_id, available_in_breakfast, available_in_lunch, available_in_dinner)
VALUES
(11, FALSE, FALSE, TRUE),
(12, FALSE, FALSE, TRUE),
(13, FALSE, FALSE, TRUE),
(14, FALSE, FALSE, TRUE);

-- [Dhruv Jore - djore] Dinner Main Courses (IDs: 15 to 20)
INSERT INTO availability_timings (menu_item_id, available_in_breakfast, available_in_lunch, available_in_dinner)
VALUES
(15, FALSE, FALSE, TRUE),
(16, FALSE, FALSE, TRUE),
(17, FALSE, FALSE, TRUE),
(18, FALSE, FALSE, TRUE),
(19, FALSE, FALSE, TRUE),
(20, FALSE, FALSE, TRUE);

-- [Dhruv Jore - djore] Seasonal Specials (Summer, Fall, Winter, Spring)
INSERT INTO availability_timings (menu_item_id, available_in_breakfast, available_in_lunch, available_in_dinner)
VALUES
(25, FALSE, TRUE, TRUE),  -- Summer Gazpacho
(26, FALSE, TRUE, TRUE),  -- Autumn Harvest Salad
(27, FALSE, TRUE, TRUE),  -- Winter Beef Stew
(28, FALSE, TRUE, TRUE);  -- Spring Pea Risotto

-- [Yashkumar Burnwal - yburnwal] Insert Customers
INSERT INTO customer (name, mobile, email) VALUES
('John Doe', '987-654-3210', 'john.doe@example.com'),
('Jane Smith', '876-543-2109', 'jane.smith@example.com'),
('Robert Brown', '765-432-1098', 'robert.brown@example.com'),
('Emily Davis', '654-321-0987', 'emily.davis@example.com'),
('Michael Johnson', '543-210-9876', 'michael.johnson@example.com'),
('Sarah Wilson', '432-109-8765', 'sarah.wilson@example.com'),
('David Lee', '321-098-7654', 'david.lee@example.com'),
('Olivia Taylor', '210-987-6543', 'olivia.taylor@example.com'),
('Daniel Harris', '109-876-5432', 'daniel.harris@example.com'),
('Sophia Martinez', '098-765-4321', 'sophia.martinez@example.com'),
('Chris Walker', '987-123-4567', 'chris.walker@example.com'),
('Emma Robinson', '876-234-5678', 'emma.robinson@example.com'),
('Liam Hall', '765-345-6789', 'liam.hall@example.com'),
('Ava Allen', '654-456-7890', 'ava.allen@example.com'),
('Noah Young', '543-567-8901', 'noah.young@example.com');

-- [Priyanshu Laddha - prladdha] Insert Reservations
INSERT INTO reservations (customer_id, reservation_time, number_of_guests, table_id, special_requests) VALUES
(1, '2025-05-15 19:00:00', 2, 5, 'Anniversary Celebration - Window Seat'),
(2, '2025-05-16 20:00:00', 4, 10, 'Birthday Celebration - Bring Cake'),
(3, '2025-05-17 18:30:00', 6, 14, 'Gluten-Free Dietary Request'),
(4, '2025-05-18 12:00:00', 2, 2, 'Business Lunch - Quiet Table'),
(5, '2025-05-19 19:30:00', 3, 6, 'Vegetarian Meal Required'),
(6, '2025-05-20 18:00:00', 8, 16, 'Large Family Gathering'),
(7, '2025-05-21 19:00:00', 10, 18, 'Private Dining Room - Anniversary'),
(8, '2025-05-22 13:00:00', 1, 1, 'Window Seating Preferred'),
(9, '2025-05-23 18:45:00', 5, 13, 'Birthday Party - Need Extra Cake'),
(10, '2025-05-24 20:00:00', 2, 4, 'Accessible Seating Needed');

-- [Yashkumar Burnwal]
-- Insert into reservations table
INSERT INTO reservations (customer_id, reservation_time,
number_of_guests, table_id, special_requests) VALUES
(1, '2025-05-15 19:00:00', 2, 5, 'Anniversary Celebration - Window Seat'),
(2, '2025-05-16 20:00:00', 4, 10, 'Birthday Celebration - Bring Cake'),
(3, '2025-05-17 18:30:00', 6, 14, 'Gluten-Free Dietary Request'),
(4, '2025-05-18 12:00:00', 2, 2, 'Business Lunch - Quiet Table'),
(5, '2025-05-19 19:30:00', 3, 6, 'Vegetarian Meal Required'),
(6, '2025-05-20 18:00:00', 8, 16, 'Large Family Gathering'),
(7, '2025-05-21 19:00:00', 10, 18, 'Private Dining Room - Anniversary'),
(8, '2025-05-22 13:00:00', 1, 1, 'Window Seating Preferred'),
(9, '2025-05-23 18:45:00', 5, 13, 'Birthday Party - Need Extra Cake'),
(10, '2025-05-24 20:00:00', 2, 4, 'Accessible Seating Needed');

-- Insert Orders with specific order_id 16, 17, 18, 19
INSERT INTO orders (order_id, table_id, total_price, order_status, employee_id, order_type, payment_method) 
VALUES 
(16, 5, 72.85, 'Served', 8, 'Dine In', 'Credit Card'),    
(17, 8, 45.90, 'Served', 9, 'Dine In', 'Cash'),  
(18, 2, 28.95, 'Confirmed', 8, 'Dine In', 'Debit Card'),  
(19, 18, 260.00, 'Served', 9, 'Dine In', 'Credit Card');

-- Insert Order Items linked to correct order_ids
-- Order 16 (Dinner for 2: Appetizer + Main + Dessert)
INSERT INTO order_items (order_id, menu_item_id, quantity) VALUES
(16, 11, 1), -- Crispy Calamari (Appetizer)
(16, 16, 1), -- Ribeye Steak (Main)
(16, 27, 1); -- Chocolate Lava Cake (Dessert)

-- Order 17 (Lunch for 1: Main + Beverage)
INSERT INTO order_items (order_id, menu_item_id, quantity) VALUES
(17, 15, 1), -- Grilled Salmon (Main)
(17, 29, 1); -- Fresh Orange Juice (Beverage)

-- Order 18 (Solo Lunch: Main only)
INSERT INTO order_items (order_id, menu_item_id, quantity) VALUES
(18, 8, 1); -- Vegetable Quinoa Bowl (Main)

-- Order 19 (Private Event - Big Combo)
INSERT INTO order_items (order_id, menu_item_id, quantity) VALUES
(19, 12, 3), -- Bruschetta (Appetizer)
(19, 18, 2), -- Thai Green Curry (Main)
(19, 19, 2), -- Truffle Pasta (Main)
(19, 26, 2), -- Autumn Harvest Salad (Seasonal Special)
(19, 37, 2), -- House White Wine (Drink)
(19, 39, 2); -- Craft Lager (Drink)

-- Relevant SELECT Queries

-- 1. List all available tables for seating
SELECT table_number, seating_capacity, availability_status
FROM restaurant_tables
WHERE availability_status = 'available';

-- 2. Display the full current menu with categories
SELECT ms.section_name, msc.subcategory_name, mi.item_name, mi.price, mi.dietary_type
FROM menu_items mi
JOIN menu_subcategories msc ON mi.subcategory_id = msc.subcategory_id
JOIN menu_sections ms ON msc.section_id = ms.section_id
WHERE mi.availability = TRUE;

-- 3. Find the best-selling menu items
SELECT mi.item_name, SUM(oi.quantity) AS total_ordered
FROM order_items oi
JOIN menu_items mi ON oi.menu_item_id = mi.menu_item_id
GROUP BY mi.item_name
ORDER BY total_ordered DESC
LIMIT 10;

-- 4. List all seasonal specials for the current season
SELECT mi.item_name, mis.season_name
FROM menu_item_seasons mis
JOIN menu_items mi ON mis.menu_item_id = mi.menu_item_id
WHERE mis.season_name = 'Summer';

-- 5. Find all items available for Breakfast
SELECT mi.item_name
FROM availability_timings at
JOIN menu_items mi ON at.menu_item_id = mi.menu_item_id
WHERE at.available_in_breakfast = TRUE;

-- 6. Show recent orders with table number and total price
SELECT o.order_id, rt.table_number, o.total_price, o.order_status
FROM orders o
JOIN restaurant_tables rt ON o.table_id = rt.table_id
ORDER BY o.order_timestamp DESC
LIMIT 20;

-- 7. List employees and the number of orders they have handled
SELECT e.employee_name, COUNT(o.order_id) AS total_orders_handled
FROM employee e
LEFT JOIN orders o ON e.employee_id = o.employee_id
GROUP BY e.employee_id, e.employee_name
ORDER BY total_orders_handled DESC;

-- 8. View detailed information about an order (items, quantity, price)
SELECT o.order_id, mi.item_name, oi.quantity, mi.price, (oi.quantity * mi.price) AS item_total
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN menu_items mi ON oi.menu_item_id = mi.menu_item_id
WHERE o.order_id = 16;
