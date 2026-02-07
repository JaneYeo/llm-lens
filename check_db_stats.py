import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), 'llm_lens.db')

def check_counts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("Article counts by Source and Status:")
    cursor.execute('''
        SELECT source, status, COUNT(*) as count 
        FROM articles 
        GROUP BY source, status
        ORDER BY source, status
    ''')
    rows = cursor.fetchall()
    for row in rows:
        print(f"Source: {row['source']:<25} | Status: {row['status']:<15} | Count: {row['count']}")
    
    conn.close()

if __name__ == "__main__":
    check_counts()
