# 第六次作业 贪心与动态规划

Python 3，全部使用标准库。采用至多装满，物品编号从 1 开始。

```powershell
python coin.py
python -m unittest -v
python knapsack.py
python knapsack.py --help
```

## 课堂数据与输出

教师补充的课堂截图已保存为 evidence/classroom_scores.png。重量为 [300,200,350,400,250]，重要度为 [90,60,115,120,80]，保存在 classroom_items.json，作为程序默认输入。

原 items.json 的空值及 ranked_items.json 的临时名次分保留用于追溯，不再用于课堂验收。原始 Word 材料没有改动。

运行 python knapsack.py 即可计算容量1000、容量800、容量1000且必投帐篷三种情况；结果分别为315、255、290。默认必投编号1，可用 --required 改选。

结果写入 results/knapsack.json 与 results/analysis.md，包含输入哈希、实际使用数据、完整dp最后一行、逐步回溯和预算对比。按每1g一列精确计算350g和250g的物品重量。

## 验收位置

- `coin.py`：`dp[c] = dp[c - coin] + 1` 是凑硬币填表核心。
- `knapsack.py`：`dp[i-1][c-w] + v` 是 0-1 背包核心；回溯时比较相邻行。
- 必投：先扣除必投重量，再求剩余物品的 0-1 背包，最后加回必投价值；超重直接报告无解。
- `test_algorithms.py`：独立枚举所有 32 个子集，核验随机样本的最优值、组合、容量、必投及无解处理。
- `research.md`：三项独立研究。
- `progress.md`：进度自查与实际限制。
- `ai_usage.md`：四问和真实验证记录。

## TRAE 与提交

此前排序赋分仅是临时建模；已用教师截图的实际分数替代，并通过32个子集穷举复核全部三种场景。

已实际使用 TRAE Agent 读取代码、执行 python coin.py、python -m unittest -v、python knapsack.py，并生成 trae_review.md。5项测试通过，三场景315、255、290均复核通过；完成截图见 evidence/trae_completed.png。最初代码由Codex编写，本轮审查与终端验证由TRAE完成。
