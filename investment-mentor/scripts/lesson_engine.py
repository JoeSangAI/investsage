"""
Investment Mentor - 课程引擎
生成双人对谈播客风格的课程内容
多样化格式 + 有机对话 + 大师智慧
"""

import os
import json
import random
from datetime import datetime
from typing import Optional, List

try:
    from mcp__MiniMax__TTS import generate_tts
except ImportError:
    generate_tts = None

from curriculum import (
    get_topic,
    get_next_topic,
    recommend_topic,
    get_topic_by_tag,
    TOPICS,
)
from memory import (
    get_user_profile,
    record_lesson_completed,
    record_concept_learning,
    record_thinking_answer,
)
from config import load_config

try:
    from news_searcher import pick_relevant_hot_topic, get_market_hot_topics, BOCHA_API_KEY
    HAS_NEWS_SEARCH = True
except ImportError:
    HAS_NEWS_SEARCH = False
    BOCHA_API_KEY = None


# 有机对话插入语库
INTERJECTIONS = [
    "等等，让我先插一句——",
    "你说的这个让我想到——",
    "这个逻辑有意思的地方在于——",
    "我简直不敢相信这个数据——",
    "等等，你刚才说的这个和之前那个是矛盾的——",
    "我们来推演一下——",
    "说实话，这个观点我一开始也不认同——",
    "让我换个角度问你——",
]


class DualHostLessonEngine:
    """双人对谈课程引擎 - 多样化格式"""

    def __init__(self):
        self.config = load_config()
        self.hosts = {
            "A": {
                "name": "明远",
                "style": "理性分析型",
                "personality": "擅长从数据和模型出发，喜欢追问底层逻辑，视角多元",
                "voice_id": "Chinese_gravelly_storyteller_vv2",
            },
            "B": {
                "name": "雨晴",
                "style": "直觉洞察型",
                "personality": "善于捕捉市场情绪和异常，关注大师智慧和跨学科思维",
                "voice_id": "Chinese_crisp_podcaster_vv1",
            },
        }

    def generate_lesson(
        self,
        topic_id: str = None,
        user_query: str = None,
        hot_topic: dict = None,
    ) -> dict:
        """生成一节课"""
        config = self.config
        profile = get_user_profile()

        if topic_id:
            topic = get_topic(topic_id)
        elif user_query:
            topic = self._match_topic_from_query(user_query)
        else:
            topic = recommend_topic(
                user_interests=profile.get("interests", []),
                completed_topics=profile.get("completed_lessons", []),
            )

        if not topic:
            topic = get_topic("REAL-RATE")

        record_concept_learning(topic["id"])

        if not hot_topic and HAS_NEWS_SEARCH and BOCHA_API_KEY:
            hot_topics = get_market_hot_topics()
            hot_topic = pick_relevant_hot_topic(topic["id"], hot_topics)

        macro_context = self._get_macro_context(topic)
        dialogue_format = topic.get("dialogue_format", "insight")

        script = self._generate_dialogue_by_format(
            topic, hot_topic, macro_context, dialogue_format
        )

        audio_files = self._generate_audio(script)
        record_lesson_completed(f"lesson_{topic['id']}", topic["id"])

        return {
            "topic": topic,
            "script": script,
            "audio_files": audio_files,
            "duration_minutes": config.get("lesson", {}).get("duration_minutes", 10),
            "hot_topic": hot_topic,
        }

    def _match_topic_from_query(self, query: str) -> Optional[dict]:
        """从用户问题匹配主题"""
        keywords = {
            "黄金": "GOLD",
            "股票": "MOAT",
            "债券": "RISK-PARITY",
            "利率": "INTEREST-RATE",
            "通胀": "INFLATION",
            "美元": "DOLLAR",
            "实际利率": "REAL-RATE",
            "周期": "CYCLE",
            "护城河": "MOAT",
            "估值": "VALUATION",
            "安全边际": "MARGIN-OF-SAFETY",
            "Mr. Market": "MR-MARKET",
            "行为金融": "BEHAVIORAL",
            "心理": "PSYCHOLOGY",
        }

        for keyword, topic_id in keywords.items():
            if keyword in query:
                topic = get_topic(topic_id)
                if topic:
                    return topic

        return None

    def _get_macro_context(self, topic: dict) -> dict:
        """获取宏观背景"""
        return {
            "gold_price": "$2,985",
            "gold_change": "-2.3%",
            "dollar_index": "104.5",
            "fed_rate": "5.25%",
            "inflation": "3.2%",
            "real_rate": "2.05%",
            "sp500_pe": "21.3",
            "10y_yield": "4.2%",
        }

    def _generate_dialogue_by_format(
        self,
        topic: dict,
        hot_topic: dict = None,
        macro_context: dict = None,
        dialogue_format: str = "insight",
    ) -> dict:
        """根据格式生成对话"""
        format_methods = {
            "insight": self._generate_insight_dialogue,
            "story": self._generate_story_dialogue,
            "debate": self._generate_debate_dialogue,
            "practical": self._generate_practical_dialogue,
            "thought": self._generate_thought_dialogue,
        }

        method = format_methods.get(dialogue_format, self._generate_insight_dialogue)
        script = method(topic, hot_topic, macro_context)

        if hot_topic:
            script = self._prepend_hot_topic(script, hot_topic)

        return script

    def _interjection(self) -> str:
        """随机返回一个有机插入语"""
        return random.choice(INTERJECTIONS)

    def _generate_insight_dialogue(
        self,
        topic: dict,
        hot_topic: dict = None,
        macro_context: dict = None,
    ) -> dict:
        """洞察驱动型：快问快答 → 突然深入 → 反转
        适用：宏观、利率、美元、黄金
        """
        topic_name = topic.get("name", "")
        hook = topic.get("hook", "")
        teaching_points = topic.get("teaching_points", [])
        master_view = topic.get("master_view", {})
        controversy = topic.get("controversy", "")
        listener_exercise = topic.get("listener_exercise", "")

        content = []

        # 开场：抛出反直觉的hook
        content.append({"speaker": "B", "text": f"明远，有个事儿特别奇怪——{hook}"})
        content.append({"speaker": "A", "text": "等等，你这话说反了吧？一般人不是都觉得..."})

        # 快问快答 - 第一层
        if teaching_points:
            content.append({"speaker": "B", "text": teaching_points[0]})
            content.append({"speaker": "A", "text": f"{self._interjection()}这个逻辑，如果反过来想呢？"})

        # 突然深入 - 第二层
        if len(teaching_points) > 1:
            content.append({"speaker": "B", "text": f"但问题没那么简单——{teaching_points[1]}"})
            content.append({"speaker": "A", "text": "等等，让我顺着你的思路往下推——这个逻辑的尽头是什么？"})

        # 大师视角（随机选一个）
        if master_view:
            master_key = random.choice(list(master_view.keys()))
            master_quote = master_view[master_key]
            masters_map = {
                "buffett": "巴菲特", "munger": "芒格", "dalio": "达利欧",
                "marks": "马克斯", "soros": "索罗斯", "lynch": "林奇",
                "templeton": "邓普顿", "burry": "伯里",
            }
            master_name = masters_map.get(master_key, master_key)
            content.append({"speaker": "A", "text": f"话说回来，{master_name}怎么说来着——'{master_quote}'"})

        # 反转观点
        if controversy:
            content.append({"speaker": "B", "text": f"但等等，这里有个矛盾——{controversy[:120]}"})
            content.append({"speaker": "A", "text": "所以真相是……？这就颠覆了我们刚才的判断。"})

        # 思考题
        if listener_exercise:
            content.append({"speaker": "B", "text": f"给你留个问题——{listener_exercise}"})

        return {
            "title": f"洞察：{topic_name}",
            "content": content,
            "format": "insight",
        }

    def _generate_story_dialogue(
        self,
        topic: dict,
        hot_topic: dict = None,
        macro_context: dict = None,
    ) -> dict:
        """故事叙事型：完整故事 → 中途打断 → 追问细节
        适用：大师思想、案例分析
        """
        topic_name = topic.get("name", "")
        hook = topic.get("hook", "")
        case_story = topic.get("case_study", "")
        master_view = topic.get("master_view", {})
        teaching_points = topic.get("teaching_points", [])
        listener_exercise = topic.get("listener_exercise", "")

        content = []

        # 开场：从一个故事开始
        content.append({"speaker": "B", "text": f"明远，我最近在琢磨一件事——{hook}"})
        content.append({"speaker": "A", "text": "说说看，我有兴趣。"})
        content.append({"speaker": "B", "text": f"其实这个问题背后有个故事——{case_story[:200]}..."})

        # 中途被打断
        content.append({"speaker": "A", "text": "等等，停一下——你刚才说的这个地方我没想通。"})

        # 追问细节
        if teaching_points:
            content.append({"speaker": "B", "text": f"好问题。让我解释一下——{teaching_points[0]}"})

        # 大师视角
        if master_view:
            master_key = random.choice(list(master_view.keys()))
            master_quote = master_view[master_key]
            masters_map = {
                "buffett": "巴菲特", "munger": "芒格", "dalio": "达利欧",
                "marks": "马克斯", "soros": "索罗斯", "lynch": "林奇",
                "templeton": "邓普顿", "burry": "伯里",
            }
            master_name = masters_map.get(master_key, master_key)
            content.append({"speaker": "A", "text": f"{master_name}可不这么认为。他说——'{master_quote}'"})

        # 追问
        content.append({"speaker": "B", "text": f"对，但是——如果把这个逻辑再往前推一步呢？{teaching_points[1] if len(teaching_points) > 1 else ''}"})
        content.append({"speaker": "A", "text": "我懂了。这个故事的教训是——事情往往比表面复杂得多。"})

        # 思考题
        if listener_exercise:
            content.append({"speaker": "B", "text": f"最后留个问题给你——{listener_exercise}"})

        return {
            "title": f"故事：{topic_name}",
            "content": content,
            "format": "story",
        }

    def _generate_debate_dialogue(
        self,
        topic: dict,
        hot_topic: dict = None,
        macro_context: dict = None,
    ) -> dict:
        """观点交锋型：A说→B反驳→激烈讨论→共识
        适用：争议话题、矛盾数据
        """
        topic_name = topic.get("name", "")
        hook = topic.get("hook", "")
        controversy = topic.get("controversy", "")
        teaching_points = topic.get("teaching_points", [])
        master_view = topic.get("master_view", {})
        listener_exercise = topic.get("listener_exercise", "")

        content = []

        # 开场：抛出争议
        content.append({"speaker": "B", "text": f"明远，我觉得{topic_name}这事儿的答案是明摆着的——{hook}"})

        # 明远反驳
        content.append({"speaker": "A", "text": f"等等，这个我完全不同意。你只看到了表面——{teaching_points[0] if teaching_points else ''}"})
        content.append({"speaker": "B", "text": "什么？你这说法站不住脚吧？我的逻辑是——"})

        # 雨晴坚持
        if len(teaching_points) > 1:
            content.append({"speaker": "B", "text": teaching_points[1]})

        # 激烈讨论
        content.append({"speaker": "A", "text": f"{self._interjection()}你这么说不全面。实际情况是——{teaching_points[2] if len(teaching_points) > 2 else '还要考虑更多因素'}"})

        # 大师介入
        if master_view:
            for master_key, master_quote in list(master_view.items())[:2]:
                masters_map = {
                    "buffett": "巴菲特", "munger": "芒格", "dalio": "达利欧",
                    "marks": "马克斯", "soros": "索罗斯", "lynch": "林奇",
                    "templeton": "邓普顿", "burry": "伯里",
                }
                master_name = masters_map.get(master_key, master_key)
                content.append({"speaker": "A", "text": f"说到这个，{master_name}有句话特别到位——'{master_quote}'"})

        # 争议焦点
        if controversy:
            content.append({"speaker": "B", "text": f"好吧好吧，我们先退一步——{controversy[:120]}"})
            content.append({"speaker": "A", "text": "这才对嘛。所以答案是……要看情况。"})

        # 共识
        content.append({"speaker": "A", "text": "说到底，这个问题的本质是——没有简单的对错，关键看你站在哪个角度。"})

        # 思考题
        if listener_exercise:
            content.append({"speaker": "B", "text": f"给你留个思考题——{listener_exercise}"})

        return {
            "title": f"交锋：{topic_name}",
            "content": content,
            "format": "debate",
        }

    def _generate_practical_dialogue(
        self,
        topic: dict,
        hot_topic: dict = None,
        macro_context: dict = None,
    ) -> dict:
        """实战复盘型：真实场景 → 拆解决策 → 教训总结
        适用：具体标的、实际交易
        """
        topic_name = topic.get("name", "")
        hook = topic.get("hook", "")
        case_story = topic.get("case_study", "")
        teaching_points = topic.get("teaching_points", [])
        master_view = topic.get("master_view", {})
        quant_tip = topic.get("quant_tip", "")
        listener_exercise = topic.get("listener_exercise", "")

        content = []

        # 开场：从真实场景切入
        content.append({"speaker": "B", "text": f"明远，我跟你说个我亲身经历的事儿——{hook}"})
        content.append({"speaker": "A", "text": "这事我当时也听说了。你当时怎么想的？"})

        # 拆解决策逻辑
        if teaching_points:
            content.append({"speaker": "B", "text": f"我当时是这么判断的——{teaching_points[0]}"})
            content.append({"speaker": "A", "text": f"{self._interjection()}你这个逻辑有个漏洞——你忽略了什么？"})

        # 案例复盘
        if case_story:
            content.append({"speaker": "B", "text": f"结果呢？市场给了答案——{case_story[:150]}..."})
            content.append({"speaker": "A", "text": "所以这里面的教训是——理论是一回事，现实是另一回事。"})

        # 量化工具
        if quant_tip:
            content.append({"speaker": "B", "text": f"实操上有个参考——{quant_tip}"})

        # 大师会怎么做
        if master_view:
            master_key = random.choice(list(master_view.keys()))
            master_quote = master_view[master_key]
            masters_map = {
                "buffett": "巴菲特", "munger": "芒格", "dalio": "达利欧",
                "marks": "马克斯", "soros": "索罗斯", "lynch": "林奇",
                "templeton": "邓普顿", "burry": "伯里",
            }
            master_name = masters_map.get(master_key, master_key)
            content.append({"speaker": "A", "text": f"反过来想想，{master_name}会怎么处理这种事？他说——'{master_quote}'"})

        # 教训总结
        content.append({"speaker": "B", "text": f"总结一下今天的教训——{topic_name}这件事上，最重要的是……"})
        content.append({"speaker": "A", "text": "记住一条：市场永远有机会，但钱是赚不完的，命只有一条。"})

        # 思考题
        if listener_exercise:
            content.append({"speaker": "B", "text": f"给你留个实战题——{listener_exercise}"})

        return {
            "title": f"实战：{topic_name}",
            "content": content,
            "format": "practical",
        }

    def _generate_thought_dialogue(
        self,
        topic: dict,
        hot_topic: dict = None,
        macro_context: dict = None,
    ) -> dict:
        """思想实验型：假设场景 → 推演结果 → 颠覆认知
        适用：大师框架、哲学思考
        """
        topic_name = topic.get("name", "")
        hook = topic.get("hook", "")
        teaching_points = topic.get("teaching_points", [])
        master_view = topic.get("master_view", {})
        analogy = topic.get("analogy", "")
        controversy = topic.get("controversy", "")
        listener_exercise = topic.get("listener_exercise", "")

        content = []

        # 开场：假设场景
        content.append({"speaker": "B", "text": f"明远，我最近在想一个有趣的思想实验——{hook}"})
        content.append({"speaker": "A", "text": "有意思，说来听听。"})

        # 假设场景深入
        if teaching_points:
            content.append({"speaker": "B", "text": f"假设我们现在处于这样的情况——{teaching_points[0]}"})
            content.append({"speaker": "A", "text": f"{self._interjection()}如果真的是这样，那意味着什么？"})

        # 推演
        if len(teaching_points) > 1:
            content.append({"speaker": "B", "text": f"推演下去会怎样呢——{teaching_points[1]}"})
            content.append({"speaker": "A", "text": "等等，这个推论有个前提我不认同——假设本身可能有问题。"})

        # 大师视角
        if master_view:
            for master_key, master_quote in list(master_view.items())[:2]:
                masters_map = {
                    "buffett": "巴菲特", "munger": "芒格", "dalio": "达利欧",
                    "marks": "马克斯", "soros": "索罗斯", "lynch": "林奇",
                    "templeton": "邓普顿", "burry": "伯里",
                }
                master_name = masters_map.get(master_key, master_key)
                content.append({"speaker": "A", "text": f"有意思的是，{master_name}可不这么认为——'{master_quote}'"})

        # 颠覆认知
        if controversy:
            content.append({"speaker": "B", "text": f"但最颠覆认知的是——{controversy[:120]}"})
            content.append({"speaker": "A", "text": "这彻底改变了我对这个问题的看法。"})

        # 比喻
        if analogy:
            content.append({"speaker": "B", "text": f"说到底，这事儿就像——{analogy}"})

        # 思考题
        if listener_exercise:
            content.append({"speaker": "B", "text": f"给你留个思想题——{listener_exercise}"})

        return {
            "title": f"思想：{topic_name}",
            "content": content,
            "format": "thought",
        }

    def _prepend_hot_topic(self, script: dict, hot_topic: dict) -> dict:
        """在课程开头加入热点话题 - 用真实新闻引发兴趣"""
        news = hot_topic.get("news", [])
        first_news = news[0] if news else {}

        topic_name = hot_topic.get("name", "")

        # 热点开场 - 用真实新闻
        intro_text = f"明远你看，市场上有个事儿特别有意思——{first_news.get('title', topic_name + '最近的市场动态')}"
        if first_news.get("snippet"):
            intro_text += f"，{first_news['snippet'][:80]}"

        # 构建开场白
        hot_content = [
            {"speaker": "B", "text": intro_text},
            {"speaker": "A", "text": "是啊，这种行情让很多人懵了。但如果我们懂了背后的逻辑，就能看清本质。"},
            {"speaker": "B", "text": f"没错！今天我们就用{topic_name}这个话题，带你看穿这个现象。"},
        ]

        # 跳过原对话的前2行开场白（因为hot topic开场更精彩）
        original_content = script.get("content", [])
        # 找到第一个重复内容的位置并跳过
        skip_count = 0
        for i, line in enumerate(original_content[:3]):
            text = line.get("text", "")
            if "明远" in text or "跟你说个事儿" in text:
                skip_count = i + 2  # 跳过这个开场对话
                break

        # 把热点插入到开头，跳过原开场白，原有内容接在后面
        new_content = hot_content + original_content[skip_count:]
        script["content"] = new_content

        return script

    def _generate_audio(self, script: dict) -> dict:
        """生成语音文件"""
        if generate_tts is None:
            return {"status": "unavailable", "message": "TTS模块不可用"}

        audio_files = {}
        config = self.config.get("tts", {})

        for i, line in enumerate(script.get("content", [])):
            speaker_key = line.get("speaker")
            voice_id = self.hosts[speaker_key]["voice_id"]
            text = line.get("text", "")

            try:
                result = generate_tts(
                    text=text,
                    voice_id=voice_id,
                    speed=config.get("speed", 1.0),
                )
                audio_files[f"line_{i}"] = result
            except Exception as e:
                audio_files[f"line_{i}"] = {"status": "error", "message": str(e)}

        return {"status": "generated", "files": audio_files}

    def format_script_as_text(self, script: dict) -> str:
        """把脚本格式化为可读的文本"""
        lines = []
        lines.append(f"# {script.get('title', '课程')}\n")

        host_a = self.hosts["A"]
        host_b = self.hosts["B"]

        for line in script.get("content", []):
            speaker_key = line.get("speaker")
            text = line.get("text", "")

            if speaker_key == "A":
                lines.append(f"【{host_a['name']}】：{text}")
            else:
                lines.append(f"【{host_b['name']}】：{text}")

        return "\n".join(lines)


def generate_lesson(
    topic_id: str = None,
    user_query: str = None,
    hot_topic: dict = None,
) -> dict:
    """便捷函数：生成一节课"""
    engine = DualHostLessonEngine()
    return engine.generate_lesson(topic_id, user_query, hot_topic)


def format_lesson_text(script: dict) -> str:
    """便捷函数：格式化课程文本"""
    engine = DualHostLessonEngine()
    return engine.format_script_as_text(script)


if __name__ == "__main__":
    # 测试 - 生成不同格式的两期播客
    for topic_id in ["GOLD", "MOAT", "BEHAVIORAL"]:
        topic = get_topic(topic_id)
        print(f"\n{'='*60}")
        print(f"格式: {topic.get('dialogue_format', 'unknown')}")
        print(f"标题: {topic['name']}")
        print(f"{'='*60}")
        lesson = generate_lesson(topic_id)
        print(format_lesson_text(lesson["script"]))
