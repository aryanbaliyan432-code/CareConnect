from bson import ObjectId
from datetime import datetime


def fmt(doc: dict) -> dict:
    """Convert MongoDB document to JSON-serializable dict."""
    if doc is None:
        return None
    result = {}
    for key, val in doc.items():
        if key == "_id":
            result["id"] = str(val)
        elif isinstance(val, ObjectId):
            result[key] = str(val)
        elif isinstance(val, datetime):
            result[key] = val.isoformat()
        elif isinstance(val, dict):
            result[key] = fmt(val)
        elif isinstance(val, list):
            result[key] = [fmt(i) if isinstance(i, dict) else i for i in val]
        else:
            result[key] = val
    return result
