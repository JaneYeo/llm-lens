import libsql
import inspect

try:
    print(f"connect signature: {inspect.signature(libsql.connect)}")
except Exception as e:
    print(f"Error checking signature: {e}")
