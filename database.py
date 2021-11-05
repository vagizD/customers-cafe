"""
The database interacting module.
Functions to implement:
create_table()
    add_customer(phone_number, surname, name, date_of_registration)
    delete_customer(phone_number)
    add_expenses(phone_number, expenses)
        get_certain_customer(phone_number)  # returns a dictionary with data
        get_customers()  # returns a list of dictionaries
        get_bonus_info(bonus_card)  # returns number of customers and list of dictionaries with data
        top_bottom_customers(number, order, criteria)  # returns X top/bottom customers by parameter.
"""

import sqlite3

customers_database = 'customers_database.db'


def create_table():
    connection = sqlite3.connect(customers_database)
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS customers (phone_number integer primary key, surname text, name text, '
                   'date_of_registration integer, total_expenses integer, bonus_card text)')

    connection.commit()
    connection.close()


def add_customer(phone_number, surname, name, date_of_registration):
    date_of_registration = date_of_registration.split("/")
    time = ""
    for date in date_of_registration:
        time = time + date

    connection = sqlite3.connect(customers_database)
    cursor = connection.cursor()

    cursor.execute('INSERT INTO customers VALUES (?, ?, ?, ?, 0, "standard")', (phone_number, surname, name,
                                                                                time))

    connection.commit()
    connection.close()


def delete_customer(phone_number):
    connection = sqlite3.connect(customers_database)
    cursor = connection.cursor()

    cursor.execute('DELETE FROM customers WHERE phone_number = ?', (phone_number,))

    connection.commit()
    connection.close()


def add_expenses(phone_number, expenses, update):  # also updates bonus card level
    customer = get_certain_customer(phone_number)
    amount = expenses + customer['total_expenses']

    connection = sqlite3.connect(customers_database)
    cursor = connection.cursor()

    cursor.execute('UPDATE customers SET total_expenses = ? WHERE phone_number = ?', (amount, phone_number))
    cursor.execute('UPDATE customers SET bonus_card = ? WHERE phone_number = ?', (update, phone_number))

    connection.commit()
    connection.close()


def get_certain_customer(phone_number):
    connection = sqlite3.connect(customers_database)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM customers WHERE phone_number = ?', (phone_number,))

    customer = cursor.fetchall()[0]

    connection.close()

    return {'phone_number': int(f"+7{customer[0]}"), 'surname': customer[1], 'name': customer[2], 'date_of_registration':
            customer[3], 'total_expenses': customer[4], 'bonus_card': customer[5]}


def get_customers():
    connection = sqlite3.connect(customers_database)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM customers')

    customers = [{'phone_number': int(f"+7{customer[0]}"), 'surname': customer[1], 'name': customer[2], 'date_of_registration':
                 customer[3], 'total_expenses': customer[4], 'bonus_card': customer[5]}
                 for customer in cursor.fetchall()
                 ]

    connection.close()

    return customers


def get_bonus_info(bonus_card):
    connection = sqlite3.connect(customers_database)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM customers WHERE bonus_card = ?', (bonus_card,))

    bonus_card_customers = [{'phone_number': int(f"+7{customer[0]}"), 'surname': customer[1], 'name': customer[2],
                             'date_of_registration': customer[3], 'total_expenses': customer[4], 'bonus_card':
                             customer[5]} for customer in cursor.fetchall()]

    connection.close()

    return bonus_card_customers


def top_bottom_customers(number, order, criteria):  # integer, 'ASC'/'DESC', integer (1 or 2)
    connection = sqlite3.connect(customers_database)
    cursor = connection.cursor()

    if criteria == 1:
        cursor.execute(f'SELECT * FROM customers ORDER BY date_of_registration {order}')
    else:
        cursor.execute(f'SELECT * FROM customers ORDER BY total_expenses {order}')

    customers = [{'phone_number': int(f"+7{customer[0]}"), 'surname': customer[1], 'name': customer[2], 'date_of_registration':
                  customer[3], 'total_expenses': customer[4], 'bonus_card':
                  customer[5]} for customer in cursor.fetchmany(number)]

    connection.close()

    return customers
