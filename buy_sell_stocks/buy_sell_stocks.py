from typing import List
import time
import tracemalloc
import random
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
 
sys.setrecursionlimit(100000)

class Solution:
    def recurse(self, i:int, buy:int, prices:List[int]) -> int:
        if i == len(prices) : return 0
        
        if buy :
            profit = max(-prices[i] + self.recurse(i+1,0,prices), self.recurse(i+1,1,prices))
        else :
            profit = max(prices[i] + self.recurse(i+1,1,prices), self.recurse(i+1,0,prices))
        return profit

    def memo(self,i:int,buy:int,prices:List[int],dp:List[List[int]]) -> int:
        if i == len(prices) : return 0
        if dp[i][buy] != -1 : return dp[i][buy]
        if buy :
            profit = max(-prices[i] + self.memo(i+1,0,prices,dp), self.memo(i+1,1,prices,dp))
        else :
            profit = max(prices[i] + self.memo(i+1,1,prices,dp), self.memo(i+1,0,prices,dp))
        dp[i][buy] = profit
        return profit
    
    def tabulation(self, prices: List[int]) -> int:
        n = len(prices)
        dp = [[0]*2 for _ in range(n+1)]
        
        for i in range(n-1,-1,-1):
            for buy in range(2):
                if buy :
                    profit = max(-prices[i] + dp[i+1][0], dp[i+1][1])
                else :
                    profit = max(prices[i] + dp[i+1][1], dp[i+1][0])
                dp[i][buy] = profit
        return dp[0][1]

    def fourVariable(self, prices: List[int]) -> int:
        n = len(prices)
        aheadBuy = aheadNotBuy = 0
        for i in range(n-1,-1,-1):
            for buy in range(2):
                curBuy = max(-prices[i] + aheadNotBuy, aheadBuy)
                curNotBuy = max(prices[i] + aheadBuy, aheadNotBuy)
                aheadBuy = curBuy
                aheadNotBuy = curNotBuy
        return curBuy


def main():
    sol = Solution()
    sizes = list(range(1, 30))
 
    approaches = [
        ("Recursive",   lambda p: sol.recurse(0, 1, p),                               "#e24b4a"),
        ("Memoization", lambda p: sol.memo(0, 1, p, [[-1]*2 for _ in range(len(p))]), "#378add"),
        ("Tabulation",  lambda p: sol.tabulation(p),                                  "#1D9E75"),
        ("4-Variable",  lambda p: sol.fourVariable(p),                                "#BA7517"),
    ]
    
    results = {name: [] for name, _, _ in approaches}
    
    for n in sizes:
        prices = [random.randint(1, 1000) for _ in range(n)]
        for name, func, _ in approaches:
            start = time.perf_counter()
            func(prices)
            end = time.perf_counter()
            results[name].append((end - start) * 1000)
        print(f"n={n} done")
    
    mem_results = {name: [] for name, _, _ in approaches}

    for n in sizes:
        prices = [random.randint(1, 1000) for _ in range(n)]
        for name, func, _ in approaches:
            tracemalloc.start()
            func(prices)
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            mem_results[name].append(peak / 1024)
        print(f"mem n={n} done")
    
    offset = max(results["Recursive"]) * 0.08

    results_display = {
        "Recursive":   results["Recursive"],
        "Memoization": [t + offset for t in results["Memoization"]],
        "Tabulation":  [t + offset * 0.5 for t in results["Tabulation"]],
        "4-Variable":  [t + offset * 0.25 for t in results["4-Variable"]],
    }
    
    # ── plot ──────────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#cccccc")
    ax.spines["bottom"].set_color("#cccccc")
    ax.tick_params(colors="#555555", labelsize=9)
    ax.yaxis.label.set_color("#555555")
    ax.xaxis.label.set_color("#555555")
    
    for name, _, color in approaches:
        ax.plot(sizes, results_display[name], marker="o", markersize=3, linewidth=1.8, label=name, color=color)
    
    ax.set_title("Runtime — all 4 approaches (n = 1 to 30)\n(memo/tab/4var offset for visibility)", fontsize=12)
    ax.set_xlabel("n (array size)")
    ax.set_ylabel("time (ms)")
    ax.legend(fontsize=9)
    
    plt.tight_layout()
    plt.savefig("runtime_n30.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("Saved to runtime_n30.png")
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#cccccc")
    ax2.spines["bottom"].set_color("#cccccc")
    ax2.tick_params(colors="#555555", labelsize=9)
    ax2.yaxis.label.set_color("#555555")
    ax2.xaxis.label.set_color("#555555")

    for name, _, color in approaches:
        ax2.plot(sizes, mem_results[name], marker="o", markersize=3, linewidth=1.8, label=name, color=color)

    ax2.set_title("Memory — all 4 approaches (n = 1 to 30)", fontsize=12)
    ax2.set_xlabel("n (array size)")
    ax2.set_ylabel("peak memory (KB)")
    ax2.legend(fontsize=9)

    plt.tight_layout()
    plt.savefig("memory_n30.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("Saved to memory_n30.png")

if __name__ == "__main__":
    main()
                    