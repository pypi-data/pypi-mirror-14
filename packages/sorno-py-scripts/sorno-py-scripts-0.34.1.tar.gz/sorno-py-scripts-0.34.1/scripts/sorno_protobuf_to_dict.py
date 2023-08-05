#!/usr/bin/env python
"""sorno_protobuf_to_dict.py converts text format of protobufs to python dict.

The script launches ipython for you to play with the parsed python dict.


    Copyright 2016 Heung Ming Tai

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import argparse
import re
import sys

from sorno import debuggingutil


class App(object):
    def __init__(self, args):
        self.args = args

    def run(self):
        with open(self.args.file) as f:
            content = f.read().strip()

        # make any protobuf field key which has protobuf value  to be a dict key
        # fld {...} => "fld": {...}
        obj_str = re.sub(r'([^ ]+) \{', r'"\1": {', content)

        # make any non-protobuf field to be a dict key
        # fld: ... => "fld": ...
        obj_str = re.sub(r'([^ "]+): ', r'"\1": ', obj_str)

        # separate all fields...
        # "fld": 123 => "fld": 123,
        obj_str = re.sub("(?<!\{)\n", ",\n", obj_str)
        # make it a root dict
        obj_str = "{%s}" % obj_str

        print("Your object before python eval:")
        print(obj_str)

        header = "Your object is in the variable: obj"
        header += "\nThe following functions are available: "
        functions = ("pprint",)
        header += ",".join(sorted(functions))

        from pprint import pprint
        obj = eval(obj_str)

        debuggingutil.ipython_here(header=header)

        return 0


def parse_args(cmd_args):
    description = __doc__.split("Copyright 2016")[0].strip()

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "file"
    )

    args = parser.parse_args(cmd_args)
    return args


def main():
    args = parse_args(sys.argv[1:])

    app = App(args)
    sys.exit(app.run())


if __name__ == '__main__':
    main()
