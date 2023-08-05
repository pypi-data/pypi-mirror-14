# -*- coding: utf-8 -*-

import subprocess


def current_sha():
    return subprocess.check_output(
        ['git', 'rev-parse', 'HEAD']
    ).strip().decode('utf-8')


def diff(start, end):
    return subprocess.check_output(
        ['git', 'diff', '-M', start + '..' + end]
    ).strip().decode('utf-8')


def parent_sha(sha):
    return subprocess.check_output(
        ['git', 'rev-list', '--parents', '-n', '1', sha]
    ).strip().decode('utf-8').split()[1]
