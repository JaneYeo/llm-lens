import libsql
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("TURSO_DATABASE_URL")
token = os.getenv("TURSO_AUTH_TOKEN")

print(f"URL: {url}")
print(f"Token length: {len(token) if token else 0}")

try:
    conn = libsql.connect("test_turso.db", sync_url=url, auth_token=token)
    print("Connecting...")
    conn.sync()
    print("Sync successful!")
    cur = conn.cursor()
    cur.execute("SELECT 1")
    print(f"Result: {cur.fetchone()}")
    conn.close()
except Exception as e:
    print(f"Failed: {e}")
