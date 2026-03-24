"""
Investment Mentor - 主入口
每天生成一段双人对谈播客风格的语音课
"""

import os
import sys
import argparse
from datetime import datetime

# 添加脚本目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# 导入
from lesson_engine import generate_lesson, format_lesson_text
from memory import (
    get_user_profile,
    print_progress,
    record_question,
    record_thinking_answer,
    get_progress_summary,
)
from curriculum import get_topic, get_next_topic, recommend_topic, get_topic_by_tag, TOPICS
from config import load_config


def cmd_lesson(args):
    """生成今日课程"""
    topic_id = args.topic if hasattr(args, 'topic') and args.topic else None

    if args.dry_run:
        # 预览模式
        profile = get_user_profile()
        if topic_id:
            topic = get_topic(topic_id)
        else:
            topic = recommend_topic(
                profile.get("level", "L1"),
                profile.get("concepts_mastered", []),
            )

        print(f"\n{'='*60}")
        print(f"📚 今日课程预览")
        print(f"{'='*60}")
        print(f"主题：{topic['name']}")
        print(f"分类：{topic.get('category', '专题')}")
        print(f"标签：{', '.join(topic.get('tags', []))}")
        print(f"Hook：{topic.get('hook', '')}")
        print(f"\n描述：{topic.get('description', '')}")
        print(f"\n核心知识点：")
        for point in topic.get("teaching_points", []):
            print(f"  • {point}")
        print(f"\n争议点：{topic.get('controversy', '无')[:80]}...")
        print(f"\n比喻：{topic.get('analogy', '无')}")
        print(f"\n思考题：{topic.get('listener_exercise', '无')}")
        print(f"{'='*60}")
        return

    # 生成完整课程
    print("\n🎙️ 正在生成课程，请稍候...")

    hot_topic = None
    if args.hot:
        # 可以接入实时热点
        hot_topic = {
            "title": "黄金暴跌",
            "description": "美元强势导致黄金单日下跌3%",
        }

    result = generate_lesson(topic_id=topic_id, hot_topic=hot_topic)
    topic = result["topic"]
    script = result["script"]

    # 打印课程文本
    lesson_text = format_lesson_text(script)

    print(f"\n{'='*60}")
    print(f"🎙️ {result['topic']['name']} | {topic.get('category', '专题')}")
    print(f"{'='*60}")
    print(lesson_text)
    print(f"{'='*60}")
    print(f"⏱️ 时长约 {result['duration_minutes']} 分钟")
    print(f"💡 思考题：学完想想这个问题，然后回复'/invest 回答 [你的想法]'")

    return result


def cmd_ask(args):
    """回答用户问题"""
    question = args.question if hasattr(args, 'question') else ""

    if not question:
        print("请输入你的问题，例如：/invest ask 黄金为什么能避险？")
        return

    # 记录问题
    record_question(question)

    # 简单匹配相关主题
    topic_match = {
        "黄金": "L1-WHAT-IS-GOLD",
        "股票": "L1-WHAT-IS-STOCK",
        "债券": "L1-WHAT-IS-BOND",
        "利率": "L2-INTEREST-RATE",
        "通胀": "L2-INFLATION",
        "美元": "L2-DOLLAR",
        "实际利率": "L2-REAL-RATE",
        "周期": "L3-MARKET-CYCLE",
        "风险": "L3-RISK-PARITY",
    }

    related_topic = None
    for keyword, topic_id in topic_match.items():
        if keyword in question:
            related_topic = get_topic(topic_id)
            break

    print(f"\n{'='*60}")
    print(f"💬 你的问题：{question}")
    print(f"{'='*60}")

    if related_topic:
        print(f"\n📖 相关知识点：{related_topic['name']}")
        print(f"   {related_topic.get('description', '')}")
        print(f"\n   核心要点：")
        for point in related_topic.get("teaching_points", []):
            print(f"   • {point}")
        print(f"\n   💡 {related_topic.get('analogy', '')}")
    else:
        print("\n这个问题比较综合，我建议先听一下《实际利率》和《市场周期》这两课，会有更深的理解。")

    print(f"\n{'='*60}")


def cmd_answer(args):
    """记录思考题答案"""
    answer = args.answer if hasattr(args, 'answer') else ""

    if not answer:
        print("请输入你的思考答案，例如：/invest 回答 我觉得黄金的避险属性在于...")
        return

    profile = get_user_profile()
    current_topic = profile.get("concepts_learning", [""])[0] if profile.get("concepts_learning") else None

    record_thinking_answer(current_topic or "unknown", answer)

    print(f"\n{'='*60}")
    print(f"✅ 收到你的思考！")
    print(f"{'='*60}")
    print(f"你的回答：{answer[:100]}{'...' if len(answer) > 100 else ''}")
    print(f"\n📚 继续学习下一课？输入 /invest lesson")


def cmd_progress(args):
    """查看学习进度"""
    print_progress()


def cmd_list(args):
    """列出知识点"""
    level = args.level if hasattr(args, 'level') and args.level else None

    if level:
        topics = get_topic_by_tag(level.lower())
        print(f"\n{'='*60}")
        print(f"📚 {level}标签知识点")
        print(f"{'='*60}")
        for t in topics:
            print(f"  • {t['name']} ({t['id']})")
            print(f"    {t.get('description', '')}")
    else:
        profile = get_user_profile()

        print(f"\n{'='*60}")
        print(f"📚 知识体系总览")
        print(f"{'='*60}")

        # 按分类展示
        categories = {}
        for topic in TOPICS.values():
            cat = topic.get("category", "其他")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(topic)

        for cat, topics in categories.items():
            print(f"\n【{cat}】")
            for t in topics:
                mastered = "✓" if t['id'] in profile.get("concepts_mastered", []) else "○"
                print(f"    {mastered} {t['name']} ({t['id']})")

        print(f"\n{'='*60}")
        print(f"✅ 已掌握 | ○ 未学习")
        print(f"标签：macro=宏观 | master=大师智慧 | practice=实战 | gold=黄金专题 | psychology=心理")


def main():
    parser = argparse.ArgumentParser(description="Investment Mentor - 投资教练")
    subparsers = parser.add_subparsers(dest="cmd", help="命令")

    # lesson 命令
    lesson_parser = subparsers.add_parser("lesson", help="生成今日课程")
    lesson_parser.add_argument("-t", "--topic", help="指定主题ID")
    lesson_parser.add_argument("--hot", action="store_true", help="结合热点话题")
    lesson_parser.add_argument("--dry-run", action="store_true", help="预览模式")

    # ask 命令
    ask_parser = subparsers.add_parser("ask", help="提问")
    ask_parser.add_argument("question", nargs="?", help="问题内容")

    # 回答 命令
    answer_parser = subparsers.add_parser("回答", help="回答思考题")
    answer_parser.add_argument("answer", nargs="?", help="答案内容")

    # 进度 命令
    subparsers.add_parser("进度", help="查看学习进度")

    # list 命令
    list_parser = subparsers.add_parser("list", help="列出知识点")
    list_parser.add_argument("-l", "--level", help="筛选级别")

    args = parser.parse_args()

    if args.cmd == "lesson":
        cmd_lesson(args)
    elif args.cmd == "ask":
        cmd_ask(args)
    elif args.cmd == "回答":
        cmd_answer(args)
    elif args.cmd == "进度":
        cmd_progress(args)
    elif args.cmd == "list":
        cmd_list(args)
    else:
        # 默认显示帮助
        print("""
🎙️ Investment Mentor - 你的个人投资教练

使用方法：
  /invest lesson      生成今日课程
  /invest lesson -t L1-WHAT-IS-GOLD   指定主题
  /invest lesson --dry-run            预览模式
  /invest ask 黄金为什么能避险         提问
  /invest 回答 我觉得...              回答思考题
  /invest 进度                        查看进度
  /invest list                        列出所有知识点
  /invest list -l L2                  只看L2级别
        """)


if __name__ == "__main__":
    main()
