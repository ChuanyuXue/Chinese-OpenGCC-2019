/*挑战任务
给定一个字符串 s=s_1s_2...s_N，其中N是字符串的长度，s_i是第i个字符。现给出以下定义：

s 的子串 s[i...j] 表示字符串s=s_is_{i+1}...s_j；

s 的长度为l的 前缀 为s=s_1s_2...s_l；

s 的长度为l的 后缀 为s=s_{N-l+1}s_{N-l+2}...s_N；

对于一个前缀，如果它也是一个后缀，那么称其为超级前缀。

现求s包含多少个超级前缀，以及每个超级前缀作为s的子串出现的次数。

编程要求
补全右侧代码区中的vector<pair<int, int>> solve(string s)函数，完成挑战任务中提出的要求。

返回结果中，每个元素对应一个超级前缀，其中first成员是该超级前缀的长度，second成员是其作为子串出现的次数，所有元素按照first成员升序排序。

如果需要，你可以在solve函数外添加其它代码，但是 不要 改变Solver类的名字以及solve函数的定义。

函数参数说明如下：

string s：表示字符串s，长度为N。（1 <= N <= 100000）
测试说明
样例1输入：

s = ABACABA

样例1输出：

1 4

3 2

7 1

样例2输入：

s = AAA

样例2输出：

1 3

2 2

3 1

开始你的任务吧，祝你成功！*/

#ifndef __SOLVER_H__
#define __SOLVER_H__
//#include<stdio.h>
#include<string.h>
#include <cstring>

#include <bits/stdc++.h>
using namespace std;

class Solver {
	public: 
	
void kmp_pre(string x,int m,int next[])
{
    int i,j;
    j = next[0] = -1;
    i = 0;
    while(i < m){
        while(-1 != j && x[i] != x[j]) j = next[j];
        next[++i] = ++j;
    }
}

void preKMP(string x,int m,int kmpNext[]){
    int i,j;
    j = kmpNext[0] = -1;
    i = 0;
    while(i < m){
        while(-1 != j && x[i] != x[j]) j = kmpNext[j];
        if(x[++i] == x[++j]) kmpNext[i] = kmpNext[j];
        else kmpNext[i] = j;
    }
}

int Cnext[400005];
int kmp_Count(string x,int m,string y,int n){
    memset(Cnext,0,sizeof Cnext);
    int i,j;
    int ans = 0;
    //kmp_pre(x,m,Cnext);
    preKMP(x,m,Cnext);
    i = j = 0;
    while (i < n){
        while (-1 != j && y[i] != x[j])j = Cnext[j];
        i++;j++;
        while(j >= m){
            ans++;
            j = Cnext[j];
        }
    }
    return ans;
}




//char s[max];
int next[400005];
int len;
int a[400005];
void get_next(string s,int len) {
    int i=0;
    int j=-1;
    next[0]=-1;
    while(i<len){
        if(j==-1||s[i]==s[j]){
            i++;
            j++;
            next[i]=j;
        }
        else{
            j=next[j];
        }
    }
}

  	
        //printf("%d %d\n",len,aa);
  //  }



	vector<pair<int, int> > solve(string s) {
		/********** Begin **********/
			vector<pair<int, int> >vec;
        int i,j;
        memset(next,0,sizeof(next));
        len=s.length();
        get_next(s,len);
        j=next[len];
        int cnt=0;
        while(j>0) {
            a[cnt++]=j;
            j=next[j];
        }
        int aa = 0;
       // char* sss=new char[400005];
        //char sss[400005];
        string sss;
        sss=s; 
        //strcpy(sss,s);
        char tmp;
        for(i=cnt-1;i>=0;i--) {
            tmp = sss[a[i]];
            sss[a[i]] = 0;
            aa = kmp_Count(sss,a[i],s,len);
          //  pair<int, int> p1(a[i],aa);
          //  pair<int, int> vec = p1;
          //  pair<int, int> vec = make_pair(a[i],aa);
          	pair<int,int> temp1;
			  temp1.first = a[i];
			  temp1.second = aa; 
            vec.push_back(temp1);									//		printf("%d %d\n",a[i],aa);
            sss[a[i]] = tmp;
        }
        aa = kmp_Count(sss,len,s,len);
        //vec.push_back(make_pair<int, int>(len,aa));
        pair<int,int> temp2;
			  temp2.first = len;
			  temp2.second = aa; 
            vec.push_back(temp2);
        // pair<int, int> p1(len,aa);
        // pair<int, int> vec = p1;
         //pair<int, int> vec = make_pair(len,aa);
		return vec;
		/********** End **********/
	}
	
};
#endif