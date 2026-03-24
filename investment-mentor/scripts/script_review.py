"""
Investment Mentor - 播客文字稿自检清单
每次生成初稿后自动检查，确保质量底线
"""

# 播客质量自检维度
REVIEW_DIMENSIONS = {
    "hook": {
        "name": "开头钩子",
        "weight": 1.5,
        "checkpoints": [
            "前3句话内有没有抛出让人好奇的问题？",
            "有没有反直觉的statement让人想继续听？",
        ],
        "keywords": ["奇怪", "反常", "不可思议", "为什么", "陷阱", "误区", "有意思"],
    },
    "counter_intuitive": {
        "name": "反常识观点",
        "weight": 2.0,
        "checkpoints": [
            "有没有颠覆大众认知的point？",
            "有没有'大多数人都想错了'的洞察？",
            "有没有'教科书不会教'的实战智慧？",
        ],
        "keywords": ["误区", "其实", "但", "相反", "表面上", "真相是"],
    },
    "dialogue_organic": {
        "name": "对话有机感",
        "weight": 1.5,
        "checkpoints": [
            "有没有追问和接话？",
            "有没有被打断和转折？",
            "是不是一直'是的然后'的流水账？",
        ],
        "bad_patterns": ["是的", "然后", "接下来", "首先", "其次", "最后"],
    },
    "awe_moment": {
        "name": "啊哈时刻",
        "weight": 1.5,
        "checkpoints": [
            "有没有让人拍大腿的瞬间？",
            "有没有让人想截图分享的句子？",
            "有没有一个反问比陈述更有力的地方？",
        ],
    },
    "master_depth": {
        "name": "大师深度",
        "weight": 1.0,
        "checkpoints": [
            "引用大师之后有没有展开？",
            "大师的话有没有被'翻译'成普通人能用的语言？",
        ],
    },
    "takeaway": {
        "name": "带走感",
        "weight": 2.0,
        "checkpoints": [
            "结尾有没有清晰的actionable建议？",
            "有没有留思考题让用户参与？",
        ],
        "keywords": ["记住", "答案是", "三个问题", "算一算", "实战题"],
    },
    "narrative_arc": {
        "name": "叙事弧线",
        "weight": 1.0,
        "checkpoints": [
            "开头、中段、结尾节奏是否不同？",
            "有没有'起承转合'而不是平铺直叙？",
        ],
    },
    "emotion_variation": {
        "name": "情绪起伏",
        "weight": 1.0,
        "checkpoints": [
            "全篇是否只有一种情绪（平静）？",
            "有没有惊讶、质疑、感叹等情绪变化？",
        ],
    },
}


def score_dimension(dimension_name: str, script_lines: list) -> dict:
    """对单个维度打分"""
    dim = REVIEW_DIMENSIONS[dimension_name]
    score = 0
    issues = []
    suggestions = []

    script_text = " ".join([line["text"] for line in script_lines])

    # 检查关键词
    if "keywords" in dim:
        keyword_count = sum(1 for kw in dim["keywords"] if kw in script_text)
        if keyword_count > 0:
            score += 2
        else:
            issues.append(f"缺少维度'{dim['name']}'的信号词")

    # 检查不良模式
    if "bad_patterns" in dim:
        bad_count = sum(1 for bp in dim["bad_patterns"] if bp in script_text)
        if bad_count > 3:
            issues.append(f"发现{bad_count}处流水账模式")
            suggestions.append("减少'是的然后'结构，多用追问和转折")

    # 检查问号（代表追问和参与）
    question_count = script_text.count("？")
    if question_count < 3 and dimension_name == "dialogue_organic":
        issues.append("问句太少，对话感不足")
        suggestions.append("增加反问和追问")

    return {
        "dimension": dim["name"],
        "weight": dim["weight"],
        "score": score,
        "max_score": 5,
        "issues": issues,
        "suggestions": suggestions,
    }


def review_script(script: dict) -> dict:
    """对整篇文字稿进行质量自检"""
    lines = script.get("content", [])
    if not lines:
        return {"error": "Empty script"}

    results = []
    total_weighted_score = 0
    total_weight = 0

    for dim_name in REVIEW_DIMENSIONS:
        result = score_dimension(dim_name, lines)
        results.append(result)
        total_weighted_score += result["score"] * result["weight"]
        total_weight += result["weight"]

    overall_score = round(total_weighted_score / total_weight, 1)

    # 评级
    if overall_score >= 4.5:
        grade = "A"
        verdict = "优质，可以生成"
    elif overall_score >= 3.5:
        grade = "B"
        verdict = "良好，有小幅改进空间"
    elif overall_score >= 2.5:
        grade = "C"
        verdict = "及格，需要改进"
    else:
        grade = "D"
        verdict = "不达标，建议重写"

    all_issues = []
    all_suggestions = []
    for r in results:
        all_issues.extend(r["issues"])
        all_suggestions.extend(r["suggestions"])

    return {
        "overall_score": overall_score,
        "grade": grade,
        "verdict": verdict,
        "dimension_scores": results,
        "issues": list(dict.fromkeys(all_issues)),
        "suggestions": list(dict.fromkeys(all_suggestions)),
    }


def print_review_report(review_result: dict):
    """打印可读的审查报告"""
    print(f"\n{'='*60}")
    print(f"📋 播客文字稿质量自检报告")
    print(f"{'='*60}")
    print(f"\n综合评分: {review_result['overall_score']} / 5  ({review_result['grade']})")
    print(f"结论: {review_result['verdict']}")

    print(f"\n--- 各维度评分 ---")
    for r in review_result["dimension_scores"]:
        bar = "█" * r["score"] + "░" * (5 - r["score"])
        print(f"  {r['dimension']:<12} {bar}  {r['score']}/5")

    if review_result["issues"]:
        print(f"\n--- 发现问题 ---")
        for issue in review_result["issues"]:
            print(f"  ⚠️  {issue}")

    if review_result["suggestions"]:
        print(f"\n--- 改进建议 ---")
        for sug in review_result["suggestions"]:
            print(f"  💡  {sug}")

    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    # 演示用法
    demo_script = {
        "title": "测试：美元还是黄金",
        "content": [
            {"speaker": "A", "text": "明远，我最近被问最多的一个问题是——现在该持有美元还是黄金？"},
            {"speaker": "B", "text": "好问题。但这个问题本身就有陷阱——你得先告诉我，你的投资目标是什么。"},
            {"speaker": "A", "text": "这话怎么说？一般人不是看哪个涨就买哪个吗？"},
            {"speaker": "B", "text": "这就是散户最常见的误区。看涨跌买股票，看涨跌买黄金——听起来合理，但其实是在追趋势。"},
        ]
    }
    result = review_script(demo_script)
    print_review_report(result)
