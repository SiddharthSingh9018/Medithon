import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.store import STORE

if __name__ == "__main__":
    STORE.load()
    STORE.save()
    print("Store initialized")
