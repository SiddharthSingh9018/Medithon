import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.services.context_extraction import extract_context_for_mentions
from app.services.perception_derivation import derive_perception_for_mentions

if __name__ == "__main__":
    print(extract_context_for_mentions())
    print(derive_perception_for_mentions())
