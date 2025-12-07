# crypto_project/cipher_base.py

import os
import sys
from .string_utils import color_string


class CipherBase:
    """
    Base class for Cipher.
    """

    def print_run_header(self, cipher_name, operation, file_path):
        attacking = (operation == "attack")
        sys.stderr.write("Cipher:     {}\n".format(cipher_name))
        sys.stderr.write("Operation:  {}\n".format(color_string(operation, attacking)))
        sys.stderr.write("Input File: {}\n".format(file_path))

    def read_file(self, file_path):
        if not os.path.exists(file_path):
            raise RuntimeError(f"ERROR: File {file_path} does not exist.")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
