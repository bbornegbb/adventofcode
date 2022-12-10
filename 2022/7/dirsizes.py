#!/usr/bin/env python

from collections import namedtuple

File = namedtuple("File", "name size")


class Directory(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.files = []
        self.subdirs = {}

    def find_subdir(self, name):
        return self.subdirs[name]

    def add_subdir(self, name):
        self.subdirs[name] = Directory(name, self)

    def add_file(self, name, size):
        self.files.append(File(name, size))

    def total_filesize(self):
        return sum(f.size for f in self.files)

    def __str__(self):
        subdirs = "[" + ", ".join(str(sd) for sd in self.subdirs.values()) + "]"
        return f"Directory({self.name}, subdirs={subdirs}, files={self.files}"


def build_dirtree(f):
    root = Directory("/", None)
    for line in f:
        line = line.strip()
        tokens = line.split()
        if line.startswith("$ cd "):
            dirname = tokens[2]
            if dirname == "/":
                cwd = root
            elif dirname == "..":
                cwd = cwd.parent
            else:
                cwd = cwd.find_subdir(dirname)
        elif line.startswith("$ ls"):
            continue
        elif line.startswith("dir "):
            cwd.add_subdir(tokens[1])
        else:  # file entry
            size = int(tokens[0])
            name = tokens[1]
            cwd.add_file(name, size)
    return root


def compute_dirsizes(dirtree):
    total = 0
    for d in dirtree.subdirs.values():
        total += compute_dirsizes(d)
    total += dirtree.total_filesize()
    dirtree.totalsize = total
    return total


def get_dirsizes(dirtree, path=None):
    path = f"{path}/{dirtree.name}" if path else dirtree.name
    for d in dirtree.subdirs.values():
        yield from get_dirsizes(d, path)
    yield (path, dirtree.totalsize)


def analyze(fname):
    with open(fname) as f:
        dirtree = build_dirtree(f)
    print(dirtree)
    print(compute_dirsizes(dirtree))
    print(list(get_dirsizes(dirtree)))
    dirsover100k = sum(ds[1] for ds in get_dirsizes(dirtree) if ds[1] <= 100000)
    totalsize = dirtree.totalsize
    available = 70000000 - totalsize
    required = 30000000 - available
    delcandidates = (ds for ds in get_dirsizes(dirtree) if ds[1] >= required)
    delsize = totalsize
    delname = dirtree.name
    for candidate in delcandidates:
        if candidate[1] < delsize:
            delname, delsize = candidate
    print(
        f"directories over 100k = {dirsover100k:12}\n"
        f"available space = {available:18}\n"
        f"required space = {required:19}\n"
        f"size of deleted directory = {delsize:8}\n"
        f"name of deleted directroy = {delname}"
    )


if __name__ == "__main__":
    # analyze("test.txt")
    analyze("input.txt")
