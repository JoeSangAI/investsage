"""
Investment Mentor - 配置加载器
"""

import os
import yaml
from typing import Optional

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")


def load_config() -> dict:
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def get_tts_config() -> dict:
    """获取TTS配置"""
    config = load_config()
    return config.get("tts", {
        "voice_id_male": "Chinese_Male_1",
        "voice_id_female": "Chinese_Female_1",
        "speed": 1.0,
    })


def get_lesson_config() -> dict:
    """获取课程配置"""
    config = load_config()
    return config.get("lesson", {
        "duration_minutes": 10,
        "warmup_seconds": 5,
        "hot_topic_weight": 0.4,
        "user_need_weight": 0.3,
        "knowledge_weight": 0.3,
    })


def get_learning_config() -> dict:
    """获取学习配置"""
    config = load_config()
    return config.get("learning", {
        "default_level": "L1",
        "new_lesson_interval": 1,
        "review_threshold": 3,
    })


if __name__ == "__main__":
    print("=== 配置测试 ===")
    print(f"TTS: {get_tts_config()}")
    print(f"课程: {get_lesson_config()}")
    print(f"学习: {get_learning_config()}")
