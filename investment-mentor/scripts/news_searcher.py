"""
Investment Mentor - 新闻和大帅观点搜索模块
使用 Bocha API 搜索市场热点和大师观点
"""

import os
import time
from typing import Optional

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ── Bocha API 配置 ──────────────────────────────────────────
BOCHA_API_KEY = os.getenv("BOCHA_API_KEY", "")


def _call_bocha_api(endpoint: str, params: dict) -> Optional[dict]:
    """调用 Bocha API"""
    if not BOCHA_API_KEY or not HAS_REQUESTS:
        return None

    try:
        url = f"https://api.bocha.com/{endpoint}"
        params["apiKey"] = BOCHA_API_KEY
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def search_news(query: str, count: int = 5) -> list[dict]:
    """搜索新闻"""
    result = _call_bocha_api("v1/news-search", {
        "query": query,
        "pageSize": count,
        "freshness": "Day",
    })

    if not result or result.get("code") != 200:
        return []

    data = result.get("data", {})
    items = data.get("news", {}).get("value", [])
    return [
        {
            "title": item.get("name", ""),
            "snippet": item.get("description", "")[:200],
            "date": item.get("datePublished", ""),
        }
        for item in items[:count]
    ]


def search_hot_topic(topic: str, count: int = 3) -> list[dict]:
    """搜索某个主题的最新热点"""
    queries = [
        f"{topic} 最新消息",
        f"{topic} 市场动态 2026",
    ]
    all_items = []
    for q in queries:
        items = search_news(q, count=count)
        all_items.extend(items)
        time.sleep(0.1)

    # 去重
    seen = set()
    unique = []
    for item in all_items:
        key = item.get("title", "")[:30]
        if key and key not in seen:
            seen.add(key)
            unique.append(item)
    return unique[:count]


def get_market_hot_topics() -> dict:
    """
    获取当前市场热点话题
    用于课程结合热点
    """
    topics_to_check = [
        ("黄金", "贵金属"),
        ("原油", "大宗商品"),
        ("美联储", "宏观经济"),
        ("美元", "外汇"),
        ("美股", "股市"),
        ("A股", "股市"),
        ("比特币", "加密货币"),
    ]

    hot_topics = {}
    for topic, category in topics_to_check:
        news = search_hot_topic(topic, count=2)
        if news:
            hot_topics[topic] = {
                "name": topic,
                "category": category,
                "news": news,
            }
        time.sleep(0.1)

    return hot_topics


def pick_relevant_hot_topic(topic_id: str, hot_topics: dict) -> Optional[dict]:
    """根据课程主题匹配相关热点"""
    topic_keywords = {
        "GOLD": ["黄金", "贵金属"],
        "STOCK": ["股票", "美股", "A股"],
        "BOND": ["债券", "国债", "美债"],
        "INTEREST": ["美联储", "利率", "加息"],
        "INFLATION": ["通胀", "物价", "美联储"],
        "DOLLAR": ["美元", "外汇", "DXY"],
        "REAL-RATE": ["实际利率", "美债", "TIPS"],
        "CYCLE": ["周期", "经济", "衰退"],
        "RISK": ["风险", "波动", "股市"],
        "MOAT": ["股票", "公司", "护城河"],
        "VALUATION": ["估值", "股票", "DCF"],
    }

    keywords = topic_keywords.get(topic_id, [])
    for kw in keywords:
        if kw in hot_topics:
            return hot_topics[kw]
    return None


if __name__ == "__main__":
    print("=== 测试热点搜索 ===")
    topics = get_market_hot_topics()
    for name, data in topics.items():
        print(f"\n{name}:")
        for n in data.get("news", [])[:2]:
            print(f"  - {n['title']}")
