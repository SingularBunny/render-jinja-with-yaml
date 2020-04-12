#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright:
#   2018 PM <github.com/perfide>
# License:
#   BSD-3
#   http://directory.fsf.org/wiki/License:BSD_3Clause

"""
Use a yaml-config to render Jinja2 templates
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List

import jinja2
import yaml


def parse_args(args: List[str]):
    parser = argparse.ArgumentParser(
        description='Use a yaml-config to render Jinja2 templates')
    parser.add_argument('-y', '--yaml', type=argparse.FileType('r'), required=True, help='Path to the yaml-config')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--templates', nargs='+', help='Paths to the j2 files or folders')
    parser.add_argument('-o', '--output-folder', help='Path to output files')
    parser.add_argument('-e', '--file-type-extension', help='File Type to generate')
    return parser.parse_args(args)


def main(args: List[str]=sys.argv[1:]) -> None:
    args = parse_args(args)

    with args.yaml as f:
        config = yaml.safe_load(f.read())

    fs_loader = jinja2.FileSystemLoader(args.templates if args.templates else args.templates_folder, encoding='utf-8')
    env = jinja2.Environment(loader=fs_loader)
    for name in env.list_templates():
        if not name.endswith('.j2'):
            continue
        tmpl = env.get_template(name)
        cfn = tmpl.render(**config)
        # strip the trailing '.j2' extension
        output_file = name.rsplit('.', 1)[0]
        output_path = os.path.join(args.output_folder if args.output_folder else
                                   os.getcwd(), output_file + '.' + args.file_type_extension
                                   if args.file_type_extension else output_file)

        if args.output_folder:
            Path(args.output_folder).mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as fh:
            fh.write(cfn)
            # the jinja renderer seems to strip the end-of-file new-line
            fh.write('\n')


if __name__ == '__main__':
    main()
