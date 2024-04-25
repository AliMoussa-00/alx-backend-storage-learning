# MySQL advanced

[tasks](https://drive.google.com/file/d/15CmsI0Eh18EfKMHRRkVmWyDaYWXHUI7u/view?usp=drive_linkhttps://drive.google.com/file/d/15CmsI0Eh18EfKMHRRkVmWyDaYWXHUI7u/view?usp=drive_link)

---

## [MySQL cheatsheet](https://intranet.alxswe.com/rltoken/8w9di_hk19DIMSBEV3EayQ "MySQL cheatsheet")

---

## Indexes

In MySQL, indexes are data structures that improve the speed of data retrieval operations on database tables. They work much like the index in a book, allowing MySQL to quickly locate specific rows within a table without having to scan the entire table.

However, they should be used judiciously and tailored to the specific needs of your application to achieve the best performance benefits.

**while using primary keys automatically creates indexes for efficient data access and uniqueness enforcement, depending on your specific query patterns, you may still need to create additional indexes for optimal performance.**

```sql
CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100),
    age INT
);
```

**Now, let's say you frequently query the `customers` table to retrieve customer information based on their email addresses. In this scenario, you might want to create an additional index on the `email` column to improve query performance:**

```sql
CREATE INDEX idx_email ON customers (email);
```

After creating the index on the `email` column, queries that involve filtering or searching by email addresses will likely be faster. When you execute a query that filters or searches based on the `email` column, MySQL can utilize the newly created index to quickly locate the relevant rows without having to scan the entire table sequentially.

---

## MySQL Stored Procedures: A Simple Explanation

### What is a Stored Procedure?

A Stored Procedure is like a pre-written script or a set of SQL statements stored on the database server. It's a reusable piece of code that you can call multiple times without having to rewrite the same SQL queries.

### Why Use Stored Procedures?

1. **Code Reusability**: Instead of writing the same SQL logic in multiple places, you write it once in a Stored Procedure and call it wherever needed.
  
2. **Improved Performance**: Stored Procedures are precompiled and stored on the database server. This means they can execute faster than sending multiple SQL statements over the network.
  
3. **Enhanced Security**: You can grant users permission to execute a Stored Procedure without giving them direct access to the underlying tables. This adds a layer of security to your database.
  

### Anatomy of a Stored Procedure:

1. **Name**: A unique name to identify the Stored Procedure.
  
2. **Parameters**: Optional inputs that you can pass to the Stored Procedure. It's like providing arguments to a function.
  
3. **SQL Statements**: The core logic of the Stored Procedure. It can contain any valid SQL statements, including SELECT, INSERT, UPDATE, DELETE, etc.
  
4. **Variables**: You can declare and use variables within a Stored Procedure to store temporary data.
  
5. **Control Flow Statements**: Similar to programming languages, Stored Procedures support control flow statements like IF-ELSE, WHILE loops, etc.
  
6. **Output Parameters**: Optional outputs that the Stored Procedure can return after execution.
  

### Example:

#### Creating a Stored Procedure:

Before creating a Stored Procedure, remember to change the delimiter to something other than `;`, so that it doesn't interfere with the body of the procedure. After defining the procedure, reset the delimiter back to `;`.

```sql
DELIMITER $$

CREATE PROCEDURE GetCustomerByID (IN customerID INT)
BEGIN
    SELECT * FROM customers WHERE id = customerID;
END $$

DELIMITER ;
```

#### Calling the Stored Procedure:

```sql
CALL GetCustomerByID(123);
```

#### More Examples:

1. **Procedure with Parameters:**

```sql
DELIMITER $$

CREATE PROCEDURE UpdateCustomerEmail (IN customerID INT, IN newEmail VARCHAR(100))
BEGIN
    UPDATE customers SET email = newEmail WHERE id = customerID;
END $$

DELIMITER ;
```

2. **Procedure with Variables and Control Flow:**

```sql
DELIMITER //

CREATE PROCEDURE GetHighValueCustomers ()
BEGIN
    DECLARE minPurchase INT;
    SET minPurchase = 1000;

    SELECT * FROM customers WHERE total_purchase > minPurchase;
END //

DELIMITER ;
```

3. **Procedure with Output Parameters:**

```sql
DELIMITER //

CREATE PROCEDURE GetCustomerCount (OUT totalCustomers INT)
BEGIN
    SELECT COUNT(*) INTO totalCustomers FROM customers;
END //

DELIMITER ;
```

**Example:**

In the following example, we pass user_id through IN parameter to get the user name. Within the procedure, we have used IF ELSEIF and ELSE statement to get user name against multiple user id. The user name will be stored into INOUT parameter user_name.

```sql
CREATE DEFINER=`root`@`127.0.0.1`
PROCEDURE `GetUserName`(INOUT user_name varchar(16),
IN user_id varchar(16))
BEGIN
DECLARE uname varchar(16);
SELECT name INTO uname
FROM user
WHERE userid = user_id;
IF user_id = "scott123" 
THEN
SET user_name = "Scott";
ELSEIF user_id = "ferp6734" 
THEN
SET user_name = "Palash";
ELSEIF user_id = "diana094" 
THEN
SET user_name = "Diana";
END IF;
END

Execute the procedure:

mysql> CALL GetUserName(@A,'scott123')$$
Query OK, 1 row affected (0.00 sec)

mysql> SELECT @A $$
+-------+
| @A    |
+-------+
| Scott |
+-------+
1 row in set (0.00 sec)
```

---

## MySQL Triggers: A Comprehensive Explanation

### What are Triggers?

Triggers are special types of stored procedures that automatically execute in response to certain events on a particular table or view in a database. These events include INSERT, UPDATE, DELETE operations, or even specific column modifications.

### Why Use Triggers?

1. **Automated Actions**: Triggers allow you to automate actions based on changes in the database, reducing the need for manual intervention.
  
2. **Data Integrity**: Triggers help enforce data integrity constraints by executing custom logic before or after data modification operations.
  
3. **Audit Logging**: Triggers can be used to track changes to specific tables by logging information about modifications.
  

### Anatomy of a Trigger:

1. **Event**: The type of operation that triggers the execution of the trigger, such as INSERT, UPDATE, or DELETE.
  
2. **Timing**: Specifies when the trigger should be executed, either before or after the event.
  
3. **Triggering Statement**: The SQL statement or statements that execute when the trigger is activated.
  

### Example:

#### Creating a Trigger:

Before creating a Trigger, remember to change the delimiter to something other than `;`, so that it doesn't interfere with the body of the trigger. After defining the trigger, reset the delimiter back to `;`.

```sql
DELIMITER //

CREATE TRIGGER after_customer_insert
AFTER INSERT ON customers
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (action, table_name, affected_row_id) 
    VALUES ('INSERT', 'customers', NEW.id);
END //

DELIMITER ;
```

#### Explanation:

- **`after_customer_insert`**: Name of the trigger.
- **`AFTER INSERT ON customers`**: Specifies that the trigger should activate after an INSERT operation on the `customers` table.
- **`FOR EACH ROW`**: Indicates that the trigger should execute for each affected row.
- **`BEGIN ... END`**: Body of the trigger containing the SQL statements.
- **`NEW.id`**: Accesses the value of the `id` column of the newly inserted row.

#### More Examples:

1. **Trigger for Audit Logging on UPDATE:**

```sql
DELIMITER //

CREATE TRIGGER after_customer_update
AFTER UPDATE ON customers
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (action, table_name, affected_row_id) 
    VALUES ('UPDATE', 'customers', NEW.id);
END //

DELIMITER ;
```

2. **Trigger for Enforcing Business Rules:**

```sql
DELIMITER //

CREATE TRIGGER before_order_insert
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    IF NEW.total_amount < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Total amount must be positive';
    END IF;
END //

DELIMITER ;
```

3. **Trigger for Cascading Deletes:**

```sql
DELIMITER //

CREATE TRIGGER after_delete_customer
AFTER DELETE ON customers
FOR EACH ROW
BEGIN
    DELETE FROM orders WHERE customer_id = OLD.id;
END //

DELIMITER ;
```

---

## MySQL Views: A Comprehensive Explanation

### What are Views?

Views in MySQL are virtual tables that are derived from one or more tables or other views. They present data from the underlying tables in a structured format, allowing you to query and manipulate the data as if it were a regular table.

### Why Use Views?

1. **Simplified Querying**: Views abstract complex SQL queries, making it easier to retrieve and analyze data from multiple tables.
  
2. **Data Security**: Views can restrict access to specific columns or rows, providing an additional layer of security by hiding sensitive data.
  
3. **Code Reusability**: Views allow you to encapsulate frequently used SQL logic, promoting code reuse and maintainability.
  

### Anatomy of a View:

1. **Query Definition**: The SQL SELECT statement that defines the data displayed by the view.
  
2. **Columns**: The columns returned by the view, which may be derived from one or more tables or other views.
  
3. **Data**: The actual data displayed by the view, which is dynamically generated based on the underlying tables.
  

### Example:

#### Creating a View:

```sql
CREATE VIEW customer_orders AS
SELECT
    c.customer_id,
    c.customer_name,
    o.order_id,
    o.order_date,
    o.total_amount
FROM
    customers c
JOIN
    orders o ON c.customer_id = o.customer_id;
```

#### Explanation:

- **`customer_orders`**: Name of the view.
- **`SELECT ... FROM customers c JOIN orders o ON c.customer_id = o.customer_id`**: SQL query that defines the data returned by the view. It retrieves customer and order information, joining the `customers` and `orders` tables.

#### Querying the View:

```sql
SELECT * FROM customer_orders WHERE customer_name = 'John Doe';
```

#### More Examples:

1. **View with Aggregated Data:**

```sql
CREATE VIEW monthly_sales AS
SELECT
    YEAR(order_date) AS year,
    MONTH(order_date) AS month,
    SUM(total_amount) AS total_sales
FROM
    orders
GROUP BY
    YEAR(order_date), MONTH(order_date);
```

2. **View with Filtered Data:**

```sql
CREATE VIEW active_customers AS
SELECT * FROM customers WHERE last_purchase_date > DATE_SUB(NOW(), INTERVAL 1 YEAR);
```

3. **View with Calculated Columns:**

```sql
CREATE VIEW product_profitability AS
SELECT
    product_id,
    product_name,
    unit_price,
    cost_price,
    (unit_price - cost_price) AS profit_margin
FROM
    products;
```

---

Sure, here's how you can explain creating a function in README text format:

---

## Creating a User-Defined Function (UDF) in MySQL

### What is a User-Defined Function?

A User-Defined Function (UDF) in MySQL is a custom function created by the user to extend the functionality of MySQL. UDFs allow you to perform specific tasks that are not supported by built-in functions.

### How to Create a Function?

To create a UDF in MySQL, you use the `CREATE FUNCTION` statement. Here's the basic syntax:

```sql
CREATE FUNCTION function_name ([parameters])
RETURNS data_type
BEGIN
    -- Function body with SQL statements
END;
```

- `function_name`: The name of the function you want to create.
- `[parameters]`: Optional parameters that the function can accept.
- `RETURNS`: Specifies the data type of the value that the function will return.
- `BEGIN ... END`: The body of the function containing SQL statements.

### Example:

Suppose we want to create a function named `add_numbers` that takes two parameters `num1` and `num2` and returns their sum. Here's how we can do it:

```sql
CREATE FUNCTION add_numbers (num1 INT, num2 INT)
RETURNS INT
BEGIN
    DECLARE result INT;
    SET result = num1 + num2;
    RETURN result;
END;
```

This function adds two numbers and returns the result. Once the function is created, it can be used like any other built-in function in SQL queries