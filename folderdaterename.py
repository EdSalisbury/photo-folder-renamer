#!/usr/bin/env python3
"""
Photo Folder renamer - renames folders to a standardized format
Ed Salisbury <ed.salisbury@gmail.com>
Last Modified: 2020-03-23
"""
import os
import os.path
import argparse
import re


class Renamer:
    def __init__(self, **kwargs):
        self.path = kwargs['path']

    def get_month_num(self, name):
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                  'October', 'November', 'December']
        return months.index(name) + 1

    def match_underscores(self, name):
        matches = re.match(r"(\d\d\d\d)_(\d\d)_(\d\d)(.*)", name)
        if matches:
            m = matches.groups()
            return f"{m[0]}-{m[1]}-{m[2]}{m[3]}"

    def match_months(self, name):
        matches = re.match(r'(\w+) (\d+), (\d+)', name)
        if matches:
            m = matches.groups()
            return f"{int(m[2])}-{self.get_month_num(m[0]):02}-{int(m[1]):02}"

    def match_location(self, name):
        matches = re.match(r'(.*?), (\w+) (\d+), (\d+)$', name)
        if matches:
            m = matches.groups()
            return f"{int(m[3])}-{self.get_month_num(m[1]):02}-{int(m[2]):02} - {m[0]}"

    def rename(self):
        paths = os.listdir(self.path)
        for path in paths:
            new_folder = self.match_underscores(path) or self.match_months(path) or self.match_location(path)

            if new_folder:
                old_path = os.path.join(self.path, path)
                new_path = os.path.join(self.path, new_folder)
                if not os.path.exists(new_path):
                    print(f"Renaming {path} to {new_path}")
                    os.rename(old_path, new_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Renames folders that have certain formats to a standardized"
                                                 " YYYY-MM-DD format")
    parser.add_argument('path', help='directory of folders')

    args = parser.parse_args()

    renamer = Renamer(**vars(args))
    renamer.rename()
