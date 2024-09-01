import unittest
# Load this project's module explicitly, including when invoked from repository root.
import importlib.util as _import_util
from pathlib import Path as _Path
import sys as _sys
_spec = _import_util.spec_from_file_location(
    "sunil_agents_" + _Path(__file__).parent.name, _Path(__file__).with_name("main.py"))
_main = _import_util.module_from_spec(_spec)
_sys.modules[_spec.name] = _main
_spec.loader.exec_module(_main)
validate = _main.validate
loads_strict = _main.loads_strict

class SchemaTests(unittest.TestCase):
    def test_nested_success_and_bad_item_path(self):
        schema={"type":"array","items":{"type":"integer","minimum":0}}
        self.assertEqual(validate([0,1,2],schema),[])
        self.assertIn("$[1]",validate([0,-1],schema)[0])

