"""
Assign articles from AmCAT sets for background processing in nlpipe
"""

import sys, argparse

from nlpipe import tasks
from nlpipe.pipeline import parse_background
from nlpipe.celery import app

modules = {n.split(".")[-1]: t for (n,t) in app.tasks.iteritems() if n.startswith("nlpipe")}

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('module', help='nlpipe module (task) name ({})'.format(", ".join(sorted(modules))),
                    choices=modules, metavar="module")
parser.add_argument('--adhoc', help='Ad hoc: parse sentence directly (provide sentence instead of ids)',
                    action='store_true', default=False)
parser.add_argument('target', nargs='+', help='Article id(s) (or text in adhoc mode)')

args = parser.parse_args()
task = modules[args.module]

if args.adhoc:
    text = " ".join(args.target)
    result = task.process(text)
    print result
else:
    aids = [int(x) for x in args.target]
    for aid in aids:
        task.run(aid)
