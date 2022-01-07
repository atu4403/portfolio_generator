from cerberus import Validator, schema


def validate(yml_object: dict) -> str:
    if not isinstance(yml_object, dict):
        return "invalid: must be of dict type"
    schema = {
        "template": {"type": "string", "required": True},
        "created_at": {"type": "string"},
        "user": {"type": "string"},
        "names": {
            "type": "dict",
            "schema": {
                "github": {"type": "string"},
                "qiita": {"type": "string"},
                "zenn": {"type": "string"},
            },
        },
        "apis": {
            "type": "dict",
            "schema": {},
        },
    }
    if yml_object.get("apis"):
        for key in yml_object["apis"]:
            schema["apis"]["schema"][key] = {
                "type": "dict",
                "schema": {
                    "url": {"type": "string", "required": True},
                    "type": {
                        "type": "string",
                        "required": True,
                        "allowed": ["json", "rss", "xml"],
                    },
                },
            }
    # print("===============", schema)
    v = Validator(schema)
    if v.validate(yml_object):
        return None
    return f"invalid: {v.errors}"
