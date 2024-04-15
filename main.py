"""A strict, inspectable schema subset for structured model-output adapters."""
import argparse
import json
import math
from pathlib import Path

KEYS={"type","properties","required","additionalProperties","items","enum","minLength","maxLength","minimum","maximum","minItems","maxItems"}
TYPES={"object","array","string","number","integer","boolean","null"}


def finite_number(value):
    return type(value) is int or (type(value) is float and math.isfinite(value))

