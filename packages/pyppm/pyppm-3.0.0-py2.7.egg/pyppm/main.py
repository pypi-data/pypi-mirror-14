#!/usr/bin/env python

import os
import sys
import argparse
import tempfile
from getpass import getpass
from Crypto.Cipher import AES

DECRYPTED_STRING = "Don't DELETE THI LINE"


def parse():
    p = argparse.ArgumentParser()
    p.add_argument("-n", dest="new", action="store_true", help="create a new file and encrypt it")
    p.add_argument("-r", dest="rewrite", action="store_true", help="rewrite an encripted file")
    p.add_argument("--editor", dest="editor", default="vim")
    p.add_argument("source")
    return p.parse_args()


def edit_file(lines, editor):
    import subprocess

    if lines[:len(DECRYPTED_STRING)] != DECRYPTED_STRING:
        print("The file can't be decrypted")
        return

    with tempfile.NamedTemporaryFile("w+f") as tf:
        tf.write(lines)
        tf.file.flush()

        environ = os.environ.copy()
        cmd = '%s "%s"' % (editor, tf.name)
        c = subprocess.Popen(cmd, env=environ, shell=True)
        c.wait()

        tf.file.seek(0)
        return tf.read()


class AESHandler(object):

    def __init__(self, bit=32, master_key=None):
        self.bit = bit
        self.aes_format = "%{bit}s".format(bit=bit)
        self.master_key = master_key

    def _make_aes(self, master_key=None):
        if master_key is None:
            master_key = self.master_key
        aes = AES.new(self.aes_format % master_key)
        return aes

    def encrypt(self, x, master_key=None):
        aes = self._make_aes(master_key=master_key)
        return aes.encrypt(self.aes_format % x)

    def decrypt(self, x, aes=None):
        if aes is None:
            aes = self._make_aes()
        try:
            return aes.decrypt(x).decode()
        except UnicodeDecodeError:
            return aes.decrypt(x)

    def encrypt_lines(self, strings):
        lines = []
        for l in strings.split("\n"):
            if len(l) > self.bit:
                raise ValueError("too long string")
            lines.append(l)
        return b"".join([self.encrypt(l) for l in lines])

    def decrypt_lines(self, strings):
        lines = []
        while strings:
            lines.append(strings[:self.bit])
            strings = strings[self.bit:]

        return "\n".join([self.decrypt(l).lstrip() for l in lines])


def main():
    args = parse()
    master_key = getpass("master key> ")
    handler = AESHandler(master_key=master_key)

    if args.new:
        if os.path.isfile(args.source):
            print("%s exists already" % args.source)
            sys.exit(1)
        lines = DECRYPTED_STRING
    elif args.rewrite:
        with open(args.source, "r") as f:
            lines = handler.decrypt_lines(f.read())
    else:
        print("Nothing Done. Try --help")
        sys.exit(1)

    new = edit_file(lines, args.editor)
    if new:
        with open(args.source, "w") as f:
            f.write(handler.encrypt_lines(new))
    else:
        print("Nothing to write")
        sys.exit(1)

if __name__ == '__main__':
    main()
