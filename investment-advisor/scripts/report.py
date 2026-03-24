"""
Investment Advisor - 报告生成模块
"""

import os
from datetime import datetime
from typing import Optional

from .market_fetcher import get_price, _get_ticker_name


def generate_report(
    ticker: str,
    asset_name: str,
    price_data: dict,
    macro_data: dict,
    news: list,
    master_views: str,
    analysis: str,
    user_query: str = "",
    output_path: Optional[str] = None,
) -> str:
    """
    生成完整的投资分析报告

    Returns:
        Markdown 格式的报告字符串
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 价格信号表格
    price_table = _build_price_table(price_data)

    # 宏观指标
    macro_section = _build_macro_section(macro_data)

    # 新闻摘要
    news_section = _build_news_section(news)

    report = f"""# 📊 投资分析报告

**标的**：{asset_name}（{ticker}）
**生成时间**：{now}

---

## 📉 价格信号

{price_table}

## 🌍 宏观逻辑

{macro_section}

## 📰 市场新闻

{news_section}

## 🧭 大师框架分析

### 巴菲特视角
（护城河、别人恐惧时贪婪、合理价格）

### 芒格视角
（逆向思考、多元思维）

### 达利欧视角
（宏观周期、风险平价）

### 马克斯视角
（钟摆理论、第二层思维）

## 🔍 大师实时观点

{master_views}

---

## 💡 AI 分析

{analysis}

---

_报告由 Investment Advisor 生成_
"""

    # 保存到文件
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"报告已保存: {output_path}")

    return report


def _build_price_table(price_data: dict) -> str:
    """构建价格信号表格"""
    if not price_data or price_data.get("error"):
        return "（价格数据不可用）"

    rows = []

    # 当前价格
    price = price_data.get("price")
    if price:
        rows.append(f"| 当前价格 | {price} | — |")

    # 涨跌幅
    change = price_data.get("change", 0)
    change_pct = price_data.get("change_pct", 0)
    signal = _get_signal_emoji(change_pct)
    rows.append(f"| 单日涨跌 | {change:+.2f}（{change_pct:+.2f}%） | {signal} |")

    # 均线
    ma20 = price_data.get("ma20")
    if ma20 and price:
        diff = (price - ma20) / ma20 * 100
        ma_signal = "📈 高于" if diff > 0 else "📉 低于"
        rows.append(f"| 20日均线 | {ma20} | {ma_signal}（{diff:+.2f}%） |")

    # 高低点
    high = price_data.get("high")
    low = price_data.get("low")
    if high and low:
        rows.append(f"| 今日区间 | {low} - {high} | — |")

    return "| 指标 | 数值 | 信号 |\n|------|------|------|\n" + "\n".join(rows)


def _get_signal_emoji(change_pct: float) -> str:
    """根据涨跌幅返回信号 emoji"""
    if change_pct > 3:
        return "🔥 暴涨"
    elif change_pct > 1:
        return "📈 上涨"
    elif change_pct > 0:
        return "↗️ 小涨"
    elif change_pct == 0:
        return "➡️ 持平"
    elif change_pct > -1:
        return "↘️ 小跌"
    elif change_pct > -3:
        return "📉 下跌"
    else:
        return "💥 暴跌"


def _build_macro_section(macro_data: dict) -> str:
    """构建宏观逻辑部分"""
    if not macro_data:
        return "（宏观数据不可用）"

    lines = []
    indicator_names = {
        "FEDFUNDS": "联邦基金利率",
        "T10YIE": "10年期通胀预期",
        "GDPC1": "实际GDP",
        "DXY": "美元指数",
    }

    for code, data in macro_data.items():
        if isinstance(data, dict):
            name = data.get("name", indicator_names.get(code, code))
            value = data.get("value")
            if value is not None:
                lines.append(f"- **{name}**：{value}")

    return "\n".join(lines) if lines else "（宏观数据不可用）"


def _build_news_section(news: list) -> str:
    """构建新闻部分"""
    if not news:
        return "（暂无相关新闻）"

    lines = []
    for i, item in enumerate(news[:5], 1):
        title = item.get("title", "无标题")
        snippet = item.get("snippet", "")
        if len(snippet) > 150:
            snippet = snippet[:150] + "..."
        lines.append(f"**{i}. {title}**")
        if snippet:
            lines.append(f"   {snippet}")
        lines.append("")

    return "\n".join(lines).strip()


def generate_alert_report(
    ticker: str,
    price_data: dict,
    analysis: str,
    output_path: Optional[str] = None,
) -> str:
    """生成预警报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    asset_name = price_data.get("name", _get_ticker_name(ticker))
    change_pct = price_data.get("change_pct", 0)

    emoji = "📈" if change_pct > 0 else "📉"
    direction = "暴涨" if abs(change_pct) > 5 else ("大涨" if change_pct > 0 else "大跌") if abs(change_pct) > 3 else ("上涨" if change_pct > 0 else "下跌")

    report = f"""# ⚠️ 投资预警

**标的**：{asset_name}（{ticker}）
**时间**：{now}
**异动**：{emoji} {direction} {change_pct:+.2f}%

---

## 📉 价格详情

- 当前价格：{price_data.get('price', 'N/A')}
- 单日涨跌：{price_data.get('change', 0):+.2f}（{change_pct:+.2f}%）
- 20日均线：{price_data.get('ma20', 'N/A')}

---

## 💡 深度分析

{analysis}

---

_此为自动预警报告_
"""

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)

    return report
