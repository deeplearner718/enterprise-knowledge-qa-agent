"""重新生成离线示例与测试记录；从仓库根目录运行。"""
import subprocess
import sys
import os
from pathlib import Path

root = Path(__file__).resolve().parents[1]
names = ("clear", "conflict", "outside", "paraphrase", "followup", "failure")
lines = ["环境：Python " + sys.version.split()[0], "模式：mock（非真实模型调用）"]
env = dict(os.environ, PYTHONIOENCODING="utf-8")
for name in names:
    result = subprocess.run([sys.executable, "-m", "src.main", "--input", f"examples/{name}.input.json", "--mode", "mock"], cwd=root, capture_output=True, text=True, encoding="utf-8", env=env)
    if result.returncode:
        raise RuntimeError(f"{name}: {result.stderr}")
    (root / "examples" / f"{name}.output.json").write_text(result.stdout, encoding="utf-8")
    lines.append(f"{name}: 退出码 {result.returncode}，输出 examples/{name}.output.json")
tests = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=root, capture_output=True, text=True, encoding="utf-8", env=env)
lines.extend(["", "测试退出码：" + str(tests.returncode), tests.stdout + tests.stderr])
(root / "examples" / "test-results.txt").write_text("\n".join(lines), encoding="utf-8")
if tests.returncode:
    raise SystemExit(tests.returncode)
