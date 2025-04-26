import time
import socket
import os

DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = int(os.getenv('DB_PORT', 3306))

def wait_for_db():
    while True:
        try:
            sock = socket.create_connection((DB_HOST, DB_PORT), timeout=2)
            sock.close()
            print("Database is ready!")
            break
        except OSError:
            print("Waiting for database...")
            time.sleep(2)

if __name__ == "__main__":
    wait_for_db()
