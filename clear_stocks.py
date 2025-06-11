import sqlite3

conn = sqlite3.connect("stockmarket.db")

conn.execute("DELETE FROM stocks WHERE indices='NIFTY 50'")
conn.commit()

cursor = conn.execute("SELECT COUNT(*) FROM stocks WHERE indices='NIFTY 50'")
remaining = cursor.fetchone()[0]
print(f"Deleted all stocks under 'NIFTY 50'. Remaining in that category: {remaining}")

conn.close()
