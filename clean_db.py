import sqlite3

# Connect to the database
conn = sqlite3.connect('knowledge.db')
cursor = conn.cursor()

# Clean up existing tables
cursor.execute("DELETE FROM sessions")
cursor.execute("DELETE FROM messages")
cursor.execute("DELETE FROM query_cache")
cursor.execute("DELETE FROM interaction_log")

# Commit changes and close
conn.commit()
conn.close()
print("Database cleaned successfully!")
