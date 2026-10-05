"""从任意工作目录运行指定章节。"""
from pathlib import Path
import argparse
import subprocess
import sys
p = argparse.ArgumentParser()
p.add_argument("--chapters", default=",".join(map(str, range(1, 13))))
a = p.parse_args()
try:
    chapters = list(dict.fromkeys(int(x) for x in a.chapters.split(",")))
except ValueError:
    p.error("章节必须是逗号分隔的整数")
if not chapters or any(c not in range(1, 13) for c in chapters):
    p.error("章节范围为 1–12")
root = Path(__file__).resolve().parent
for c in chapters:
    subprocess.run([sys.executable, str(root / f"CH{c:02}/run.py")], check=True)
