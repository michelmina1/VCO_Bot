import pyodbc
import json

# Load database configuration from botconfig.json
with open('botconfig.json', 'r') as config_file:
    config = json.load(config_file)

connection_string = config['database']['connection_string']

def update_users(user_id, new_data):
    """
    Update the Users table.
    :param user_id: ID of the user to update.
    :param new_data: Dictionary containing the new data for the user.
    """
    update_query = """
    UPDATE Users
    SET name = ?, email = ?, age = ?
    WHERE id = ?
    """
    insert_query = """
    INSERT INTO Users (id, name, email, age)
    VALUES (?, ?, ?, ?)
    """
    update_params = (new_data['name'], new_data['email'], new_data['age'], user_id)
    insert_params = (user_id, new_data['name'], new_data['email'], new_data['age'])
    execute_query(update_query, update_params, insert_query, insert_params)

def update_orders(order_id, new_data):
    """
    Update the Orders table.
    :param order_id: ID of the order to update.
    :param new_data: Dictionary containing the new data for the order.
    """
    update_query = """
    UPDATE Orders
    SET product_id = ?, quantity = ?, order_date = ?
    WHERE id = ?
    """
    insert_query = """
    INSERT INTO Orders (id, product_id, quantity, order_date)
    VALUES (?, ?, ?, ?)
    """
    update_params = (new_data['product_id'], new_data['quantity'], new_data['order_date'], order_id)
    insert_params = (order_id, new_data['product_id'], new_data['quantity'], new_data['order_date'])
    execute_query(update_query, update_params, insert_query, insert_params)

def update_products(product_id, new_data):
    """
    Update the Products table.
    :param product_id: ID of the product to update.
    :param new_data: Dictionary containing the new data for the product.
    """
    update_query = """
    UPDATE Products
    SET name = ?, price = ?, stock = ?
    WHERE id = ?
    """
    insert_query = """
    INSERT INTO Products (id, name, price, stock)
    VALUES (?, ?, ?, ?)
    """
    update_params = (new_data['name'], new_data['price'], new_data['stock'], product_id)
    insert_params = (product_id, new_data['name'], new_data['price'], new_data['stock'])
    execute_query(update_query, update_params, insert_query, insert_params)

def execute_query(update_query, update_params, insert_query, insert_params):
    """
    Execute a given update query with parameters. If no rows are affected, execute an insert query.
    :param update_query: SQL update query to execute.
    :param update_params: Parameters for the SQL update query.
    :param insert_query: SQL insert query to execute if update affects no rows.
    :param insert_params: Parameters for the SQL insert query.
    """
    try:
        with pyodbc.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(update_query, update_params)
                if cursor.rowcount == 0:
                    cursor.execute(insert_query, insert_params)
                conn.commit()
    except pyodbc.Error as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    # Update a user
    update_users(1, {'name': 'John Doe', 'email': 'john.doe@example.com', 'age': 30})

    # Update an order
    update_orders(1, {'product_id': 2, 'quantity': 5, 'order_date': '2023-10-01'})

    # Update a product
    update_products(1, {'name': 'New Product', 'price': 19.99, 'stock': 100})