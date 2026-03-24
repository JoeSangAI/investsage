# Investment Advisor - 初始化指南

## 快速开始

### 1. 环境要求

```bash
# 确保安装了必要的 Python 包
pip install yfinance requests pyyaml
```

### 2. API Key 配置

系统使用以下 API（免费）：

**MINIMAX_API_KEY**（必须）
- 用于 AI 分析
- 从 MiniMax 平台获取

**BOCHA_API_KEY**（可选）
- 用于搜索市场新闻和大师观点
- 从 Bocha API 平台获取
- 如果不配置，将使用有限的 fallback 数据

**FRED_API_KEY**（可选）
- 用于获取宏观经济数据
- 从美联储获取：https://fred.stlouisfed.org/docs/api/api_key.html

### 3. 环境变量配置

```bash
# 在 ~/.bash_profile 或 ~/.zshrc 中添加
export MINIMAX_API_KEY="your_minimax_key"
export BOCHA_API_KEY="your_bocha_key"  # 可选
export FRED_API_KEY="your_fred_key"     # 可选
```

### 4. 运行测试

```bash
cd ~/.claude/skills/investment-advisor

# 测试价格获取
python scripts/market_fetcher.py

# 测试搜索
python scripts/news_searcher.py

# 运行完整分析
python scripts/main.py --ticker GC=F --query "黄金为什么暴跌"
```

## 配置监控标的

编辑 `scripts/config.yaml` 添加或修改监控标的：

```yaml
watchlist:
  - name: 黄金
    ticker: GC=F
    alert_threshold: 0.03  # ±3%
    weight: 0.4

  - name: 原油
    ticker: CL=F
    alert_threshold: 0.05
    weight: 0.2
```

## 设置定时任务

### macOS launchd

创建 `~/Library/LaunchAgents/com.investment-advisor.alert.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "...">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.investment-advisor.alert</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/YOUR_USER/.claude/skills/investment-advisor/scripts/alert_monitor.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>
</dict>
</plist>
```

### Cron

```bash
# 每天 8:30 运行预警检查
30 8 * * * cd ~/.claude/skills/investment-advisor && python scripts/alert_monitor.py >> data/logs/alert.log 2>&1
```

## 常见问题

### Q: 报错 "MiniMax API 不可用"
A: 确保设置了 `MINIMAX_API_KEY` 环境变量

### Q: 搜索返回空结果
A: 检查 `BOCHA_API_KEY` 是否设置，或网络是否正常

### Q: 黄金/原油价格获取失败
A: Yahoo Finance 在某些地区可能受限，尝试使用代理或 VPN
