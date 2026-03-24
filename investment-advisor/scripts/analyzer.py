"""
Investment Advisor - AI 分析引擎
融合巴菲特、芒格、达利欧、霍华德·马克斯投资智慧
使用 MiniMax-Text-2.7 进行分析
"""

import os
import json
import time
from typing import Optional

import requests


# ── MiniMax API 配置 ──────────────────────────────────────
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
MINIMAX_BASE_URL = "https://api.minimax.chat/v1"


# ── 大师投资框架 Prompt ──────────────────────────────────
# 扩展大师框架：博采众长，不局限于单一风格

MASTER_FRAMEWORK = """你是一位融合多位投资大师智慧的顶级分析师。你的分析框架来自：

【巴菲特视角 - 价值投资】
- 这项资产有护城河吗？（黄金：避险属性；股票：竞争优势/护城河）
- 别人恐惧时贪婪：当前情绪是否过度悲观/乐观？市场是否过度反应？
- 合理价格：以合理价格买入，不是以便宜价格买入平庸资产
- 能力圈：这项投资在你的能力圈内吗？

【芒格视角 - 逆向思考】
- 逆向思考：什么会让这笔投资失败？最坏的情况是什么？
- 多元思维：从宏观、地缘、心理学、概率学多角度看问题
- 激励效应：谁在这笔交易中赚钱？他们的动机是什么？
- 确认偏见：我的分析是否只看到想看到的东西？

【达利欧视角 - 宏观对冲】
- 长期债务周期：我们处于债务周期的哪个阶段？（早期/泡沫/顶部/去杠杆/萧条）
- 风险平价：这项资产在组合中的作用是什么？与其他资产的相关性？
- 宏观对冲：这笔投资能否对冲宏观风险？

【霍华德·马克斯视角 - 市场情绪】
- 钟摆理论：市场情绪偏恐惧（过度悲观）还是贪婪（过度乐观）？
- 第二层思维：我的判断在市场共识之外吗？大众怎么想？
- 周期与时机：虽然无法精确预测时机，但要知道我们处于周期的哪个位置

【索罗斯视角 - 反身性理论】
- 市场偏见：价格不只是反映基本面，还会影响基本面（反身性）
- 宏观交易：在货币、债券、股票间寻找错误定价，敢于下重注
- 冒险原则：错了就认，快跑，不要坚持错误的头寸

【彼得·林奇视角 - 成长投资】
- 成长股逻辑：关注公司故事和增长潜力，但不买估值离谱的"故事"
- 身边调研：从自己的消费习惯中发现投资机会
- 十倍股思维：从细分市场找龙头，看长期增长

【约翰·邓普顿视角 - 逆向投资】
- 逆向投资：别人恐惧时贪婪，别人贪婪时恐惧
- 全球分散：不只看美国市场，新兴市场也有机会
- 估值纪律：买在无人问津时，而不是热门时刻

【迈克尔·伯里视角 - 深度价值】
- 深度价值：清算价值、重仓低估，不从众
- 另类数据：看穿表面财务，发现隐藏的风险
- 耐心等待：等待正确的时机，不急于入场
"""


# ── Fact-Checker Prompt ──────────────────────────────────
# 金融领域幻觉信息可能致命，必须验证

FACT_CHECK_PROMPT = """你是一个严格的事实核查员。在金融分析中，任何错误的事实都可能导致严重的投资损失。

请核查以下内容中的关键事实陈述，标记出：
1. ✅ 可能是正确的陈述（需要进一步验证）
2. ⚠️ 模糊的陈述（缺乏具体数据或时间）
3. ❌ 可能是错误的陈述（与已知事实不符）

【待核查内容】
{content}

【已知背景信息】
- 当前日期：2026年3月
- 近期市场：黄金暴跌、原油大涨、地缘冲突（美伊）

请逐一核查，特别关注：
- 历史事件的时间线是否正确
- 数据是否在合理范围内
- 逻辑推论是否有前提假设

对每个关键陈述给出核查结果。
"""


MARKET_ANALYSIS_PROMPT_TEMPLATE = """{master_framework}

===

你正在分析：{asset_name}（{ticker}）

【用户问题】
{user_query}

【当前价格数据】
{price_data}

【宏观经济背景】
{macro_data}

【市场新闻】
{news_data}

【大师实时观点】（来自最新搜索）
{master_views}

===

请给出以下分析，用中文回答：

## 1. 价格信号解读
（当前价格、涨跌幅、均线位置、技术信号）

## 2. 大师框架分析（博采众长）
### 巴菲特视角
（护城河、别人恐惧时贪婪、合理价格、能力圈）

### 芒格视角（逆向思考）
（什么会让这笔投资失败？多元思维）

### 达利欧视角
（宏观周期位置、风险平价）

### 马克斯视角（钟摆理论）
（市场情绪、第二层思维）

### 索罗斯视角（反身性）
（市场偏见如何影响基本面？宏观交易机会在哪里？）

### 林奇视角（成长投资）
（公司故事是否成立？增长潜力如何？）

### 邓普顿视角（逆向投资）
（当前是否无人问津？全球机会在哪里？）

### 伯里视角（深度价值）
（清算价值如何？是否有隐藏风险？）

## 3. 综合方向判断
**短期（1-4周）**：[看涨/看跌/震荡] [方向符号]
- 主要逻辑支撑（2-3点）

**中期（1-3月）**：[看涨/看跌/震荡] [方向符号]
- 逻辑是否成立？

## 4. 风险提示
- 最大下行空间/止损位
- 触发止损的条件
- 主要风险因素

## 5. 投资建议
- 仓位建议：[观望/轻仓/标准仓/重仓]
- 入场时机参考
- 止损位置参考
- 大师会怎么做？（根据大师框架推断）

## 6. 你最想强调的一点
（用一句话总结最重要的判断）
"""


# ── MiniMax API 调用 ──────────────────────────────────────

def call_minimax(prompt: str, max_tokens: int = 1500) -> str:
    """
    调用 MiniMax-Text-2.7 进行分析
    """
    if not MINIMAX_API_KEY:
        return _fallback_analysis(prompt)

    for attempt in range(3):
        try:
            resp = requests.post(
                f"{MINIMAX_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {MINIMAX_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "MiniMax-Text-01",
                    "max_tokens": max_tokens,
                    "temperature": 0.3,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=60,
            )
            resp.raise_for_status()
            choices = resp.json().get("choices", [])
            if choices and isinstance(choices[0], dict):
                msg = choices[0]
                content = msg.get("message", {}).get("content", "") if isinstance(msg, dict) else str(choices[0])
                print(f"  [MiniMax OK]")
                return content
            return ""
        except Exception as e:
            print(f"  [MiniMax 失败{' (重试)' if attempt < 2 else ''}] {e}")
            if attempt < 2:
                time.sleep(2)

    return _fallback_analysis(prompt)


def _fallback_analysis(prompt: str) -> str:
    """
    MiniMax 不可用时的简易分析（基于规则）
    """
    return """[MiniMax API 不可用，请手动分析]

建议从以下角度思考：

1. **价格信号**：当前价格 vs 均线位置、涨跌幅
2. **大师框架**：用巴菲特/芒格/达利欧/马克斯的框架分析
3. **风险管理**：设置止损位，控制仓位

请使用 /investment 命令或直接提问，我会尝试调用 AI 分析。
"""


# ── 分析函数 ──────────────────────────────────────────────

def analyze_asset(
    ticker: str,
    asset_name: str,
    price_data: dict,
    macro_data: dict,
    news: list,
    master_views: str,
    user_query: str = "",
    max_tokens: int = 1500,
) -> str:
    """
    综合分析单个资产

    Args:
        ticker: 标的代码
        asset_name: 资产名称
        price_data: 价格数据
        macro_data: 宏观数据
        news: 市场新闻
        master_views: 大师观点（格式化后的字符串）
        user_query: 用户的问题
        max_tokens: 最大 token 数

    Returns:
        分析报告（Markdown 格式）
    """
    # 格式化价格数据
    price_str = _format_price_data(price_data)

    # 格式化宏观数据
    macro_str = _format_macro_data(macro_data)

    # 格式化新闻
    news_str = _format_news(news)

    # 构建 prompt
    prompt = MARKET_ANALYSIS_PROMPT_TEMPLATE.format(
        master_framework=MASTER_FRAMEWORK,
        asset_name=asset_name,
        ticker=ticker,
        user_query=user_query or "这笔投资当前怎么看？",
        price_data=price_str,
        macro_data=macro_str,
        news_data=news_str,
        master_views=master_views,
    )

    # 调用 MiniMax
    return call_minimax(prompt, max_tokens=max_tokens)


def _format_price_data(price_data: dict) -> str:
    """格式化价格数据"""
    if not price_data or price_data.get("error"):
        return "（价格数据不可用）"

    lines = [
        f"- 当前价格：{price_data.get('price', 'N/A')}",
        f"- 涨跌额：{price_data.get('change', 0):+.2f}",
        f"- 涨跌幅：{price_data.get('change_pct', 0):+.2f}%",
    ]

    if price_data.get("prev_close"):
        lines.append(f"- 昨收：{price_data['prev_close']}")

    if price_data.get("ma20"):
        lines.append(f"- 20日均线：{price_data['ma20']}")
        price = price_data.get("price")
        ma20 = price_data.get("ma20")
        if price and ma20:
            diff = (price - ma20) / ma20 * 100
            lines.append(f"- 均线偏离度：{diff:+.2f}%")

    if price_data.get("high"):
        lines.append(f"- 今日高点：{price_data['high']}")

    if price_data.get("low"):
        lines.append(f"- 今日低点：{price_data['low']}")

    return "\n".join(lines)


def _format_macro_data(macro_data: dict) -> str:
    """格式化宏观数据"""
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
            date = data.get("date", "")
            if value is not None:
                lines.append(f"- {name}：{value}（{date}）")

    return "\n".join(lines) if lines else "（宏观数据不可用）"


def _format_news(news: list) -> str:
    """格式化新闻"""
    if not news:
        return "（暂无相关新闻）"

    lines = []
    for i, item in enumerate(news[:5], 1):
        title = item.get("title", "")
        snippet = item.get("snippet", "")[:100]
        lines.append(f"{i}. **{title}**")
        if snippet:
            lines.append(f"   {snippet}...")

    return "\n".join(lines)


def quick_analysis(user_query: str, asset_name: str = "") -> str:
    """
    快速分析（不需要完整数据）

    用于用户提出问题但还没有完整数据时
    """
    prompt = f"""{MASTER_FRAMEWORK}

===

用户问题：{user_query}

请从大师投资智慧的角度，给出你的分析框架和建议。
不用调用任何 API，直接给出有价值的分析。

回答用中文，结构清晰。
"""
    return call_minimax(prompt, max_tokens=800)


def fact_check(content: str) -> str:
    """
    事实核查

    金融领域幻觉信息可能致命，此函数对分析内容进行事实核查

    Args:
        content: 待核查的内容（通常是分析报告）

    Returns:
        核查结果
    """
    prompt = FACT_CHECK_PROMPT.format(content=content)
    return call_minimax(prompt, max_tokens=1000)


def analyze_with_fact_check(
    ticker: str,
    asset_name: str,
    price_data: dict,
    macro_data: dict,
    news: list,
    master_views: str,
    user_query: str = "",
    max_tokens: int = 1500,
) -> dict:
    """
    带事实核查的综合分析

    先进行大师框架分析，再对分析结果进行事实核查

    Returns:
        dict: {
            "analysis": str,  # 原始分析报告
            "fact_check": str,  # 事实核查结果
        }
    """
    # 第一步：大师框架分析
    analysis = analyze_asset(
        ticker=ticker,
        asset_name=asset_name,
        price_data=price_data,
        macro_data=macro_data,
        news=news,
        master_views=master_views,
        user_query=user_query,
        max_tokens=max_tokens,
    )

    # 第二步：事实核查
    fact_check_result = fact_check(analysis)

    return {
        "analysis": analysis,
        "fact_check": fact_check_result,
    }


if __name__ == "__main__":
    # 测试
    print("=== 测试大师框架 ===")
    test_query = "当前世界格局动荡，为什么黄金反而暴跌？这不符合避险逻辑"
    result = quick_analysis(test_query, "黄金")
    print(result)
