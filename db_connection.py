import mysql.connector


def get_connection():

    return mysql.connector.connect(
        host="acela.proxy.rlwy.net",
        port=17363,
        user="root",
        password="sbEkfnUaieVZazdjdDxnBotVxWCasNoc",
        database="railway"
    )