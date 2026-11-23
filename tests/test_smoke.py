import importlib
import io
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout

from word_processor import __version__, cli


class ModuleSmoke(unittest.TestCase):
    def test_modules_import(self):
        for name in ("model", "server", "storage", "docx_write", "docx_read", "cli"):
            with self.subTest(module=name):
                importlib.import_module(f"word_processor.{name}")


class CliSmoke(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "word_processor", *args],
            capture_output=True, text=True,
        )

    def test_help(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage:", result.stdout)

    def test_version(self):
        result = self.run_cli("--version")
        self.assertEqual(result.returncode, 0)
        self.assertIn(__version__, result.stdout)

    def test_serve_is_a_stub(self):
        err = io.StringIO()
        with redirect_stderr(err), redirect_stdout(io.StringIO()):
            code = cli.main(["serve"])
        self.assertNotEqual(code, 0)
        self.assertIn("not implemented yet: see #2", err.getvalue())
