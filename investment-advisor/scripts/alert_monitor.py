"""
Investment Advisor - 预警监控模块
检测价格异动，触发深度分析
"""

import os
import sys
import json
from datetime import datetime
from typing import Optional

import yaml

# 添加项目路径
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, PROJECT_ROOT)

from scripts.market_fetcher import get_price, _get_ticker_name
from scripts.news_searcher import search_market_news, search_master_views, format_master_views_for_prompt
from scripts.analyzer import analyze_asset
from scripts.report import generate_alert_report


# ── 配置路径 ──────────────────────────────────────────────
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")
ALERT_HISTORY_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "alert_history.json")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "reports")


def load_config() -> dict:
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {"watchlist": []}


def load_alert_history() -> dict:
    """加载预警历史"""
    if os.path.exists(ALERT_HISTORY_FILE):
        try:
            with open(ALERT_HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_alert_history(history: dict):
    """保存预警历史"""
    os.makedirs(os.path.dirname(ALERT_HISTORY_FILE), exist_ok=True)
    try:
        with open(ALERT_HISTORY_FILE, "w") as f:
            json.dump(history, f, ensure_ascii=False)
    except Exception as e:
        print(f"保存预警历史失败: {e}")


def should_alert(ticker: str, change_pct: float, threshold: float) -> bool:
    """
    判断是否应该触发预警

    Args:
        ticker: 标的代码
        change_pct: 涨跌幅（百分比）
        threshold: 阈值

    Returns:
        True 如果涨跌幅超过阈值
    """
    return abs(change_pct) >= threshold * 100


def is_recently_alerted(ticker: str, history: dict, max_alerts_per_day: int = 2) -> bool:
    """
    检查是否最近已经预警过（避免重复预警）

    Args:
        ticker: 标的代码
        history: 预警历史
        max_alerts_per_day: 每天最多预警次数

    Returns:
        True 如果今天已经预警过
    """
    today = datetime.now().date().isoformat()
    ticker_history = history.get(ticker, {})

    alert_dates = ticker_history.get("alert_dates", [])
    today_count = alert_dates.count(today)

    return today_count >= max_alerts_per_day


def record_alert(ticker: str, change_pct: float, history: dict):
    """
    记录预警

    Args:
        ticker: 标的代码
        change_pct: 涨跌幅
        history: 预警历史
    """
    today = datetime.now().date().isoformat()

    if ticker not in history:
        history[ticker] = {"alerts": []}

    history[ticker]["alerts"].append({
        "date": datetime.now().isoformat(),
        "change_pct": change_pct,
    })

    if "alert_dates" not in history[ticker]:
        history[ticker]["alert_dates"] = []

    history[ticker]["alert_dates"].append(today)

    # 只保留最近 30 天的记录
    history[ticker]["alerts"] = history[ticker]["alerts"][-30:]


def check_alerts() -> list[dict]:
    """
    检查所有监控标的的预警状态

    Returns:
        触发预警的标的列表
    """
    config = load_config()
    watchlist = config.get("watchlist", [])
    history = load_alert_history()

    alerts = []

    for item in watchlist:
        ticker = item.get("ticker")
        threshold = item.get("alert_threshold", 0.05)
        name = item.get("name", _get_ticker_name(ticker))

        if not ticker:
            continue

        print(f"检查 {name}（{ticker}）...")

        # 获取价格
        price_data = get_price(ticker)

        if price_data.get("error"):
            print(f"  获取价格失败: {price_data['error']}")
            continue

        change_pct = price_data.get("change_pct", 0)

        # 检查是否触发预警
        if should_alert(ticker, change_pct, threshold):
            if is_recently_alerted(ticker, history):
                print(f"  今日已预警过，跳过")
                continue

            print(f"  ⚠️ 触发预警！涨跌幅 {change_pct:+.2f}%")

            # 记录预警
            record_alert(ticker, change_pct, history)

            alerts.append({
                "ticker": ticker,
                "name": name,
                "price_data": price_data,
                "change_pct": change_pct,
                "threshold": threshold,
            })
        else:
            print(f"  正常，涨跌幅 {change_pct:+.2f}%")

    # 保存预警历史
    save_alert_history(history)

    return alerts


def trigger_analysis(alert: dict) -> str:
    """
    触发深度分析

    Args:
        alert: 预警信息

    Returns:
        分析报告
    """
    ticker = alert["ticker"]
    name = alert["name"]
    price_data = alert["price_data"]
    change_pct = alert["change_pct"]

    print(f"\n为 {name} 生成深度分析...")

    # 获取新闻
    news = search_market_news(name, count=5)
    print(f"  获取到 {len(news)} 条新闻")

    # 获取大师观点
    master_views_raw = search_master_views(name, "大宗商品")
    master_views = format_master_views_for_prompt(master_views_raw)
    print(f"  获取大师观点")

    # 生成分析
    analysis = analyze_asset(
        ticker=ticker,
        asset_name=name,
        price_data=price_data,
        macro_data={},
        news=news,
        master_views=master_views,
        user_query=f"触发预警：单日涨跌幅 {change_pct:+.2f}%，请分析原因和后续走势",
    )

    # 生成报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(REPORTS_DIR, f"alert_{ticker}_{timestamp}.md")
    report = generate_alert_report(
        ticker=ticker,
        price_data=price_data,
        analysis=analysis,
        output_path=report_path,
    )

    return report


def main():
    """主入口"""
    print("=" * 60)
    print(f"Investment Advisor - 预警监控")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 检查预警
    alerts = check_alerts()

    if not alerts:
        print("\n无触发预警的标的")
        return

    print(f"\n共触发 {len(alerts)} 个预警：")
    for alert in alerts:
        emoji = "📈" if alert["change_pct"] > 0 else "📉"
        print(f"  {emoji} {alert['name']}：{alert['change_pct']:+.2f}%")

    # 逐一生成深度分析
    for alert in alerts:
        print("\n" + "-" * 40)
        report = trigger_analysis(alert)
        print("\n" + report)


if __name__ == "__main__":
    main()
