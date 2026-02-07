import libsql
try:
    print("libsql imported successfully")
    print(f"Version: {getattr(libsql, '__version__', 'unknown')}")
    print(f"Attributes: {dir(libsql)}")
except Exception as e:
    print(f"Error: {e}")
