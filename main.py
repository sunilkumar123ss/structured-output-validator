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


def check_schema(schema,depth=0):
    if depth > 16 or not isinstance(schema,dict):raise ValueError("schema must be an object with depth <= 16")
    if set(schema)-KEYS:raise ValueError(f"unsupported schema keywords: {sorted(set(schema)-KEYS)}")
    kind=schema.get("type")
    if not isinstance(kind, str) or kind not in TYPES:raise ValueError("schema requires one supported string type")
    permitted={"type","enum"}
    permitted |= {"object":{"properties","required","additionalProperties"},"array":{"items","minItems","maxItems"},
                  "string":{"minLength","maxLength"},"number":{"minimum","maximum"},"integer":{"minimum","maximum"}}.get(kind,set())
    if set(schema)-permitted:raise ValueError("schema contains constraints inapplicable to its type")
    if "enum" in schema and (not isinstance(schema["enum"],list) or not schema["enum"]):raise ValueError("enum must be a nonempty list")
    if kind == "object":
        props=schema.get("properties",{});required=schema.get("required",[])
        if not isinstance(props,dict) or not all(isinstance(k,str) for k in props):raise ValueError("properties must be an object")
        if not isinstance(required,list) or any(not isinstance(x,str) for x in required) or len(set(required)) != len(required) or set(required)-set(props):raise ValueError("required must name unique declared properties")
        if not isinstance(schema.get("additionalProperties",True),bool):raise ValueError("additionalProperties must be boolean")
        for child in props.values():check_schema(child,depth+1)
    if kind == "array":
        if "items" not in schema:raise ValueError("array schemas require items")
        check_schema(schema["items"],depth+1)
    for key in ("minLength","maxLength","minItems","maxItems"):
        if key in schema and (type(schema[key]) is not int or schema[key] < 0):raise ValueError(f"{key} must be a nonnegative integer")
    for key in ("minimum","maximum"):
        if key in schema and not finite_number(schema[key]):raise ValueError(f"{key} must be finite")
    for lower,upper in (("minLength","maxLength"),("minItems","maxItems"),("minimum","maximum")):
        if lower in schema and upper in schema and schema[lower] > schema[upper]:raise ValueError(f"{lower} exceeds {upper}")


def validate(value,schema):
    check_schema(schema)
    errors=[]
    def visit(data,spec,path,depth=0):
        if depth > 64:
            errors.append(f"{path}: nesting limit exceeded");return
        kind=spec["type"]
        matches={"object":isinstance(data,dict),"array":isinstance(data,list),"string":isinstance(data,str),
                 "number":finite_number(data),"integer":type(data) is int,
                 "boolean":type(data) is bool,"null":data is None}[kind]
        if not matches:errors.append(f"{path}: expected {kind}");return
        if "enum" in spec and not any(type(data) is type(option) and data == option for option in spec["enum"]):
            errors.append(f"{path}: value is not in enum")
        if kind == "object":
            props=spec.get("properties",{})
            for key in spec.get("required",[]):
                if key not in data:errors.append(f"{path}.{key}: required field missing")
            for key,child in data.items():
                if key in props:visit(child,props[key],f"{path}.{key}",depth+1)
                elif not spec.get("additionalProperties",True):errors.append(f"{path}.{key}: unexpected field")
        elif kind == "array":
            for index,child in enumerate(data):visit(child,spec["items"],f"{path}[{index}]",depth+1)
        if kind in {"array","string"}:
            minimum,maximum=("minItems","maxItems") if kind == "array" else ("minLength","maxLength")
            if minimum in spec and len(data) < spec[minimum]:errors.append(f"{path}: below {minimum}")
            if maximum in spec and len(data) > spec[maximum]:errors.append(f"{path}: exceeds {maximum}")
        elif kind in {"number","integer"}:
            if "minimum" in spec and data < spec["minimum"]:errors.append(f"{path}: below minimum")
            if "maximum" in spec and data > spec["maximum"]:errors.append(f"{path}: exceeds maximum")
    visit(value,schema,"$")
    return errors

