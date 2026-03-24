#!/usr/bin/env python3
"""
Investment Advisor - 主入口
按需查询模式：获取数据 → 搜索新闻 → AI 分析 → 输出报告
"""

import os
import sys
import argparse
from datetime import datetime

import yaml

# 添加项目路径
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, PROJECT_ROOT)

from scripts.market_fetcher import get_price, get_prices, get_macro_indicators, _get_ticker_name
from scripts.news_searcher import search_market_news, search_master_views, format_master_views_for_prompt
from scripts.analyzer import analyze_asset, quick_analysis
from scripts.report import generate_report


# ── 配置路径 ──────────────────────────────────────────────
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "reports")


def load_config() -> dict:
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {"watchlist": []}


def parse_ticker_input(ticker_str: str) -> str:
    """
    解析用户输入的标的代码

    支持格式：
    - 黄金 -> GC=F
    - 原油 -> CL=F
    - 茅台 -> 600519.SS
    - AAPL -> AAPL
    """
    mapping = {
        "黄金": "GC=F",
        "原油": "CL=F",
        "石油": "CL=F",
        "美股": "^GSPC",
        "标普": "^GSPC",
        "标普500": "^GSPC",
        "纳斯达克": "^IXIC",
        "沪深300": "000300.SS",
        "沪深": "000300.SS",
        "茅台": "600519.SS",
        "苹果": "AAPL",
        "微软": "MSFT",
        "谷歌": "GOOGL",
        "亚马逊": "AMZN",
        "特斯拉": "TSLA",
        "英伟达": "NVDA",
    }

    # 检查是否直接是代码
    if "^" in ticker_str or ".SS" in ticker_str or ticker_str in ["GC=F", "CL=F", "AAPL", "MSFT"]:
        return ticker_str

    return mapping.get(ticker_str, ticker_str)


def run_analysis(
    tickers: list[str],
    user_query: str,
    output_file: str = None,
) -> str:
    """
    运行分析

    Args:
        tickers: 标的代码列表
        user_query: 用户的问题
        output_file: 输出文件路径

    Returns:
        分析报告
    """
    print("=" * 60)
    print("Investment Advisor - 投资分析")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 获取价格数据
    print("\n[1/4] 获取价格数据...")
    prices = get_prices(tickers)
    for ticker, data in prices.items():
        if data.get("error"):
            print(f"  {ticker}: 获取失败 - {data['error']}")
        else:
            print(f"  {data.get('name', ticker)}: ${data.get('price', 'N/A')} ({data.get('change_pct', 0):+.2f}%)")

    # 获取宏观经济数据
    print("\n[2/4] 获取宏观数据...")
    macro = get_macro_indicators()
    for code, data in macro.items():
        if data.get("error"):
            print(f"  {data['name']}: 获取失败")
        else:
            print(f"  {data['name']}: {data.get('value', 'N/A')}")

    # 获取新闻和大师观点
    print("\n[3/4] 搜索新闻和大师观点...")

    # 使用第一个标的主导分析
    primary_ticker = tickers[0]
    primary_price = prices.get(primary_ticker, {})
    primary_name = primary_price.get("name", _get_ticker_name(primary_ticker))

    # 判断资产类型
    asset_type = "大宗商品" if primary_ticker in ["GC=F", "CL=F"] else "股票"

    news = search_market_news(primary_name, count=5)
    print(f"  获取到 {len(news)} 条新闻")

    master_views_raw = search_master_views(primary_name, asset_type)
    master_views = format_master_views_for_prompt(master_views_raw)
    print(f"  获取大师观点")

    # 运行分析
    print("\n[4/4] 运行 AI 分析...")
    analysis = analyze_asset(
        ticker=primary_ticker,
        asset_name=primary_name,
        price_data=primary_price,
        macro_data=macro,
        news=news,
        master_views=master_views,
        user_query=user_query,
    )

    # 生成报告
    if output_file:
        report = generate_report(
            ticker=primary_ticker,
            asset_name=primary_name,
            price_data=primary_price,
            macro_data=macro,
            news=news,
            master_views=master_views,
            analysis=analysis,
            user_query=user_query,
            output_path=output_file,
        )
    else:
        # 直接输出
        report = generate_report(
            ticker=primary_ticker,
            asset_name=primary_name,
            price_data=primary_price,
            macro_data=macro,
            news=news,
            master_views=master_views,
            analysis=analysis,
            user_query=user_query,
        )

    return report


def interactive_mode():
    """交互式查询模式"""
    print("\n" + "=" * 60)
    print("Investment Advisor - 交互式分析")
    print("=" * 60)
    print("\n支持的分析标的：")
    print("  - 黄金、原油")
    print("  - 标普500、纳斯达克、沪深300")
    print("  - 茅台、苹果、微软、特斯拉等个股")
    print("\n输入 '退出' 结束")
    print("-" * 60)

    while True:
        print("\n")
        ticker_input = input("请输入要分析的标的（黄金/原油/茅台/AAPL）: ").strip()

        if ticker_input in ["退出", "exit", "q"]:
            print("再见！")
            break

        if not ticker_input:
            continue

        ticker = parse_ticker_input(ticker_input)
        print(f"标的代码: {ticker}")

        query = input("你想了解什么？（直接回车使用默认问题）: ").strip()
        if not query:
            query = f"当前 {ticker_input} 的投资价值如何？"

        print("\n")
        report = run_analysis([ticker], query)
        print("\n" + report)


def main():
    parser = argparse.ArgumentParser(description="Investment Advisor - 投资分析助手")
    parser.add_argument("--ticker", type=str, help="标的代码（如 GC=F、AAPL、600519.SS）")
    parser.add_argument("--tickers", type=str, help="多个标的，用逗号分隔")
    parser.add_argument("--query", type=str, help="你想了解的问题")
    parser.add_argument("--interactive", action="store_true", help="交互式模式")
    parser.add_argument("--output", type=str, help="输出文件路径")
    parser.add_argument("--config", type=str, help="配置文件路径")

    args = parser.parse_args()

    # 交互式模式
    if args.interactive:
        interactive_mode()
        return

    # 解析标的
    if args.tickers:
        tickers = [parse_ticker_input(t.strip()) for t in args.tickers.split(",")]
    elif args.ticker:
        tickers = [parse_ticker_input(args.ticker)]
    else:
        # 默认分析黄金
        tickers = ["GC=F"]

    # 用户问题
    query = args.query or "这笔投资当前怎么看？有什么机会和风险？"

    # 运行分析
    report = run_analysis(tickers, query, args.output)

    # 输出
    print("\n" + "=" * 60)
    print("分析结果:")
    print("=" * 60)
    print(report)


if __name__ == "__main__":
    main()
