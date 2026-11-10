CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    city TEXT
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount REAL NOT NULL,
    order_date TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

INSERT INTO customers (name, email, city) VALUES
('Rahul Sharma', 'rahul@example.com', 'Delhi'),
('Priya Singh', 'priya@example.com', 'Mumbai'),
('Aman Verma', 'aman@example.com', 'Bangalore'),
('Neha Gupta', 'neha@example.com', 'Delhi');

INSERT INTO orders (customer_id, amount, order_date) VALUES
(1, 2500.00, '2026-01-10'),
(1, 1800.00, '2026-02-15'),
(2, 4200.00, '2026-01-20'),
(3, 1200.00, '2026-02-05'),
(3, 3500.00, '2026-03-12'),
(4, 5000.00, '2026-03-18');