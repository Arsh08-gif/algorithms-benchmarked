from typing import List
import time
import random
import matplotlib.pyplot as plt

class Solution:
    def rec(self, i:int, w:int, val:List[int], wt:List[int]) -> int:
        if w == 0: return 0
        if i ==0 : 
            if wt[i] <= w : return val[i]
            else : return 0
        not_take = 0 + self.rec(i-1, w, val,wt)
        take = float('-inf')
        if wt[i] <= w:
            take = val[i] + self.rec(i-1,w-wt[i],val,wt)
        return max(take , not_take)
    
    def rec_memo(self, i:int, w:int, val:List[int], wt:List[int],dp:List[List[int]]) -> int:
        if w == 0: return 0
        if i ==0 : 
            if wt[i] <= w : return val[i]
            else : return 0
        if dp[i][w] != -1 : return dp[i][w]
        not_take = 0 + self.rec_memo(i-1, w, val,wt,dp)
        take = float('-inf')
        if wt[i] <= w:
            take = val[i] + self.rec_memo(i-1,w-wt[i],val,wt,dp)
        dp[i][w] = max(take, not_take)
        return max(take , not_take)

    def knapsack_recursive(self,W,val,wt) -> int:
        # RECURSION TC: 2^N
        n = len(val)
        return self.rec(n-1,W,val,wt)
    
    def knapsack_memo(self,W,val,wt) -> int:
        # RECURSION WITH MEMOIZATION : TC: O(N * W) , SC : O(N*W) + O(N) {STACK OVERHEAD}
        n = len(val)
        dp = [[-1]*(W+1) for _ in range(n)]
        return self.rec_memo(n-1,W,val,wt,dp)
    
    def knapsack_tabulation(self,W,val,wt) -> int:
        n = len(val)
        
        # 1. TABULATION WITH 2D-ARRAY : SC : O( N * W )
        # dp = [[0]*(W+1) for _ in range(n)]
        # for i in range(n):
        #     dp[i][0] = 0
        # if wt[0] <= W: 
        #     dp[0][wt[0]] = val[0]
        
        # for i in range(1,n):
        #     for w in range(1,W+1):
        #         take = float('-inf')
        #         if wt[i] <= w:
        #             take = val[i] + dp[i-1][w-wt[i]]
        #         not_take = dp[i-1][w]
        #         dp[i][w] = max(take, not_take)
        # return dp[n-1][W]
    
        # 2. TABULATION WITH 2 ARRAYS : SC : O(2W)
        # prev = [0]*(W+1)
        # if wt[0] <= W: 
        #     prev[wt[0]] = val[0]
        
        # for i in range(1,n):
        #     cur = [0]*(W+1)
        #     for w in range(1,W+1):
        #         take = float('-inf')
        #         if wt[i] <= w:
        #             take = val[i] + prev[w-wt[i]]
        #         not_take = prev[w]
        #         cur[w] = max(take, not_take)
        #     prev = cur
        # return prev[W]
        
        # 3. TABULATION WITH 1 ARRAY : UPDATES PREV ARRAY ITSELF - SC : O(W)
        prev = [0]*(W+1)
        if wt[0] <= W: 
            prev[wt[0]] = val[0]
        
        for i in range(1,n):
            for w in range(W,-1,-1):
                take = float('-inf')
                if wt[i] <= w:
                    take = val[i] + prev[w-wt[i]]
                not_take = prev[w]
                prev[w] = max(take, not_take)
        return prev[W]

        
        
def main():
    # INTITAL TESTING
    # W = 5
    # val = [10, 40, 30, 50]
    # wt = [5, 4, 2, 3]
    # sol = Solution()
    # start = time.time()
    # max_res = sol.knapsack(W,val,wt)
    # end = time.time()
    # print(f'ans : {max_res}')
    # print(f'Time taken by algorithm : {end - start : .6f} sec')
    
    # CHARTS
    
    sizes = [3, 5, 10, 15, 20, 25, 30]
    recursive_times = []
    memo_times = []
    tab_times = []

    for n in sizes:
        val = [random.randint(1, 100) for _ in range(n)]
        wt  = [random.randint(1, 100) for _ in range(n)]
        W   = 500
        sol = Solution()
        
        start = time.time()
        sol.knapsack_recursive(W, val, wt)
        recursive_times.append(time.time() - start)
        
        start = time.time()
        sol.knapsack_memo(W,val,wt)
        memo_times.append(time.time() - start)
        
        start = time.time()
        sol.knapsack_tabulation(W,val,wt)
        tab_times.append(time.time() - start)
    
    # TIME COMPLEXITY CHARTS
    plt.figure(figsize=(10, 6))
    offset = 0.2
    memo_display = [t + offset for t in memo_times]
    tab_display  = [t + offset * 0.5 for t in tab_times]
    plt.plot(sizes, recursive_times, label='Recursive O(2^n)', color='steelblue')
    plt.plot(sizes, memo_display,    label='Memoization O(n*W) (offset for visibility)', linestyle='--', color='orange')
    plt.plot(sizes, tab_display,     label='Tabulation O(n*W) (offset for visibility)', color='green')
    plt.xlabel('Number of Items (n)')
    plt.ylabel('Time (seconds)')
    plt.title('0/1 Knapsack - Time Complexity Comparison')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('time_comparison.png', dpi=150)
    plt.show()
    plt.close()
    print("Time chart done, starting space chart...")  # add this
        
    # SPACE COMPARISON CHARTS
    n_values = range(1, 10001)  # number of items
    W = 1000  # fixed knapsack capacity
    recursive       = [n for n in n_values]              # O(n) stack
    memoization     = [(n * W) + n + 100 for n in n_values]  # O(n×W) + stack | tiny offset to show both
    tabulation      = [(n * W) for n in n_values]          # O(n×W)
    space_opt_2W    = [(2 * W) for _ in n_values]          # O(2W) - two arrays
    space_opt_1W    = [(W) for _ in n_values]              # O(W) - one array

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    # Left: Recursive + Memoization
    ax1.plot(n_values, recursive,    label='Recursive O(n)', color='steelblue')
    ax1.plot(n_values, memoization,  label='Memoization O(n×W)', linestyle='--', color='orange')
    ax1.set_title('Recursive vs Memoization')
    ax1.set_xlabel('Number of Items (n)')
    ax1.set_ylabel('Space Units')
    ax1.legend()
    ax1.grid(True)

    # Right: Tabulation + Space Optimized 2W + Space Optimized W
    space_offset = n_values[-1] * W * 0.03  # 5% of max tabulation value
    ax2.plot(n_values, tabulation,label='Tabulation O(n×W)', color='green')
    ax2.plot(n_values, [v + space_offset * 2 for v in space_opt_2W],label='Space Optimized O(2W) (offset)', color='red')
    ax2.plot(n_values, [v + space_offset for v in space_opt_1W],label='Space Optimized O(W) (offset)', color='purple')
    ax2.set_title('Tabulation vs Space Optimized')
    ax2.set_xlabel('Number of Items (n)')
    ax2.set_ylabel('Space Units')
    ax2.legend()
    ax2.grid(True)

    plt.suptitle('0/1 Knapsack - Space Complexity Comparison', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('space_comparison.png', dpi=150)
    plt.show()
    plt.close()
    
    

if __name__ == "__main__":
    main()
