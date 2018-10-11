# if __name__ == "__main__":
#
#     # import the sqlite3 module
#     import sqlite3
#
#     # Create a connection object
#     connection = sqlite3.connect("searchListings.db")
#
#     # Get a cursor
#     cursor = connection.cursor()
#
#     # Rename the SQLite Table
#     renameTable = "ALTER TABLE itemlistings ADD COLUMN likes Integer"
#
#     cursor.execute(renameTable)
#     exit()
