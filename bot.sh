#!/bin/bash

# 设置项目路径
PROJECT_PATH="./"  # 替换为你的本地 Git 仓库路径
cd "$PROJECT_PATH" || { echo "目录不存在"; exit 1; }

# 运行 Git 命令的函数
run_git_command() {
    output=$(git "$@" 2>&1)
    status=$?
    if [ $status -ne 0 ]; then
        echo "Git 命令失败: $output"
    fi
    echo "$output"
}

# 删除旧的 .txt 文件
delete_old_txt_files() {
    for file in *.txt; do
        [ -e "$file" ] || continue
        rm "$file"
        echo "已删除：$file"
    done
}

# 创建包含当前时间的文件
create_file_with_time() {
    today=$(date '+%Y-%m-%d')
    filename="$today.txt"
    current_time=$(date '+%H:%M:%S')
    echo "$current_time" >> "$filename"
    echo "$filename"
}

# 将文件提交到 Git
commit_to_git() {
    run_git_command add .
    run_git_command commit -m "Add time to file"
    run_git_command push origin main
}

# 自动提交函数
auto_commit() {
    echo "开始自动提交: $(date '+%Y-%m-%d')"

    delete_old_txt_files

    total_commits=$(( RANDOM % 17 + 4 ))  # 随机 4~20 次
    for ((i=1;i<=total_commits;i++)); do
        create_file_with_time
        commit_to_git
        echo "提交次数：$i/$total_commits"
        sleep 10  # 每次间隔 10 秒，可改成 60
    done
}

# 主程序
auto_commit
