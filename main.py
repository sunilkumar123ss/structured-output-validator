"""A strict, inspectable schema subset for structured model-output adapters."""
import argparse
import json
import math
from pathlib import Path

KEYS={"type","properties","required","additionalProperties","items","enum","minLength","maxLength","minimum","maximum","minItems","maxItems"}
TYPES={"object","array","string","number","integer","boolean","null"}


def finite_number(value):
    return type(value) is int or (type(value) is float and math.isfinite(value))


def loads_strict(text):
    def reject_constant(value):raise ValueError(f"non-finite JSON constant: {value}")
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError(f"duplicate JSON key: {key}")
            result[key]=value
        return result
    return json.loads(text,parse_constant=reject_constant,object_pairs_hook=pairs)

