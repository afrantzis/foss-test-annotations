import argparse
import glob
import math
import numpy
import sys

def percent(a, b):
    if a == 0 and b == 0: return 0.0
    return 100.0 * float(a) / (float(a) + float(b))

def avg(v, n): return float(v) / n

def process_stats_file(f):
    size_test = 0
    size_not_test = 0
    commits_test = 0
    commits_not_test = 0

    for l in f:
        if l.startswith("[file]"):
            (size, kind) = l.split()[-2:]
            if kind == "Test":
                size_test += int(size)
            elif kind == "NotTest":
                size_not_test += int(size)
        elif l.startswith("[commit]"):
            kind = l.split()[-1]
            if kind == "Test":
                commits_test += 1
            else:
                commits_not_test += 1

    return (percent(commits_test, commits_not_test), percent(size_test, size_not_test))

parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--list', action='store_true')
parser.add_argument('sources', nargs='+')
args = parser.parse_args()

files = []
for source in args.sources:
    if source.endswith(".stats") or source.endswith(".ta"):
        files.append(source)
    else:
        files.extend(glob.glob(source + "/*.stats"))
        files.extend(glob.glob(source + "/*.ta"))

stats = []
for fn in files:
    with open(fn, "r") as f:
        s = process_stats_file(f)
        if args.list:
            print("%s %.1f %.1f" % tuple([fn] + list(s)))
        stats.append(s)

if not args.list:
    stats_non_zero = [s for s in stats if s[0] > 0.1 and s[1] > 0.1]

    if len(stats_non_zero) > 0:
        non_zero_mean = tuple(numpy.mean(stats_non_zero, axis = 0))
    else:
        non_zero_mean = (0.0, 0.0)
    mean = tuple(numpy.mean(stats, axis = 0))
    percentile_50 = tuple(numpy.percentile(stats, 50.0, axis = 0))
    percentile_60 = tuple(numpy.percentile(stats, 60.0, axis = 0))
    percentile_70 = tuple(numpy.percentile(stats, 70.0, axis = 0))
    percentile_80 = tuple(numpy.percentile(stats, 80.0, axis = 0))
    percentile_90 = tuple(numpy.percentile(stats, 90.0, axis = 0))
    if len(stats) > 1:
        cor = numpy.corrcoef(stats, rowvar = False)[0][1]
    else:
        cor = 1.0

    print("[Mean-NonZero] Commits: %.1f Size: %.1f" % non_zero_mean)
    print("[Mean] Commits: %.1f Size: %.1f" % mean)
    print("[50%%-Percentile] Commits: %.1f Size: %.1f" % percentile_50)
    print("[60%%-Percentile] Commits: %.1f Size: %.1f" % percentile_60)
    print("[70%%-Percentile] Commits: %.1f Size: %.1f" % percentile_70)
    print("[80%%-Percentile] Commits: %.1f Size: %.1f" % percentile_80)
    print("[90%%-Percentile] Commits: %.1f Size: %.1f" % percentile_90)
    print("[pearson-cor] %.2f" % (cor,))
    print("[%%-WithTests]: %.1f" % (100.0 * len(stats_non_zero) / len(stats),))
