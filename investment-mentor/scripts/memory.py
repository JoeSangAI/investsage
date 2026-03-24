"""
Investment Mentor - 学习记忆系统
记录用户的学习进度、提问、思考题回答
"""

import os
import json
from datetime import datetime
from typing import Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PROFILE_FILE = os.path.join(DATA_DIR, "user_profile.json")
LOG_FILE = os.path.join(DATA_DIR, "learning_log.json")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def get_user_profile() -> dict:
    """获取用户画像"""
    _ensure_data_dir()
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # 默认用户画像
    return {
        "user_id": "Joe",
        "level": "L1",
        "current_topic": None,
        "completed_lessons": [],
        "questions_asked": [],
        "thinking_answers": [],
        "concepts_mastered": [],
        "concepts_learning": [],
        "last_active": datetime.now().isoformat(),
        "created_at": datetime.now().isoformat(),
    }


def save_user_profile(profile: dict):
    """保存用户画像"""
    _ensure_data_dir()
    profile["last_active"] = datetime.now().isoformat()
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


def record_question(question: str, answer: str = None):
    """记录用户的问题"""
    profile = get_user_profile()
    profile["questions_asked"].append({
        "question": question,
        "answer": answer,
        "date": datetime.now().isoformat(),
    })
    save_user_profile(profile)


def record_thinking_answer(lesson_id: str, answer: str):
    """记录用户对思考题的答案"""
    profile = get_user_profile()
    profile["thinking_answers"].append({
        "lesson_id": lesson_id,
        "answer": answer,
        "date": datetime.now().isoformat(),
    })
    save_user_profile(profile)


def record_lesson_completed(lesson_id: str, topic_id: str):
    """记录完成的课程"""
    profile = get_user_profile()
    if lesson_id not in profile["completed_lessons"]:
        profile["completed_lessons"].append(lesson_id)
    if topic_id not in profile["concepts_mastered"]:
        profile["concepts_mastered"].append(topic_id)
    if topic_id in profile["concepts_learning"]:
        profile["concepts_learning"].remove(topic_id)
    save_user_profile(profile)


def record_concept_learning(topic_id: str):
    """记录正在学习的概念"""
    profile = get_user_profile()
    if topic_id not in profile["concepts_learning"]:
        profile["concepts_learning"].append(topic_id)
    save_user_profile(profile)


def update_level(level: str):
    """更新用户等级"""
    profile = get_user_profile()
    profile["level"] = level
    save_user_profile(profile)


def get_learning_log() -> list:
    """获取学习日志"""
    _ensure_data_dir()
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def add_to_log(entry: dict):
    """添加日志条目"""
    _ensure_data_dir()
    log = get_learning_log()
    log.append({
        **entry,
        "timestamp": datetime.now().isoformat(),
    })
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def get_progress_summary() -> dict:
    """获取学习进度摘要"""
    profile = get_user_profile()
    log = get_learning_log()

    # 计算连续学习天数
    learning_days = set()
    for entry in log:
        if entry.get("type") == "lesson_completed":
            date = entry.get("timestamp", "")[:10]
            learning_days.add(date)

    # 计算平均理解程度（基于回答的正确率）
    answers = profile.get("thinking_answers", [])
    total_answers = len(answers)

    return {
        "total_lessons": len(profile.get("completed_lessons", [])),
        "total_questions": len(profile.get("questions_asked", [])),
        "total_answers": total_answers,
        "current_level": profile.get("level", "L1"),
        "concepts_mastered": len(profile.get("concepts_mastered", [])),
        "concepts_learning": profile.get("concepts_learning", []),
        "last_active": profile.get("last_active", "从未"),
        "streak_days": len(learning_days),
    }


def print_progress():
    """打印学习进度（友好格式）"""
    summary = get_progress_summary()

    print("\n" + "=" * 50)
    print("📚 你的学习进度")
    print("=" * 50)
    print(f"当前等级：{summary['current_level']}")
    print(f"已完成课程：{summary['total_lessons']} 课")
    print(f"提问数：{summary['total_questions']} 个")
    print(f"回答思考题：{summary['total_answers']} 个")
    print(f"掌握概念：{summary['concepts_mastered']} 个")
    print(f"正在学习：{', '.join(summary['concepts_learning']) or '无'}")
    print(f"最后活跃：{summary['last_active'][:10]}")
    print("=" * 50)


if __name__ == "__main__":
    print_progress()
