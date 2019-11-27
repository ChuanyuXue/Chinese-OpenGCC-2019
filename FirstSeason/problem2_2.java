/*
任务描述
A 国由N个城市和M条 单向 道路组成。这些城市划分成了若干个联邦，如果两个城市之间可以通过这些道路相互可达，那么这两个城市就属于同一个联邦。

对于每一条道路 (u_i, v_i)(u 
i
​	
 ,v 
i
​	
 )，其运输成本为 w_iw 
i
​	
 。如果一条道路连接的两个城市属于 同一个联邦，那么这条道路则 不需要 运输成本。

现在，作为 A 国的国王，你正在考虑交通运输对国家经济的影响。请求出在所有城市间的运输路线中，运输 成本最大 的是多少。（一条运输路线的总成本为其包含的所有道路的运输成本之和）

编程要求
补全右侧代码区中的int solver(int n, List<Edge> edges)函数，完成返回最长路线运输成本值。

如果需要，你可以在solver函数外添加其它代码，但是 不要 改变Task类的名字、solver函数的定义以及Edge类的实现。

函数参数说明如下：

int n：城市的个数，城市编号从1到N。（1 <= N <= 100000）
List<Edge> edges：表示图中的边，每个Edge对象有三个属性，表示从u到v有一条运输成本为w的单向道路。边总数为M。（1 <= M <= 200000，1 <= u，v <= N，1 <= w <= 1000）
测试说明
下面给出三组测试样例供参考：

样例1输入：

n = 5
edges = {
  {1, 2, 1},
  {2, 3, 1},
  {3, 4, 1},
  {4, 2, 1},
  {4, 5, 1}
};
样例1输出：

2

详细说明：样例1中有3个联邦，第一个联邦是城市1，第二个联邦是城市2、3、4，第三个联邦是城市5。城市2、3、4之间的道路不需要成本，因此最长的运输路线是1 -> 2 -> 3 -> 4 -> 5，成本为2。

样例2输入：

n = 5
edges = {
  {1, 2, 1},
  {2, 3, 1},
  {3, 4, 1},
  {4, 5, 1},
  {3, 5, 1}
};
样例2输出：

4

详细说明：样例2中没有联邦。最长的运输路线为1 -> 2 -> 3 -> 4 -> 5，成本为4。

样例3输入：

n = 5
edges = {
  {1, 2, 1},
  {1, 3, 1},
  {1, 4, 1},
  {1, 5, 1},
  {2, 3, 1},
  {3, 5, 1}
};
样例3输出：

3

详细说明：样例3中没有联邦。最长的运输路线为1 -> 2 -> 3 -> 5，成本为3。
*/

package step2;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;


public class Task {
	
	public static class Edge {
        int u;
        int v;
        int w;
    }

	final public static int Maxn = 100010, Maxe = 1000000;
	public static int first[] = new int[Maxn];
	public static int to[] = new int[Maxe];
	public static int ne[] = new int[Maxe];
	public static int c[] = new int[Maxe];
	public static int dfn[] = new int[Maxn];
	public static int low[] = new int[Maxn];
	public static int st[] = new int[Maxn];
	public static int ins[] = new int[Maxn];
	public static int belong[] = new int[Maxn];
	public static int num,top,color,cnt,ans;
	public static int dis[] = new int[Maxn];
	public static int book[] = new int[Maxn];
	

	public static void init(int n) {
	    cnt = 0;
	    ans = 0;
	    num = top = color = 0;
	    for (int i = 0; i <= n; i++) {
	        book[i] = 0;
	        ins[i] = 0;
	        belong[i] = 0;
	        first[i] = -1;
	        dis[i] = Integer.MIN_VALUE;
	    }
	}
	
	public static void add(int u, int v, int w) {
	    to[cnt] = v;
	    c[cnt] = w;
	    ne[cnt] = first[u];
	    first[u] = cnt++;
	}

	
	public static void tarjan(int x) {
	    dfn[x] = low[x] = ++num;
	    st[++top] = x;
	    ins[x] = 1;
	    for (int i = first[x]; i != -1; i = ne[i]) {
	        if (dfn[to[i]] == 0) {
	            tarjan(to[i]);
	            low[x] = Math.min(low[x], low[to[i]]);
	        } else if (ins[to[i]] != 0) {
	            low[x] = Math.min(low[x], dfn[to[i]]);
	        }
	    }
	    if (dfn[x] == low[x]) {
	        color++;
	        int y;
	        do {
	            y = st[top--];
	            ins[y] = 0;
	            belong[y] = color;
	        } while (x != y);
	    }
	}


	public static void spfa(int n) {
		Queue<Integer> q = new LinkedList<Integer>();
	    q.offer(0);
	    book[0] = 1;
	    dis[0] = 0;
	    while (!q.isEmpty()) {
	        int t = q.peek();
	        q.poll();
	        for (int i = first[t]; i != -1; i = ne[i]) {
	            if (belong[t] == belong[to[i]] && dis[to[i]] < dis[t]) {
	                dis[to[i]] = dis[t];
	                if (book[to[i]] == 0) {
	                    q.offer(to[i]);
	                    book[to[i]] = 1;
	                }
	            }
	            if (belong[t] != belong[to[i]] && dis[to[i]] < dis[t] + c[i]) {
	                dis[to[i]] = dis[t] + c[i];
	                if (book[to[i]] == 0) {
	                    book[to[i]] = 1;
	                    q.offer(to[i]);
	                }
	            }
	        }
	        book[t] = 0;
	    }
	}

	public static int solver(int n , List<Edge> edges) {
	        /**********  Begin  **********/
	    init(n);
	    int lened = edges.size();
	    for (int i = 0; i < lened; i++) {
	        add(edges.get(i).u, edges.get(i).v, edges.get(i).w);
	    }
	    for (int i = 1; i <= n; i++)
	        if (dfn[i] == 0)tarjan(i);
	    for (int i = 1; i <= n; i++)
	    	add(0, i, 0);
	    spfa(n);
	    for (int i = 1; i <= n; i++)
	    	ans = Math.max(ans, dis[i]);
	    return ans;
	    /**********  End  **********/
	}
	
}
