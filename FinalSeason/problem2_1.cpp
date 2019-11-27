/*挑战任务
A 国的国土由若干个城市组成，这些城市分布在若干个岛屿上，城市之间由一些 双向 道路连接，并且 互相联通 。如果一条道路跨越了两个岛屿，那么这条道路就是一座桥。

现在你有一张 A 国的地图，地图上标明了 A 国所有的城市和道路，但并未标明岛屿。

其中 A 国的桥满足了以下条件：如果将一条道路 删去之后，存在两个城市 不再联通，那么这条道路 一定是 一座桥。

现在，请你回答以下两个问题：

A 国一共有多少座桥；

从任一城市到另外任一城市 最多 需要经过多少座桥。

编程要求
补全右侧代码区中的pair<int, int> solve(int n, const vector<pair<int, int>> &edges)函数，完成挑战任务中提出的问题。

说明：函数的返回结果中，first成员是桥的个数，second成员是最多需要经过桥的座数。

如果需要，你可以在solve函数外添加其它代码，但是 不要 改变Solver类的名字以及solve函数的定义。

函数参数说明如下：

int n：A 国城市的个数，编号从1到N。（1 <= N <= 100000）

vector<pair<int, int>> edges：A 国所有的道路，每个pair<int, int>的两个成员变量first和second表示道路连接的两个城市的编号。道路总数为M。（1 <= M <= 500000）。

测试说明
样例1输入：

n = 5
edges = {
  {1, 2},
  {2, 3},
  {3, 4},
  {4, 2},
  {4, 5}
};
样例1输出：2 2

样例1说明：{1, 2}和{4, 5}是桥，因此从城市1到城市5需要经过两个桥。

样例2输入：

n = 5
edges = {
  {1, 2},
  {2, 3},
  {3, 4},
  {4, 5},
  {5, 1}
};
样例2输出：0 0

样例2说明：样例2中没有桥，删除任意一条道路，都可与其他城市联通，因此不需要经过桥。*/

#ifndef __SOLVER_H__
#define __SOLVER_H__

#include <bits/stdc++.h>

using namespace std;

const int MAXN = 101000;
const int MAXM = 1010000;
struct Edge {
    int to, next;
    bool cut;
} edge[MAXM];
//缩点用 只用于tarjan板子
int head[MAXN], tot;
int Low[MAXN], DFN[MAXN], Stack[MAXN];
int Index, top;
bool Instack[MAXN];
bool cut[MAXN];
int add_block[MAXN];
int bridge;
//建图用
int c[MAXN], cnt;
//dp用
int tc, hc[MAXN], vc[MAXM], nc[MAXM];
int dp[MAXN], dpv[MAXN];
int ans;

class Solver {
public:
    
    void addedge(int u, int v) {
        edge[tot].to = v;
        edge[tot].next = head[u];
        edge[tot].cut = false;
        head[u] = tot++;
    }
    void Tarjan(int u, int pre) {
        int v;
        Low[u] = DFN[u] = ++Index;
        Stack[top++] = u;
        Instack[u] = true;
        int son = 0;
        int pre_cnt = 0;
        for (int i = head[u]; i != -1; i = edge[i].next) {
            v = edge[i].to;
            if (v == pre) continue;
            if (!DFN[v]) {
                son++;
                Tarjan(v, u);
                if (Low[u] > Low[v]) 
                    Low[u] = Low[v];
                if (Low[v] > DFN[u]) {
                    bridge++;
                    edge[i].cut = true;
                    edge[i ^ 1].cut = true;
                }
                if (u != pre && Low[v] >= DFN[u]) {
                    cut[u] = true;
                    add_block[u]++;
                }
            } else if (Low[u] > DFN[v])
                Low[u] = DFN[v];
        }
        if (u == pre && son > 1)cut[u] = true;
        if (u == pre)add_block[u] = son - 1;
        Instack[u] = false;
        top--;
    }
    void init() {
        cnt = tc = tot = ans = 0;
        memset(head, -1, sizeof(head));
        memset(hc, -1, sizeof(hc));
        memset(dp, 0, sizeof(dp));
        memset(dpv, 0, sizeof(dpv));
    }
    void init1(int n) {
        Index = top = bridge = 0;
        memset(DFN, 0, sizeof(DFN));
        memset(Instack, false, sizeof(Instack));
        memset(cut, false, sizeof(cut));
        memset(add_block, 0, sizeof(add_block));
        for (int i = 1; i <= n; i++)
            if (!DFN[i]) Tarjan(i, i);
    }
    //建图
    void dfs(int x) {
        c[x] = cnt;
        for (int i = head[x]; i != -1; i = edge[i].next) {
            int y = edge[i].to;
            if (c[y] || edge[i].cut) continue;
            dfs(y);
        }
    }
    void treeDP(int x) {
        dpv[x] = 1;
        for (int i = hc[x]; i != -1; i = nc[i]) {
            int ty = vc[i];
            if (dpv[ty]) continue;
            treeDP(ty);
            ans = max(ans, dp[x] + dp[ty] + 1);
            dp[x] = max(dp[x], dp[ty] + 1);
        }
    }

    void makec(int n){
        for (int i = 1; i <= n; i++) {
            if (!c[i]) {
                cnt++;
                dfs(i);
            }
        }
        for (int i = 0; i < tot; i++) {
            int x = edge[i^1].to, y = edge[i].to;
            if (c[x] == c[y])
                continue;
            vc[tc] = c[y];
            nc[tc] = hc[c[x]];
            hc[c[x]] = tc++;
        }
    }
    pair<int, int> solve(int n, const vector<pair<int, int>> &edges) {
        /********** Begin **********/
        init();
        for (int i = 0;i < edges.size();i++) {
            int u = edges[i].first, v = edges[i].second;
            addedge(u, v);
            addedge(v, u);
        }
        init1(n);
        makec(n);
        treeDP(1);
        pair<int, int> aans;
        aans.first = cnt-1;
        aans.second = ans;
        return aans;
        /********** End **********/
    }
};

#endif