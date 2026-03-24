"""
Investment Mentor - 扁平化知识体系
每课独立 + 有深度的市场智慧 + 大师视角
没有等级递进，每课都可独立学习
"""

from typing import Optional
from datetime import datetime


# 扁平化知识体系 - 每课都是完整的市场智慧
TOPICS = {

    # ═══════════════════════════════════════════════════════
    # 🔵 宏观系列
    # ═══════════════════════════════════════════════════════

    "INTEREST-RATE": {
        "id": "INTEREST-RATE",
        "name": "利率的暗逻辑",
        "tags": ["macro", "foundation"],
        "category": "宏观",
        "dialogue_format": "insight",
        "hook": "美联储加息抗通胀，但为什么有时候越加息美元越弱？大多数人没想明白这个问题。",
        "description": "从美联储到你的投资收益，利率如何传导，为什么它是一切资产定价的锚",
        "teaching_points": [
            "联邦基金利率 → 短期国债 → 企业融资成本 → 股票估值（PE的倒数）",
            "利率是资本的成本，也是所有资产定价的锚（Risk-Free Rate）",
            "收益率曲线（Yield Curve）倒挂往往是衰退的领先指标，而非同步指标",
        ],
        "master_view": {
            "dalio": "长期债务周期中，央行最终会把利率压到0，然后开始QE",
            "munger": "看利率要看真实利率（扣除通胀），名义利率可能是央行操纵的幻觉",
        },
        "controversy": "加息一定能强美元吗？2022年加息周期中，美元确实强；但历史上也有加息美元跌的案例（比如1980年代拉美危机）。预期比动作更重要。",
        "case_study": "1981年沃尔克把利率加到20%，直接终结了通胀预期，但也导致了墨西哥等拉美国家违约——这就是加息的传导链条。",
        "quant_tip": "关注2年期和10年期国债利差，倒挂后12-18个月经济往往衰退",
        "listener_exercise": "查一下当前2y10y利差，如果是负的，想想这意味着什么？",
        "analogy": "利率像是经济的油门和刹车——美联储踩油门，经济就热；踩刹车，经济就冷。但油门和刹车的效果有延迟，而且乘客不一定感觉得到。",
    },

    "INFLATION": {
        "id": "INFLATION",
        "name": "通胀的真相",
        "tags": ["macro", "foundation"],
        "category": "宏观",
        "dialogue_format": "insight",
        "hook": "通胀率相同，结局可能完全不同——资产通胀vs消费品通胀，是两回事。",
        "description": "通胀不是单一数字，核心vs headline，及其对不同资产的影响",
        "teaching_points": [
            "CPI是headline通胀，核心通胀（Core PCE）才是美联储真正盯的——因为食物和能源波动太大",
            "通胀预期（Inflation Expectation）会自我实现——一旦大家都觉得会涨，螺旋就形成了",
            "1970年代大滞胀：工资-价格螺旋，一旦形成就很难打掉，需要沃尔克那样的credible shock",
        ],
        "master_view": {
            "volcker": "打败通胀需要credible的央行——宁可过度紧缩，也不能让预期失控",
            "buffett": "通胀期间股票不是好的对冲工具，除非企业能提价且不流失客户",
        },
        "controversy": "普通人觉得通胀是坏事，但适度的通胀其实是健康经济的标志——没有通胀，意味着需求不足甚至通缩。关键是谁在承担通胀的痛苦。",
        "case_study": "2021-2022年美国通胀：疫情后供应链断裂 + 财政刺激发钱 + 劳动力市场紧张，三重因素叠加。美联储一开始说是'暂时性'，结果判断失误，被迫激进加息。",
        "quant_tip": "TIPS债券收益率直接反映市场对实际利率的预期",
        "listener_exercise": "查查当前核心PCE同比是多少，美联储的2%目标现在处于什么位置？",
        "analogy": "通胀像是经济体的体温——37度正常，40度危险，但不是烧一下就危险，要看烧多久。",
    },

    "DOLLAR": {
        "id": "DOLLAR",
        "name": "美元的霸权逻辑",
        "tags": ["macro", "foundation"],
        "category": "宏观",
        "dialogue_format": "insight",
        "hook": "美元是全球金融的氧气——缺了它系统就死，但呼吸太多也会醉。",
        "description": "美元作为全球储备货币的定价逻辑和周期规律",
        "teaching_points": [
            "美元是全球储备货币，SWIFT结算、原油定价、大宗商品全部以美元计价",
            "美元走势影响：黄金（负相关）、大宗商品（负相关）、新兴市场（负相关）",
            "美元周期往往与新兴市场金融危机高度相关：1980拉美、1997亚洲、2022年斯里兰卡",
        ],
        "master_view": {
            "dalio": "美元霸权建立在你只能用美元买石油这个共识上，这个共识正在被侵蚀",
            "munger": "美元强不代表美国强大——往往是其他货币更弱",
        },
        "controversy": "去美元化是真实趋势还是伪命题？人民币国际化、黄金回流、各国央行增持储备……但美元占比仍然在60%以上。变化是缓慢的，但趋势是确定的。",
        "case_study": "2022年俄乌冲突后，美国把俄罗斯踢出SWIFT，冻结俄罗斯央行3000亿美元资产。这让很多国家意识到：美元武器化是真实风险。沙特开始考虑用人民币结算石油，中国和俄罗斯贸易开始用本币。",
        "quant_tip": "关注DXY（美元指数）和黄金的反向关系，以及新兴市场汇率",
        "listener_exercise": "查查人民币对美元汇率，当前是在历史高位还是低位？和2020年比呢？",
        "analogy": "美元像是全球金融的氧气——缺了它系统就死，但呼吸太多也会醉。美联储管理的是全球美元供给，不是只管美国经济。",
    },

    "REAL-RATE": {
        "id": "REAL-RATE",
        "name": "实际利率：终极锚",
        "tags": ["macro", "foundation"],
        "category": "宏观",
        "dialogue_format": "insight",
        "hook": "实际利率是持有黄金的机会成本——这才是黄金定价的核心变量，不是美元。",
        "description": "一切资产定价的底层锚，连接宏观和资产的核心变量",
        "teaching_points": [
            "实际利率 = 名义利率（FEDFUNDS）- 通胀预期（T10YIE）——精确公式是 (1+名义)/(1+通胀)-1，但简化版在低通胀时期够用",
            "实际利率是持有黄金的机会成本：实际利率↑ = 持有黄金更贵 = 黄金跌",
            "实际利率与黄金、股票估值都高度相关，是连接宏观和资产的核心变量",
        ],
        "master_view": {
            "buffett": "所有资产都应该与无风险实际利率比较——股市的Earnings Yield是否跑赢？",
            "dalio": "当实际利率为负时，人类行为会改变——囤实物、买黄金、追逐风险资产",
        },
        "controversy": "2020年实际利率跌到-1%，黄金却没创新高？为什么？因为实际利率为负的同时，美元也在走强，两个因素对冲了。所以看黄金不能只看一个变量。",
        "case_study": "2022年3月：美联储激进加息，名义利率快速上行；同时通胀预期开始回落。实际利率从负值快速转正，黄金从2050跌到1800——这就是实际利率的力量。",
        "quant_tip": "TIPS（通胀保值债券）收益率 = 实际利率，实时反映市场定价",
        "listener_exercise": "当前实际利率约2%（名义5.25% - 通胀3.2%）。如果明天通胀降到2.5%，实际利率变成多少？这对黄金意味着什么？",
        "analogy": "实际利率像是真实借贷成本——你名义上借5%，通胀3%，你真实借了2%。如果通胀变成0，你真实借了5%。",
    },

    # ═══════════════════════════════════════════════════════
    # 🟡 大师智慧系列
    # ═══════════════════════════════════════════════════════

    "MOAT": {
        "id": "MOAT",
        "name": "护城河的盲区",
        "tags": ["master", "practice", "stock"],
        "category": "大师智慧",
        "dialogue_format": "thought",
        "hook": "亚马逊的ROIC只有5%，远低于平均水平，为什么巴菲特还说是伟大公司？护城河不只是数字。",
        "description": "护城河分析的正确姿势，和为什么大多数人对护城河的理解是错的",
        "teaching_points": [
            "护城河来源：无形资产（品牌/专利）、转换成本、网络效应、成本优势",
            "护城河会变——技术变革、行业颠覆可能在一夜之间摧毁它",
            "用ROIC（资本回报率）而非ROE来衡量护城河的强度——ROIC - WACC > 0才有经济护城河",
        ],
        "master_view": {
            "buffett": "护城河要竞争对手无法复制——这才是真正的竞争优势",
            "munger": "好公司和好生意不一样——要找到能长期保持优势的好生意",
        },
        "controversy": "苹果有没有护城河？雨晴认为有——iOS生态、品牌溢价、转换成本极高。明远认为护城河在，但估值已透支10年。护城河≠值得买，估值决定入场时机。",
        "case_study": "特斯拉案例：2020年底股价1200美元，PE离谱。明远用DCF算出400美元合理价。雨晴做空，结果涨到1200美元做空亏损4倍。但雨晴的逻辑错了吗？三年后看，特斯拉跌回了合理价值。这说明：逻辑对的交易，也需要时间和耐心。",
        "quant_tip": "用ROIC - WACC > 0来判断是否有经济护城河，ROIC > 15%通常是优秀公司的标志",
        "listener_exercise": "思考你持有或关注的股票：竞争对手能复制它的竞争优势吗？5年后这个护城河还在吗？",
        "analogy": "护城河就是企业的刹车系统——能让它在竞争中停下来，而不是被拖着走。但刹车太好也可能让人过于自信，反而在颠覆者出现时反应太慢。",
    },

    "VALUATION": {
        "id": "VALUATION",
        "name": "估值的陷阱",
        "tags": ["master", "practice", "stock"],
        "category": "大师智慧",
        "dialogue_format": "thought",
        "hook": "特斯拉值多少钱？DCF说400，分析师说1200，市场说2000。谁对了？",
        "description": "DCF、相对估值、资产法的正确用法，和为什么模糊的正确胜过精确的错误",
        "teaching_points": [
            "DCF是根本：自由现金流折现到今天，NPV>0才值得看——但DCF的假设一变，结果天差地别",
            "相对估值（PE/PB/PS）用于同行比较，但不能脱离增长率和风险",
            "清算价值是估值底线——股票永远不会跌到0以下太多，但可以长期低于内在价值",
        ],
        "master_view": {
            "keynes": "模糊的正确胜过精确的错误——凯恩斯",
            "munger": "用多种方法交叉验证——如果你只能用一种方法，那是因为你理解不够深",
        },
        "controversy": "亚马逊争议：ROIC低但市值涨100倍。市场在给'假设成长'定价，还是给'现有护城河'定价？两种观点都有道理，这就是市场的复杂性。",
        "case_study": "特斯拉DCF教训：雨晴2020年DCF算出400美元合理价，做空亏损4倍。但问题是：DCF是死的，市场是活的。市场可以无限期地给成长股溢价，只要叙事还在。关键不是DCF对不对，而是你能不能承受等待的痛苦。",
        "quant_tip": "用EV/EBITDA消除资本结构影响，更适合跨行业比较；PEG=PE/Growth，<1可能低估，>2可能高估",
        "listener_exercise": "用简化DCF算一下你关注的公司：假设未来5年每年自由现金流增长X%，永续增长率Y%，贴现率Z%，结果是多少？",
        "analogy": "估值像是给企业称重——体重秤（DCF）、镜子对比（相对估值）、X光（资产法）都是工具，但没有一个是完美的。",
    },

    "CYCLE": {
        "id": "CYCLE",
        "name": "周期的悖论",
        "tags": ["master", "macro"],
        "category": "大师智慧",
        "dialogue_format": "thought",
        "hook": "达利欧说：市场永远在过度悲观和过度乐观之间摆动，从不停留在'合理位置'。",
        "description": "达利欧的债务周期、马克斯的钟摆理论，和为什么预测周期是愚蠢的但感知周期是必要的",
        "teaching_points": [
            "达利欧的长期债务周期：信贷扩张 → 泡沫 → 去杠杆 → 新周期",
            "短期债务周期（商业周期）：8-10年一次，央行用利率平滑",
            "市场周期：情绪钟摆——过度恐惧 ↔ 过度贪婪，从不停留在合理位置",
        ],
        "master_view": {
            "marks": "钟摆理论：市场在悲观和乐观之间来回摆动，从不停留在合理位置",
            "buffett": "别人恐惧时贪婪，别人贪婪时恐惧——这是逆向投资的核心，但执行需要勇气",
            "munger": "宏观周期无法精准预测，但要知道我们大概在周期的哪个位置",
        },
        "controversy": "2022年有人说是'百年未有之大变局'，但达利欧会说：这不过是又一个债务周期的正常演绎。历史不会重复，但韵律会。上一次类似情况是1970-1980年代滞胀。",
        "case_study": "2008金融危机：达利欧在2007年就预警了债务危机，但没人信。霍华德·马克斯的备忘录在2007年8月写道：'到处都是钱，杠杆堆积，风险的定价低得荒唐。'——然后市场在2008年崩塌。周期感知不能预测时间，但能告诉你位置。",
        "quant_tip": "用巴菲特指标（股市总市值/GDP）判断市场整体估值水位，>150%通常意味着高估",
        "listener_exercise": "查查当前巴菲特指标是多少？是在历史高位还是低位？这告诉你什么？",
        "analogy": "经济周期像潮汐——你不需要预测每一波浪，但要知道自己是在涨潮还是退潮。",
    },

    "RISK-PARITY": {
        "id": "RISK-PARITY",
        "name": "风险的真相",
        "tags": ["master", "macro", "practice"],
        "category": "大师智慧",
        "dialogue_format": "thought",
        "hook": "为什么达利欧的全天候策略能穿越所有经济环境？因为它不是在预测，而是在对冲。",
        "description": "风险平价、资产配置、和为什么分散投资是对无知的保护",
        "teaching_points": [
            "风险平价 = 配置风险，而非配置金额；债券波动低，需要更大仓位才能与股票风险匹配",
            "达利欧的全天候策略：股票+债券+黄金+大宗商品，抗各种经济环境",
            "相关性会变——正常时期股债负相关，危机时期可能一起跌（流动性危机）",
        ],
        "master_view": {
            "dalio": "投资组合要像一顿饭——有蛋白质（股票）、碳水（债券）、蔬菜（黄金）",
            "lamy": "分散投资是对无知的保护——如果你知道自己买什么，就不需要分散",
        },
        "controversy": "2022年股债双杀——传统60/40组合亏损20%+。达利欧的全天候也回撤。为什么？因为所有资产的相关性在危机时刻都会变成1（一起跌）。没有完美的对冲，只有相对更好的配置。",
        "case_study": "达利欧全天候策略在2022年的表现：股票-20%，债券-15%，黄金-5%，大宗商品+20%。整体还是亏的，但比纯股票组合少亏很多。这说明分散配置的真正价值：在最坏的时候少亏，而不是在最好的时候多赚。",
        "quant_tip": "计算组合的Risk Parity，而非简单的60/40股票债券配置",
        "listener_exercise": "算算你的投资组合：如果股市跌30%，你的组合会跌多少？你的风险敞口和你想的一样吗？",
        "analogy": "船要稳，不同大小的帆配合——大风小帆，小风大帆，不是只用一种帆。投资也一样，不是all in一个资产，而是在不同环境中都能活下来。",
    },

    # ═══════════════════════════════════════════════════════
    # 💎 黄金专题
    # ═══════════════════════════════════════════════════════

    "GOLD": {
        "id": "GOLD",
        "name": "黄金的恐慌期权",
        "tags": ["gold", "macro", "master"],
        "category": "专题",
        "dialogue_format": "insight",
        "hook": "黄金不产生任何现金流，为什么还能涨？因为它是对冲'恐惧'的期权。",
        "description": "理解黄金的定价逻辑、实际利率关系、和为什么它是恐慌期权",
        "teaching_points": [
            "黄金是零现金流资产，DCF估值无效——它的价值来自不可侵蚀的共识",
            "黄金是实际利率的镜像：实际利率 = 名义利率 - 通胀预期",
            "1971年布雷顿森林体系崩塌后，黄金从货币之锚变成信心的最后防线",
        ],
        "master_view": {
            "buffett": "黄金是恐慌期权——它不产生任何东西，只是在别人恐惧时给你一点心理安慰",
            "dalio": "在债务周期尾部，黄金是对冲法定货币信用的终极工具",
        },
        "controversy": "2020年实际利率-1%，黄金却没创新高？为什么？因为美元也在走强，两个因素对冲。看黄金不能只看一个变量，要看实际利率+美元+地缘的三重博弈。",
        "case_study": "2022年黄金走势：俄乌冲突开打，黄金飙到2000；然后美联储激进加息，实际利率转正，黄金跌到1800。这告诉我们：地缘避险只是短期驱动，实际利率才是中期锚。",
        "quant_tip": "关注实际利率（Real Rate）和美元指数（DXY）的反向关系",
        "listener_exercise": "查查当前黄金价格和实际利率。如果明天美联储超预期降息，实际利率会怎么变？黄金可能怎么走？",
        "analogy": "黄金像是全球投资者的恐惧保险——平时付保费，出事才赔钱。但保费是机会成本，赔钱是心理安慰。",
    },

    # ═══════════════════════════════════════════════════════
    # 🟢 实战系列
    # ═══════════════════════════════════════════════════════

    "MARGIN-OF-SAFETY": {
        "id": "MARGIN-OF-SAFETY",
        "name": "安全边际",
        "tags": ["practice", "master", "foundation"],
        "category": "实战",
        "dialogue_format": "practical",
        "hook": "格雷厄姆的核心遗产：买股票不是买代码，是买折扣。",
        "description": "安全边际的概念、为什么它是投资成功的关键、和如何在实战中运用",
        "teaching_points": [
            "安全边际 = 内在价值 - 买入价格。内在价值是你的估计，买入价格是市场的出价",
            "安全边际的本质是对自己无知的保护——你的估值可能是错的",
            "格雷厄姆的清算价值法：股价低于净流动资产的2/3就是极好的安全边际",
        ],
        "master_view": {
            "buffett": "安全边际是投资的根本原则——用四毛买一块的东西，即使判断错误也不会亏太多",
            "graham": "安全边际永远不要太小，因为你的计算可能有误差",
        },
        "controversy": "成长股投资是否需要安全边际？传统派说不需要，因为成长股的价值在于未来。但巴菲特后来也买成长股，关键是你对成长的确定性有多高。确定性越高，安全边际的要求越低。",
        "case_study": "2008年金融危机中的安全边际机会：花旗银行股价从55美元跌到1美元。问题是：股价便宜不代表安全——如果公司破产，再便宜也没用。真正的安全边际是：你估算的内在价值比股价高很多，且公司不会破产。",
        "quant_tip": "用市净率（PB）和净流动资产（NCA）比较：PB < 1意味着股价低于净资产，但不一定安全，要看资产质量",
        "listener_exercise": "找你关注的一只股票，用格雷厄姆公式估算内在价值：内在价值 = EPS × (8.5 + 2×预期年增长率)。当前股价低于估算价值吗？安全边际多大？",
        "analogy": "安全边际就像桥梁的承重设计：设计承重50吨，实际只跑20吨的车。投资的margin of safety是同样的道理——给自己留余地，因为你的计算可能是错的。",
    },

    "MR-MARKET": {
        "id": "MR-MARKET",
        "name": "Mr. Market的寓言",
        "tags": ["practice", "master", "psychology"],
        "category": "实战",
        "dialogue_format": "practical",
        "hook": "格雷厄姆说市场是个躁郁症患者，每天报不同的价格。你要利用他，而不是被他利用。",
        "description": "格雷厄姆的Mr. Market寓言，和如何不被市场情绪左右",
        "teaching_points": [
            "Mr. Market每天给你报价，有时狂热，有时抑郁，但从不消失",
            "他每天报价是让你有机会买或卖，不是给你指令——你可以忽略他",
            "真正的问题是：你是否比他更了解这只股票的价值？如果不是，就别和他交易",
        ],
        "master_view": {
            "buffett": "你要学会利用市场的过度悲观或乐观，而不是被它左右",
            "marks": "钟摆理论：市场在悲观和乐观之间摆动，停在中间的时间最短",
        },
        "controversy": "被动投资 vs 主动投资：如果你相信Mr. Market总是过度反应，那主动投资有价值；如果你相信市场基本有效，那被动指数更好。两者都有大量证据支持——关键是你的能力和性格适合哪个。",
        "case_study": "2020年3月新冠暴跌：市场在一个月内暴跌34%。如果你相信Mr. Market是抑郁的，那时候就是最好的买入机会。但问题是：那时候没人知道底部在哪里。控制住不在最低点卖出的恐惧，比抄到底更重要。",
        "quant_tip": "用股债利差（Earnings Yield - 10Y Bond Yield）判断市场情绪：利差为正说明股票相对债券更有吸引力",
        "listener_exercise": "当你特别想卖出或买进一只股票时，问自己：这个决定是基于对价值的判断，还是基于当天市场的报价？如果是后者，Mr. Market正在影响你。",
        "analogy": "Mr. Market就像一个每天给你报价的合伙人——他有时疯狂报高价，有时抑郁报低价。你是他的主人，不是他的奴隶。他服务你，不是指挥你。",
    },

    # ═══════════════════════════════════════════════════════
    # 🔴 行为金融系列
    # ═══════════════════════════════════════════════════════

    "BEHAVIORAL": {
        "id": "BEHAVIORAL",
        "name": "投资心智的盲点",
        "tags": ["psychology", "master", "foundation"],
        "category": "行为金融",
        "dialogue_format": "debate",
        "hook": "芒格说：知道我会死在哪里，就永远不去那个地方。投资最大的敌人是自己的心智。",
        "description": "行为金融学核心：锚定效应、损失厌恶、可得性启发，和如何避免常见投资心理陷阱",
        "teaching_points": [
            "锚定效应：第一个遇到的价格会锚定你的判断——买入成本价成了'合理价位'的心理锚",
            "损失厌恶：亏损的痛苦是盈利快感的两倍——这就解释了为什么拿不住盈利却死守亏损",
            "可得性启发：最近发生的事会被高估概率——2020年疫情暴跌后，很多人觉得持有现金最安全，结果错失反弹",
        ],
        "master_view": {
            "munger": "人要避免变态精神状态——嫉妒、过度自怜、怨恨。投资成功的最大敌人是让自己变成最差的投资者",
            "buffett": "最大的投资错误不是买错了什么，而是别人恐惧时你也恐惧，别人贪婪时你也贪婪",
        },
        "controversy": "为什么均线金叉/死叉这么吸引人？因为它满足了你的控制幻觉——好像有一个简单规则可以预测市场。但统计上，所有技术指标长期都是负期望收益。",
        "case_study": "2022年A股4500点：很多人在5000点买入，在4000点割肉。为啥？因为4500点成了'便宜'的心理锚，4000点反而成了'危险'。这不是价值判断，是锚定效应在作祟。",
        "quant_tip": "用最大回撤（Max Drawdown）和回本需要的涨幅比较：亏损50%需要涨100%才能回本",
        "listener_exercise": "想想你过去的一次投资决策：有没有被'锚定'在某个价格？有没有因为'损失厌恶'而做出非理性决定？写下当时的心理状态。",
        "analogy": "投资心智的盲点就像眼镜上的污渍——你看市场是变形的，但你自己看不见。识别这些盲点，是投资成熟的第一步。",
    },

    "PSYCHOLOGY": {
        "id": "PSYCHOLOGY",
        "name": "芒格的25种心理倾向",
        "tags": ["psychology", "master"],
        "category": "行为金融",
        "dialogue_format": "debate",
        "hook": "芒格说：聪明人最大的愚蠢，是不知道自己为什么会愚蠢。",
        "description": "芒格25种误判心理学的核心洞察，和如何在投资中避免它们",
        "teaching_points": [
            "激励效应：永远先问'谁从这笔交易中赚钱'——利益不一致时，信息不可信",
            "社会认同：别人都在买/卖，你就想跟着——但法不责众不代表正确",
            "简单化倾向：'这件事太复杂了，我选择相信简单的解释'——这是危险的",
        ],
        "master_view": {
            "munger": "要学会逆向思考：与其想怎么成功，不如想怎么避免失败。列出25种让你投资失败的原因，然后远离它们。",
        },
        "controversy": "专业投资者也会犯这些心理错误吗？是的，而且更多。因为他们太聪明了，会用复杂的逻辑为自己的情绪化决策找理由。",
        "case_study": "LTCM崩盘1998：诺贝尔经济学奖得主+天才数学家组成的对冲基金，最后破产。原因？杠杆过高+极端概率事件（俄罗斯违约）+ 模型假设失效。激励机制让他们重仓，心理傲慢让他们忽视风险提示。",
        "quant_tip": "用持仓集中度检查过度自信：前十大持仓超过60%说明可能过度自信",
        "listener_exercise": "选择3个芒格的心理倾向例子，找出它们如何在你过去的投资决策中出现过。写下具体的触发情境。",
        "analogy": "芒格说：手里有锤子，看什么都像钉子。多元思维模型不是为了让你用所有工具，而是让你知道什么时候用什么工具。",
    },
}


def get_topic(topic_id: str) -> Optional[dict]:
    """获取知识点"""
    return TOPICS.get(topic_id)


def get_next_topic(current_topic_id: str = None, completed_topics: list = None) -> dict:
    """获取下一个推荐知识点（扁平化推荐，多样性优先）"""
    import random
    completed = completed_topics or []

    # 收集未完成的topic
    remaining = [tid for tid in TOPICS.keys() if tid not in completed]

    if not remaining:
        # 所有课程都学完了，随机选一个复习
        return TOPICS.get(random.choice(list(TOPICS.keys())))

    # 按标签分类，确保多样性
    tag_weights = {}
    for tid in remaining:
        topic = TOPICS[tid]
        tags = topic.get("tags", [])
        for tag in tags:
            tag_weights[tag] = tag_weights.get(tag, 0) + 1

    # 优先选择标签覆盖少的topic
    for tid in remaining:
        topic = TOPICS[tid]
        tags = topic.get("tags", [])
        # 给每个topic计算一个'多样性分数'
        uniqueness = sum(1 / tag_weights.get(tag, 1) for tag in tags)
        topic["_uniqueness_score"] = uniqueness

    # 选择多样性分数最高的
    remaining.sort(key=lambda t: TOPICS[t].get("_uniqueness_score", 0), reverse=True)

    # 从前3个多样性最高的随机选一个，增加随机性
    candidates = remaining[:3]
    chosen_id = random.choice(candidates)
    return TOPICS[chosen_id]


def get_topic_by_tag(tag: str) -> list:
    """获取某个标签的所有知识点"""
    return [t for t in TOPICS.values() if tag in t.get("tags", [])]


def recommend_topic(user_interests: list = None, completed_topics: list = None) -> dict:
    """推荐知识点（基于兴趣和多样性）"""
    import random

    completed = completed_topics or []
    interests = user_interests or []

    # 如果用户有关注主题，优先推荐相关的
    if interests:
        for tag in interests:
            matching = get_topic_by_tag(tag)
            for topic in matching:
                if topic["id"] not in completed:
                    return topic

    # 否则返回多样性最高的下一个
    return get_next_topic(completed_topics=completed)


def format_topic_summary(topic: dict) -> str:
    """格式化知识点摘要"""
    lines = []
    lines.append(f"# {topic['name']}")
    lines.append(f"**标签**: {', '.join(topic.get('tags', []))}")
    lines.append(f"**hook**: {topic.get('hook', '')}")
    lines.append(f"\n{topic.get('description', '')}")
    lines.append(f"\n## 核心要点:")
    for point in topic.get("teaching_points", []):
        lines.append(f"- {point}")
    return "\n".join(lines)


if __name__ == "__main__":
    print("=== 扁平化知识体系 ===")
    print(f"共 {len(TOPICS)} 个独立课程\n")

    # 按分类展示
    categories = {}
    for topic in TOPICS.values():
        cat = topic.get("category", "其他")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(topic["name"])

    for cat, topics in categories.items():
        print(f"\n{cat}:")
        for t in topics:
            print(f"  - {t}")

    print("\n\n=== 测试推荐 ===")
    topic = get_next_topic()
    print(f"推荐课程: {topic['name']}")
    print(f"Hook: {topic['hook']}")
