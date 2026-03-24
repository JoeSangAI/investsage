"""
Investment Advisor - 市场数据获取模块
使用 yfinance 获取价格数据，FRED API 获取宏观经济数据
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Optional

import requests
import yfinance as yf

# ── FRED API 配置 ──────────────────────────────────────────
FRED_API_KEY = os.getenv("FRED_API_KEY", "")
FRED_BASE_URL = "https://api.stlouisfed.org/fred"

# ── 价格缓存 ──────────────────────────────────────────────
CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "price_cache.json")


def _load_cache() -> dict:
    """加载价格缓存"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_cache(cache: dict):
    """保存价格缓存"""
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f, ensure_ascii=False)
    except Exception:
        pass


def _is_cache_valid(cache: dict, ticker: str, max_age_minutes: int = 15) -> bool:
    """检查缓存是否有效"""
    if ticker not in cache:
        return False
    timestamp = cache[ticker].get("timestamp", "")
    try:
        cached_time = datetime.fromisoformat(timestamp)
        age = (datetime.now() - cached_time).total_seconds() / 60
        return age < max_age_minutes
    except Exception:
        return False


def get_price(ticker: str, use_cache: bool = True) -> dict:
    """
    获取单个标的的最新价格和相关信息

    Returns:
        {
            "ticker": "GC=F",
            "name": "黄金",
            "price": 2985.5,
            "change": -70.3,
            "change_pct": -2.3,
            "high": 3050.0,
            "low": 2950.0,
            "volume": 123456,
            "ma20": 2940.0,
            "timestamp": "2026-03-23T09:30:00"
        }
    """
    cache = _load_cache() if use_cache else {}

    # 检查缓存
    if use_cache and _is_cache_valid(cache, ticker):
        return cache[ticker]

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # 获取历史数据计算均线
        hist = stock.history(period="1mo")
        ma20 = float(hist["Close"].rolling(20).mean().iloc[-1]) if len(hist) >= 20 else None

        # 计算单日涨跌幅
        prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose")
        current_price = info.get("regularMarketPrice") or info.get("currentPrice")

        if prev_close and current_price:
            change = current_price - prev_close
            change_pct = (change / prev_close) * 100
        else:
            change = 0
            change_pct = 0

        result = {
            "ticker": ticker,
            "name": _get_ticker_name(ticker),
            "price": current_price,
            "change": change,
            "change_pct": round(change_pct, 2),
            "high": info.get("dayHigh"),
            "low": info.get("dayLow"),
            "volume": info.get("regularMarketVolume"),
            "prev_close": prev_close,
            "ma20": round(ma20, 2) if ma20 else None,
            "timestamp": datetime.now().isoformat(),
        }

        # 更新缓存
        if use_cache:
            cache[ticker] = result
            _save_cache(cache)

        return result

    except Exception as e:
        # 如果有缓存且请求失败，返回缓存
        if ticker in cache:
            return cache[ticker]
        return {
            "ticker": ticker,
            "name": _get_ticker_name(ticker),
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def get_prices(tickers: list[str]) -> dict[str, dict]:
    """批量获取多个标的的价格"""
    results = {}
    for ticker in tickers:
        results[ticker] = get_price(ticker)
        time.sleep(0.1)  # 避免请求过快
    return results


def _get_ticker_name(ticker: str) -> str:
    """获取标的名称"""
    names = {
        "GC=F": "黄金",
        "CL=F": "原油",
        "^GSPC": "标普500",
        "^IXIC": "纳斯达克",
        "000300.SS": "沪深300",
        "600519.SS": "茅台",
        "AAPL": "苹果",
        "MSFT": "微软",
        "GOOGL": "谷歌",
        "AMZN": "亚马逊",
        "TSLA": "特斯拉",
        "NVDA": "英伟达",
    }
    return names.get(ticker, ticker)


def get_macro_indicators() -> dict:
    """
    获取宏观经济指标（从 FRED API）

    Returns:
        {
            "FEDFUNDS": {"name": "联邦基金利率", "value": 5.25, "date": "2026-03-01"},
            "T10YIE": {"name": "10年期通胀预期", "value": 2.35, "date": "2026-03-20"},
            ...
        }
    """
    if not FRED_API_KEY:
        return _get_fallback_macro()

    indicators = {
        "FEDFUNDS": "联邦基金利率",
        "T10YIE": "10年期通胀预期",
        "GDPC1": "实际GDP",
        "DXY": "美元指数",
    }

    results = {}
    for code, name in indicators.items():
        try:
            url = f"{FRED_BASE_URL}/series/observations"
            params = {
                "series_id": code,
                "api_key": FRED_API_KEY,
                "file_type": "json",
                "limit": 1,
                "sort_order": "desc",
            }
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            observations = data.get("observations", [])
            if observations:
                obs = observations[0]
                results[code] = {
                    "name": name,
                    "value": float(obs["value"]) if obs["value"] != "." else None,
                    "date": obs["date"],
                }
            time.sleep(0.1)
        except Exception as e:
            results[code] = {"name": name, "error": str(e)}

    return results


def _get_fallback_macro() -> dict:
    """FRED API 不可用时的备用数据"""
    return {
        "FEDFUNDS": {"name": "联邦基金利率", "value": 5.25, "date": "2026-03-01", "note": "参考值"},
        "T10YIE": {"name": "10年期通胀预期", "value": 2.35, "date": "2026-03-20", "note": "参考值"},
        "GDPC1": {"name": "实际GDP", "value": 2.1, "date": "2026-03-01", "note": "参考值"},
        "DXY": {"name": "美元指数", "value": 104.5, "date": "2026-03-23", "note": "参考值"},
    }


def get_asset_basic_info(ticker: str) -> dict:
    """获取资产基本信息（用于基本面分析）"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            "ticker": ticker,
            "name": info.get("shortName") or info.get("longName", _get_ticker_name(ticker)),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "dividend_yield": info.get("dividendYield"),
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
            "avg_volume": info.get("averageVolume"),
            "beta": info.get("beta"),
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


if __name__ == "__main__":
    # 测试
    print("=== 测试价格获取 ===")
    gold = get_price("GC=F")
    print(f"黄金: ${gold.get('price', 'N/A')} ({gold.get('change_pct', 0):+.2f}%)")

    print("\n=== 测试宏观经济 ===")
    macro = get_macro_indicators()
    for code, data in macro.items():
        print(f"{data['name']}: {data.get('value', 'N/A')}")
