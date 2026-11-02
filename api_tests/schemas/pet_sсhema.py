
PET_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "category": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
            "required": ["id", "name"],
        },
        "photoUrls": {
            "type": "array",
            "items": {"type": "string"},
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                },
                "required": ["id", "name"],
            }
        },
        "status": {
            "type": "string",
            "enum": ["available", "pending", "sold"],
        }
    },
    "required": ["id", "name", "status"]
}


PET_LIST_SCHEMA = {
    "type": "array",
    "items": PET_SCHEMA
}


ERROR_SCHEMA = {
    "type": "object",
    "properties": {
        "code": {"type": "integer"},
        "type": {"type": "string"},
        "message": {"type": "string"}
    },
    "required": ["code", "type", "message"]

}