#!/usr/bin/env python3
import contextlib
import io
import textwrap
import unittest

import bytecode
from bytecode import Label, Instr, Bytecode, Block, BytecodeBlocks
from bytecode.tests import disassemble


class DumpCodeTests(unittest.TestCase):
    maxDiff = 80 * 100

    def check_dump_bytecode(self, code, expected, lineno=None):
        with contextlib.redirect_stdout(io.StringIO()) as stderr:
            if lineno is not None:
                bytecode.dump_bytecode(code, lineno=True)
            else:
                bytecode.dump_bytecode(code)
            output = stderr.getvalue()

        self.assertEqual(output, expected)

    def test_bytecode(self):
        source = """
            def func(test):
                if test == 1:
                    return 1
                elif test == 2:
                    return 2
                return 3
        """
        code = disassemble(source, function=True)
        code = code.to_bytecode()

        # without line numbers
        expected = """
    LOAD_FAST 'test'
    LOAD_CONST 1
    COMPARE_OP 2
    POP_JUMP_IF_FALSE <label_instr6>
    LOAD_CONST 1
    RETURN_VALUE

label_instr6:
    LOAD_FAST 'test'
    LOAD_CONST 2
    COMPARE_OP 2
    POP_JUMP_IF_FALSE <label_instr13>
    LOAD_CONST 2
    RETURN_VALUE

label_instr13:
    LOAD_CONST 3
    RETURN_VALUE

        """[1:].rstrip(" ")
        self.check_dump_bytecode(code, expected)

        # with line numbers
        expected = """
    L.  2   0: LOAD_FAST 'test'
            1: LOAD_CONST 1
            2: COMPARE_OP 2
            3: POP_JUMP_IF_FALSE <label_instr6>
    L.  3   4: LOAD_CONST 1
            5: RETURN_VALUE

label_instr6:
    L.  4   7: LOAD_FAST 'test'
            8: LOAD_CONST 2
            9: COMPARE_OP 2
           10: POP_JUMP_IF_FALSE <label_instr13>
    L.  5  11: LOAD_CONST 2
           12: RETURN_VALUE

label_instr13:
    L.  6  14: LOAD_CONST 3
           15: RETURN_VALUE

        """[1:].rstrip(" ")
        self.check_dump_bytecode(code, expected, lineno=True)

    def test_bytecode_broken_label(self):
        label = Label()
        code = Bytecode([Instr('JUMP_ABSOLUTE', label)])

        expected = "    JUMP_ABSOLUTE <error: unknown label>\n\n"
        self.check_dump_bytecode(code, expected)

    def test_blocks_broken_jump(self):
        block = Block()
        code = BytecodeBlocks()
        code[0].append(Instr('JUMP_ABSOLUTE', block))

        expected = textwrap.dedent("""
            label_block1:
                JUMP_ABSOLUTE <error: unknown block>

        """).lstrip("\n")
        self.check_dump_bytecode(code, expected)

    def test_bytecode_blocks(self):
        source = """
            def func(test):
                if test == 1:
                    return 1
                elif test == 2:
                    return 2
                return 3
        """
        code = disassemble(source, function=True)

        # without line numbers
        expected = textwrap.dedent("""
            label_block1:
                LOAD_FAST 'test'
                LOAD_CONST 1
                COMPARE_OP 2
                POP_JUMP_IF_FALSE <label_block3>
                -> label_block2

            label_block2:
                LOAD_CONST 1
                RETURN_VALUE

            label_block3:
                LOAD_FAST 'test'
                LOAD_CONST 2
                COMPARE_OP 2
                POP_JUMP_IF_FALSE <label_block5>
                -> label_block4

            label_block4:
                LOAD_CONST 2
                RETURN_VALUE

            label_block5:
                LOAD_CONST 3
                RETURN_VALUE

        """).lstrip()
        self.check_dump_bytecode(code, expected)

        # with line numbers
        expected = textwrap.dedent("""
            label_block1:
                L.  2   0: LOAD_FAST 'test'
                        1: LOAD_CONST 1
                        2: COMPARE_OP 2
                        3: POP_JUMP_IF_FALSE <label_block3>
                -> label_block2

            label_block2:
                L.  3   0: LOAD_CONST 1
                        1: RETURN_VALUE

            label_block3:
                L.  4   0: LOAD_FAST 'test'
                        1: LOAD_CONST 2
                        2: COMPARE_OP 2
                        3: POP_JUMP_IF_FALSE <label_block5>
                -> label_block4

            label_block4:
                L.  5   0: LOAD_CONST 2
                        1: RETURN_VALUE

            label_block5:
                L.  6   0: LOAD_CONST 3
                        1: RETURN_VALUE

        """).lstrip()
        self.check_dump_bytecode(code, expected, lineno=True)

    def test_concrete_bytecode(self):
        source = """
            def func(test):
                if test == 1:
                    return 1
                elif test == 2:
                    return 2
                return 3
        """
        code = disassemble(source, function=True)
        code = code.to_concrete_bytecode()

        # without line numbers
        expected = """
  0    LOAD_FAST 0
  3    LOAD_CONST 1
  6    COMPARE_OP 2
  9    POP_JUMP_IF_FALSE 16
 12    LOAD_CONST 1
 15    RETURN_VALUE
 16    LOAD_FAST 0
 19    LOAD_CONST 2
 22    COMPARE_OP 2
 25    POP_JUMP_IF_FALSE 32
 28    LOAD_CONST 2
 31    RETURN_VALUE
 32    LOAD_CONST 3
 35    RETURN_VALUE
""".lstrip("\n")
        self.check_dump_bytecode(code, expected)

        # with line numbers
        expected = """
L.  2   0: LOAD_FAST 0
        3: LOAD_CONST 1
        6: COMPARE_OP 2
        9: POP_JUMP_IF_FALSE 16
L.  3  12: LOAD_CONST 1
       15: RETURN_VALUE
L.  4  16: LOAD_FAST 0
       19: LOAD_CONST 2
       22: COMPARE_OP 2
       25: POP_JUMP_IF_FALSE 32
L.  5  28: LOAD_CONST 2
       31: RETURN_VALUE
L.  6  32: LOAD_CONST 3
       35: RETURN_VALUE
""".lstrip("\n")
        self.check_dump_bytecode(code, expected, lineno=True)


class MiscTests(unittest.TestCase):
    def test_version(self):
        import setup
        self.assertEqual(bytecode.__version__, setup.VERSION)


if __name__ == "__main__":
    unittest.main()
