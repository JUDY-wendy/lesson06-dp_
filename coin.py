"""Step1：贪心反例与动态规划，直接运行 python coin.py。"""


def validate(coins, amount):
    if type(amount) is not int or amount < 0:
        raise ValueError("金额须为非负整数")
    coins = list(coins)
    if not coins or any(type(c) is not int or c <= 0 for c in coins):
        raise ValueError("面额须为正整数")
    return sorted(set(coins), reverse=True)


def coin_greedy(coins, amount):
    coins = validate(coins, amount)
    chosen = []
    for coin in coins:
        count, amount = divmod(amount, coin)
        chosen.extend([coin] * count)
    return (len(chosen), chosen) if amount == 0 else (None, [])


def coin_dp(coins, amount):
    coins = validate(coins, amount)
    dp = [0] + [float("inf")] * amount
    last = [0] * (amount + 1)
    for c in range(1, amount + 1):
        for coin in coins:
            if coin <= c and dp[c - coin] + 1 < dp[c]:
                dp[c] = dp[c - coin] + 1  # 填表核心：最后一枚硬币之前的最优值加一
                last[c] = coin
    if dp[amount] == float("inf"):
        return None, []
    chosen = []
    c = amount
    while c:
        chosen.append(last[c])
        c -= last[c]
    return dp[amount], chosen


if __name__ == "__main__":
    print("面额 [1,5,11]，金额 15")
    print("贪心：", coin_greedy([1, 5, 11], 15))
    print("动规：", coin_dp([1, 5, 11], 15))
