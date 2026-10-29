"""至多装满的 0-1 背包，保留完整 dp 表与回溯轨迹。仅用标准库。"""
import argparse
import hashlib
import json
from pathlib import Path


def solve(items, capacity, required=()):
    if type(capacity) is not int or capacity < 0:
        raise ValueError("容量须为非负整数")
    ids = [x['id'] for x in items]
    if len(set(ids)) != len(ids):
        raise ValueError("物品编号不能重复")
    for x in items:
        if type(x['weight']) is not int or x['weight'] <= 0:
            raise ValueError("重量须为正整数")
        if type(x['value']) is not int or x['value'] < 0:
            raise ValueError("重要度缺失或不是非负整数，请提供原始数据")
    required = set(required)
    if not required <= set(ids):
        raise ValueError("必投编号不存在")
    fixed = [x for x in items if x['id'] in required]
    remaining = capacity - sum(x['weight'] for x in fixed)
    if remaining < 0:
        raise ValueError("必投项目已超出容量，无可行解")
    optional = [x for x in items if x['id'] not in required]
    dp = [[0] * (remaining + 1) for _ in range(len(optional) + 1)]
    for i, x in enumerate(optional, 1):
        w, v = x['weight'], x['value']
        for c in range(remaining + 1):
            dp[i][c] = dp[i-1][c]
            if c >= w:
                dp[i][c] = max(dp[i][c], dp[i-1][c-w] + v)  # 0-1：取上一行，避免重复选
    c = remaining
    chosen = list(required)
    path = []
    for i in range(len(optional), 0, -1):
        x = optional[i-1]
        take = dp[i][c] != dp[i-1][c]  # 同分优先不取，保证输出可复现
        next_c = c - x['weight'] if take else c
        path.append({'from': [i, c], 'to': [i-1, next_c],
                     'id': x['id'], 'take': take, 'value': dp[i][c]})
        if take:
            chosen.append(x['id'])
        c = next_c
    return {'capacity': capacity, 'required': sorted(required),
            'value': dp[-1][-1] + sum(x['value'] for x in fixed),
            'chosen': sorted(chosen), 'dp_last_row': dp[-1], 'trace': path}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=Path(__file__).with_name('classroom_items.json'))
    parser.add_argument('--values', type=int, nargs=5, help='按原始顺序提供五个重要度，不改数据文件')
    parser.add_argument('--required', type=int, nargs='+', default=[1], help='必投编号，默认帐篷')
    args = parser.parse_args()
    raw = args.data.read_bytes()
    items = json.loads(raw.decode('utf-8-sig'))
    if args.values:
        if len(items) != 5:
            parser.error('--values 只适用于五件物品')
        items = [dict(x, value=v) for x, v in zip(items, args.values)]
    try:
        results = [solve(items, 1000), solve(items, 800), solve(items, 1000, args.required)]
    except ValueError as e:
        parser.exit(2, str(e) + '\n')
    output = Path(__file__).with_name('results')
    output.mkdir(exist_ok=True)
    evidence = {'data_sha256': hashlib.sha256(raw).hexdigest(),
                'values_override': args.values, 'items_used': items, 'results': results}
    (output / 'knapsack.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# 背包运行结果', '', '采用至多装满；同分优先不取。', '']
    for r in results:
        title = f"容量 {r['capacity']}，必投 {r['required']}"
        print(title, '最优值', r['value'], '组合', r['chosen'])
        lines += [f'## {title}', '', f"最优值：{r['value']}；组合：{r['chosen']}。", '',
                  'dp 最后一行（数组下标就是容量，包含所有容量）：', '',
                  '```text', json.dumps(r['dp_last_row']), '```', '',
                  '| 当前格 | 值 | 物品 | 决策 | 前驱格 |', '|---|---|---|---|---|']
        for t in r['trace']:
            lines.append(f"| {t['from']} | {t['value']} | {t['id']} | {'取' if t['take'] else '不取'} | {t['to']} |")
        lines.append('')
    drop = results[0]['value'] - results[1]['value']
    lines += [f'预算由 1000 降到 800，最优值下降 {drop}。容量减少使可行组合集合缩小，最优值不能增加；选中组合和剩余空间见上表。']
    (output / 'analysis.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    main()
