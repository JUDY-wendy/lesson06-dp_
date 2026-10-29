"""使用独立穷举核验 DP，不以缺失的课堂数据伪造验收结果。"""
import itertools
import random
import unittest
import json
from pathlib import Path
from coin import coin_dp, coin_greedy
from knapsack import solve


def brute(items, capacity, required=()):
    best = -1
    for bits in itertools.product((0, 1), repeat=len(items)):
        chosen = [x for x, bit in zip(items, bits) if bit]
        if not set(required) <= {x['id'] for x in chosen}:
            continue
        if sum(x['weight'] for x in chosen) <= capacity:
            best = max(best, sum(x['value'] for x in chosen))
    return best


class Checks(unittest.TestCase):
    def test_classroom_data(self):
        items = json.loads(Path(__file__).with_name('classroom_items.json').read_text(encoding='utf-8'))
        for capacity, required in [(1000, ()), (800, ()), (1000, (1,))]:
            result = solve(items, capacity, required)
            self.assertEqual(result['value'], brute(items, capacity, required))
        result = solve(items, 1000)
        self.assertEqual(result['value'], 315)
        self.assertEqual(result['chosen'], [3, 4, 5])

    def test_coin_checkpoint(self):
        self.assertEqual(coin_greedy([1, 5, 11], 15), (5, [11, 1, 1, 1, 1]))
        self.assertEqual(coin_dp([1, 5, 11], 15), (3, [5, 5, 5]))

    def test_coin_boundaries(self):
        self.assertEqual(coin_dp([2], 0), (0, []))
        self.assertEqual(coin_dp([2], 3), (None, []))
        self.assertEqual(coin_greedy([3, 4], 6), (None, []))
        self.assertEqual(coin_dp([3, 4], 6), (2, [3, 3]))
        with self.assertRaises(ValueError):
            coin_dp([0, 1], 3)

    def test_knapsack_against_enumeration(self):
        rng = random.Random(6)
        for case in range(80):
            items = [dict(id=i+1, weight=rng.randint(1, 12), value=rng.randint(0, 30)) for i in range(5)]
            capacity = rng.randint(0, 35)
            for required in ((), (1,)):
                expected = brute(items, capacity, required)
                if expected < 0:
                    with self.assertRaises(ValueError):
                        solve(items, capacity, required)
                    continue
                result = solve(items, capacity, required)
                self.assertEqual(result['value'], expected)
                chosen = [x for x in items if x['id'] in result['chosen']]
                self.assertEqual(sum(x['value'] for x in chosen), expected)
                self.assertLessEqual(sum(x['weight'] for x in chosen), capacity)
                self.assertEqual(len(set(result['chosen'])), len(result['chosen']))
                self.assertTrue(set(required) <= set(result['chosen']))

    def test_missing_data(self):
        with self.assertRaises(ValueError):
            solve([dict(id=1, weight=300, value=None)], 1000)
        self.assertEqual(solve([], 0)['value'], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
