#!/bin/bash
# 每日日报执行脚本，crontab 调用此文件
# 用法：
#   bash run.sh                  # 正常运行
#   bash run.sh --init           # 首次使用时初始化索引（只需运行一次）
#   bash run.sh --limit 5        # 限制处理数量

# 加载用户环境变量
source ~/.zshrc 2>/dev/null || source ~/.bash_profile 2>/dev/null

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d).log"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') 开始运行 ===" >> "$LOG_FILE"
python3 "$SCRIPT_DIR/main.py" "$@" >> "$LOG_FILE" 2>&1
echo "=== $(date '+%Y-%m-%d %H:%M:%S') 运行完成 ===" >> "$LOG_FILE"
