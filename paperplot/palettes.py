"""语义科研调色板。

借鉴自 figures4papers (ChenLiu-1996) 的 house style，将颜色与语义角色绑定，
使"本文方法 / 改进 / 对比 / 基线"在不同图表间保持一致的视觉编码。

两类色：
- 标量角色色 (SEMANTIC_PALETTE / SEMANTIC_PALETTE_LIST)：单一角色 -> 单一 hex，
  可直接传给 `Plotter.set_palette` / `bind_color`，或写入 .mplstyle 的 axes.prop_cycle。
- 色阶 band (SEMANTIC_BANDS)：浅 -> 深的同色系列，用于 alpha 不够表达层次时
  (如多组对比的浅/中/深)，或作为 ablation/分组场景的候选色阶。
"""

# 标量角色：单一语义 -> 单一 hex。
# 蓝 = 本文方法 / 关键结果；绿 = 改进 / 正向变体；红 = 对比 / 对照；
# 灰 = 背景 / 参考类别；金 = 单点高亮。
SEMANTIC_PALETTE = {
    "proposed": "#0F4D92",
    "improvement": "#8BCF8B",
    "contrast": "#B64342",
    "baseline": "#CFCECE",
    "highlight": "#FFD700",
}

# 扁平 list，用于 prop_cycle / set_palette。
# 顺序与 SEMANTIC_PALETTE 的插入顺序一致。
SEMANTIC_PALETTE_LIST = list(SEMANTIC_PALETTE.values())

# 色阶 band：浅 -> 深。完整照搬 figures4papers design-theory.md 的 band 定义。
SEMANTIC_BANDS = {
    "green": ["#DDF3DE", "#AADCA9", "#8BCF8B"],
    "red": ["#F6CFCB", "#E9A6A1", "#B64342"],
    "blue": ["#3775BA", "#0F4D92"],
}

__all__ = ["SEMANTIC_PALETTE", "SEMANTIC_PALETTE_LIST", "SEMANTIC_BANDS"]
