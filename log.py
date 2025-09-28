import os
import random
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path

# 仓库路径（脚本需在仓库根目录运行）
repo_path = Path(__file__).resolve().parent
print("Repository:", repo_path)

# 固定时间范围：2016-09-05 到 2025-09-26
start_date = datetime(2021, 6, 1).date()
end_date   = datetime(2022, 6, 11).date()

def safe_git(cmd, env=None):
    """执行 git 命令，若 index.lock 存在或出错则跳过"""
    lock_file = repo_path / ".git" / "index.lock"
    if lock_file.exists():
        print(f"跳过命令 {' '.join(cmd)} —— index.lock 存在")
        return False
    try:
        subprocess.run(cmd, env=env, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"跳过失败命令: {' '.join(cmd)}")
        return False

current = start_date
day_counter = 0

while current <= end_date:
    day_counter += 1

    # 每 10 天随机跳过 1 天
    if day_counter % 3 == 0 and random.choice([True, False]):
        print(f"跳过整天 {current}")
        current += timedelta(days=1)
        continue

    commits_today = random.randint(1, 10)
    for _ in range(commits_today):
        # 随机当天时间
        h, m, s = random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)
        commit_dt = datetime(current.year, current.month, current.day, h, m, s)
        filename = commit_dt.strftime("%Y%m%d_%H%M%S") + ".txt"
        file_path = repo_path / filename

        # 创建临时文件
        file_path.write_text(f"commit at {commit_dt.isoformat()}\n")

        # 设置提交时间环境变量
        env = os.environ.copy()
        date_str = commit_dt.strftime("%Y-%m-%d %H:%M:%S")
        env["GIT_AUTHOR_DATE"] = date_str
        env["GIT_COMMITTER_DATE"] = date_str

        # 尝试提交
        if safe_git(["git", "add", filename], env):
            if safe_git(["git", "commit", "-m", f"Fake commit {date_str}"], env):
                safe_git(["git", "rm", "--cached", filename], env)

        # 删除临时文件
        if file_path.exists():
            file_path.unlink()

    current += timedelta(days=1)

print("虚拟提交生成完成！")
