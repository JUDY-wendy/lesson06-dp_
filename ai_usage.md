# AI 使用记录

## 关键指令原文

教师最初指令：

> 你是一名优秀的学生我是你的老师，现在请你阅读"D:\zyl66\人工智能程序设计与实践\第六次作业"，并利用trae完成本节课作业

教师补充：

> 从最重要到不重要排列：食物、睡袋、帐篷、炉具、水具     "C:\Users\zyl66\Desktop\编程相关\TraeCode CN.lnk"

发送给 TRAE 的完整指令由 trae_prompt.txt 与命令中补充组成：

> 请按附加指令审查当前作业并运行验证。教师已补充重要度排序，ranked_items.json 按名次赋分为3、2、4、5、1，请运行 python coin.py、python -m unittest -v、python knapsack.py --data ranked_items.json。不要声称复现315，不修改原始数据，不自动提交远端。将实际审查与运行结果写入 trae_review.md。

## 四问格式

- 角色：教师委托完成课堂实验，AI 提供 Python 算法实现与验证；学生身份信息未提供。
- 背景：阅读三份第六次课 Word 材料，发现重要度列为空，随后收到排序与 TRAE 快捷方式。
- 任务：完成凑硬币、背包回溯、预算800、必投约束、完整末行与回溯报告，以及三项研究题。
- 约束：标准库、中文注释、至多装满、原材料不改；排序转换为名次分必须披露；不伪造315、学生手动验证或 push。

## 实际工具与验证

代码与初稿由 Codex 编写。通过快捷方式定位 `D:\LeStoreDownload\TRAE\Trae CN.exe`，调用其 trae-cn.cmd 打开本项目并通过 chat --mode agent 发送审查请求；启动命令退出码为0，但后续未检测到持续运行的 TRAE 进程，也未生成审查文件。启动与发送不代表已经收到 TRAE 审查结果，只有实际产生的 trae_review.md 才能作为后续执行证据。

Codex 已实际执行：

```text
python coin.py
贪心：(5, [11, 1, 1, 1, 1])
动规：(3, [5, 5, 5])

python -m unittest -v
Ran 4 tests ... OK

python knapsack.py --data ranked_items.json
容量 1000，必投 [] 最优值 11 组合 [2, 3, 4]
容量 800，必投 [] 最优值 9 组合 [3, 4]
容量 1000，必投 [1] 最优值 10 组合 [1, 2, 4]
```

验证方式：独立遍历32个子集，核对80组固定随机样本的普通/必投最优值、返回组合、重量与无解；测试零金额、不可凑金额、非法面额、空物品表、缺失重要度。输入哈希和实际使用值附在 results/knapsack.json。

学生本人验证：尚未记录。教师提供的三个原始 Word 文件未改动，哈希见 source_hashes.json。

## 教师补充截图后的更新

关键指令原文：“那我给你重要度分数”，附课堂登山背包截图。识别值为帐篷90、炉具60、睡袋115、食物120、水具80，截图保存于 evidence/classroom_scores.png。

此前名次赋分输出仅为历史记录；当前验收改用 classroom_items.json，程序默认读取此文件。Codex实际执行 python knapsack.py 和 python -m unittest -v，输出如下：

```text
容量1000，无必投：315，[3,4,5]
容量800，无必投：255，[2,3,5]
容量1000，必投帐篷：290，[1,4,5]
Ran 5 tests ... OK
```

新增课堂数据回归测试，将三种结果分别与全部32个子集的穷举最优值比较，并断言课堂315和[3,4,5]。原Word材料保持不变。此轮由Codex运行，未新增TRAE完成证据。

## TRAE 实际使用完成记录

2026-10-29重新排查后，TRAE作业窗口成功运行。通过窗口输入任务，先在Chat模式读取代码，再切换Agent模式实际执行。最终关键指令原文：

> 现已切换Agent模式，请实际调用终端执行python coin.py、python -m unittest -v、python knapsack.py，工作目录为当前lesson06-dp。三条命令成功后创建trae_review.md记录你实际执行的原始输出与结论。不要push，不改原始材料。

TRAE已生成trae_review.md，记录三条命令及输出，结果为硬币5枚与3枚、背包315/255/290、5项测试通过。Codex读取该文件核对后，在TRAE窗口点击全部保留。完成界面保存为evidence/trae_completed.png。此前“尚无TRAE完成证据”描述为历史状态，以本段及最新进度报告为准。初稿由Codex编写，TRAE承担本轮实际代码审查与运行验证；该过程仍不等同于学生本人手动验证。
