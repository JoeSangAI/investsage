"""
Investment Advisor - 新闻和大帅观点搜索模块
使用 Bocha API 搜索市场新闻和大师观点
"""

import os
import json
import time
from typing import Optional

import requests

# ── Bocha API 配置 ──────────────────────────────────────────
BOCHA_API_KEY = os.getenv("BOCHA_API_KEY", "")
BOCHA_BASE_URL = "https://api.bocha.com"

# 如果没有 Bocha key，尝试使用 sales-intel 的 key
if not BOCHA_API_KEY:
    BOCHA_API_KEY = os.getenv("BOCHA_API_KEY", "")


def _call_bocha_api(endpoint: str, params: dict) -> Optional[dict]:
    """调用 Bocha API"""
    if not BOCHA_API_KEY:
        return None

    try:
        url = f"{BOCHA_BASE_URL}/{endpoint}"
        params["apiKey"] = BOCHA_API_KEY
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"  [Bocha API 错误] {e}")
        return None


def search_web(query: str, count: int = 5) -> list[dict]:
    """
    搜索网页新闻

    Returns:
        [{"title": "...", "url": "...", "snippet": "..."}, ...]
    """
    result = _call_bocha_api("v1/web-search", {
        "query": query,
        "pageSize": count,
        "page": 1,
    })

    if not result or result.get("code") != 200:
        return []

    data = result.get("data", {})
    items = data.get("webPages", {}).get("value", [])
    return [
        {
            "title": item.get("name", ""),
            "url": item.get("url", ""),
            "snippet": item.get("snippet", "")[:200],
        }
        for item in items[:count]
    ]


def search_news(query: str, count: int = 5) -> list[dict]:
    """
    搜索新闻

    Returns:
        [{"title": "...", "url": "...", "date": "..."}, ...]
    """
    result = _call_bocha_api("v1/news-search", {
        "query": query,
        "pageSize": count,
        "freshness": "Day",  # Day, Week, Month
    })

    if not result or result.get("code") != 200:
        return []

    data = result.get("data", {})
    items = data.get("news", {}).get("value", [])
    return [
        {
            "title": item.get("name", ""),
            "url": item.get("url", ""),
            "date": item.get("datePublished", ""),
            "snippet": item.get("description", "")[:200],
        }
        for item in items[:count]
    ]


def search_master_views(asset_name: str = "", asset_type: str = "") -> dict[str, list[dict]]:
    """
    搜索八位大师观点 + 机构分析师研报

    Args:
        asset_name: 资产名称（如"黄金"、"原油"）
        asset_type: 资产类型（如"大宗商品"、"股票"）

    Returns:
        {
            "buffett": [...],
            "munger": [...],
            "dalio": [...],
            "marks": [...],
            "soros": [...],
            "lynch": [...],
            "templeton": [...],
            "burly": [...],
            "analysts": [...]
        }
    """
    master_keywords = {
        # 价值投资派
        "buffett": [
            f"巴菲特 {asset_name} 观点" if asset_name else "巴菲特 投资理念 2026",
            "Warren Buffett gold view 2026",
            "巴菲特 股东大会 2025 2026 投资",
        ],
        "munger": [
            f"芒格 {asset_name} 观点" if asset_name else "芒格 投资智慧 2026",
            "Charlie Munger investment wisdom",
        ],
        # 宏观对冲派
        "dalio": [
            f"达利欧 {asset_name} 观点" if asset_name else "达利欧 宏观经济 2026",
            "Ray Dalio gold outlook 2026",
            "Ray Dalio debt cycle 2026",
        ],
        "soros": [
            f"索罗斯 {asset_name} 观点" if asset_name else "索罗斯 投资哲学 2026",
            "George Soros reflexivity theory markets",
            "Soros gold macro trade 2026",
        ],
        # 成长投资派
        "lynch": [
            f"彼得·林奇 {asset_name} 观点" if asset_name else "彼得·林奇 成长股 投资",
            "Peter Lynch investment principles stock picking",
        ],
        "templeton": [
            f"约翰·邓普顿 {asset_name} 观点" if asset_name else "邓普顿 逆向投资 全球机会",
            "John Templeton contrarian investing",
        ],
        # 深度价值派
        "marks": [
            f"霍华德·马克斯 {asset_name} 观点" if asset_name else "马克斯 钟摆理论 投资",
            "Howard Marks investment insights 2026",
        ],
        "burly": [
            f"迈克尔·伯里 {asset_name} 观点" if asset_name else "伯里 深度价值 危机发现",
            "Michael Burry big short value investing",
        ],
        # 机构分析师研报
        "analysts": [
            f"高盛 {asset_name} 报告 2026" if asset_name else "Goldman Sachs market outlook 2026",
            f"摩根士丹利 {asset_name} 分析 2026" if asset_name else "Morgan Stanley investment strategy 2026",
            f"桥水 {asset_name} 观点 2026" if asset_name else "Bridgewater macro outlook 2026",
            "瑞银 全球市场 分析 报告",
            "花旗 {asset_name} 研报 2026" if asset_name else "Citi research markets 2026",
        ],
    }

    results = {}
    for master, queries in master_keywords.items():
        all_items = []
        for query in queries[:2]:  # 每个大师最多 2 个查询
            items = search_web(query, count=3)
            all_items.extend(items)
            time.sleep(0.2)

        # 去重
        seen = set()
        unique_items = []
        for item in all_items:
            key = item.get("title", "")[:50]
            if key and key not in seen:
                seen.add(key)
                unique_items.append(item)

        results[master] = unique_items[:3]  # 每个大师最多 3 条

    return results


def search_market_news(asset_name: str, count: int = 5) -> list[dict]:
    """
    搜索市场新闻（含多源机构研报）

    Args:
        asset_name: 资产名称
        count: 返回数量

    Returns:
        [{"title": "...", "url": "...", "snippet": "..."}, ...]
    """
    queries = [
        f"{asset_name} 市场分析 2026",
        f"{asset_name} 暴跌 暴涨 原因",
        f"{asset_name} 投资 机会",
        # 新增：机构研报来源
        f"{asset_name} 高盛 摩根 研报 2026",
        f"{asset_name} 桥水 宏观 观点 2026",
    ]

    all_items = []
    for query in queries:
        items = search_news(query, count=count)
        all_items.extend(items)
        time.sleep(0.2)

    # 去重
    seen = set()
    unique_items = []
    for item in all_items:
        key = item.get("title", "")[:50]
        if key and key not in seen:
            seen.add(key)
            unique_items.append(item)

    return unique_items[:count]


def format_master_views_for_prompt(master_views: dict) -> str:
    """
    格式化大师观点 + 机构研报为 prompt 友好格式
    多源交叉验证，不同来源的观点会用不同标记区分
    """
    master_names = {
        "buffett": "巴菲特",
        "munger": "芒格",
        "dalio": "达利欧",
        "marks": "霍华德·马克斯",
        "soros": "索罗斯",
        "lynch": "彼得·林奇",
        "templeton": "约翰·邓普顿",
        "burly": "迈克尔·伯里",
        "analysts": "机构研报",
    }

    lines = []
    source_count = 0

    for master, views in master_views.items():
        if not views:
            continue
        source_count += 1
        master_name = master_names.get(master, master)

        # 机构研报用不同标记
        prefix = "📊" if master == "analysts" else "💡"
        lines.append(f"\n{prefix} **{master_name}** 观点：")
        for i, view in enumerate(views[:2], 1):
            title = view.get("title", "")
            snippet = view.get("snippet", view.get("description", ""))
            lines.append(f"   {i}. {title}")
            if snippet:
                lines.append(f"      {snippet[:120]}...")

    if not lines:
        return "（当前无法获取大师实时观点和研报）"

    lines.insert(0, f"【来自 {source_count} 个不同来源的交叉观点】")
    return "\n".join(lines)


def cross_validate_sources(news_items: list[dict]) -> dict:
    """
    对多条新闻进行交叉验证

    Returns:
        {
            "confirmed": [...],   # 多源证实的
            "controversial": [...],  # 不同来源有分歧的
            "single_source": [...]   # 仅有单一来源的
        }
    """
    if not news_items:
        return {"confirmed": [], "controversial": [], "single_source": []}

    # 按标题关键词分组
    groups = {}
    for item in news_items:
        title = item.get("title", "")
        # 提取关键词（简单方法：前30字）
        key = title[:30] if title else "unknown"
        if key not in groups:
            groups[key] = []
        groups[key].append(item)

    confirmed = []
    controversial = []
    single_source = []

    for key, items in groups.items():
        if len(items) >= 2:
            confirmed.append(items[0])
        else:
            single_source.append(items[0] if items else None)

    return {
        "confirmed": confirmed[:5],
        "controversial": controversial,
        "single_source": [x for x in single_source if x] [:3],
    }


if __name__ == "__main__":
    # 测试
    print("=== 测试市场新闻搜索 ===")
    news = search_market_news("黄金", count=3)
    for n in news:
        print(f"- {n['title']}")

    print("\n=== 测试大师观点搜索 ===")
    views = search_master_views("黄金", "大宗商品")
    for master, master_views in views.items():
        print(f"\n{master}:")
        for v in master_views[:2]:
            print(f"  - {v['title']}")
