/*任务描述
Alice 希望实现一个简单的文本编辑器，但是她coding能力不足，所以希望你来帮助她。Alice 的编辑器需要支持以下功能：

插入功能：格式为“I text”，在光标后面 插入 一段文本text。插入后，光标移动到插入字符串之后。

退格功能：格式为“B n”，删除光标 前面 的n个字符，如果光标前面没有字符，则不进行操作。

删除功能：格式为“D n”，删除光标 后面 的n个字符，如果光标后面没有字符，则不进行操作。

左移功能：格式为“L n”，将光标 向左移动 n个字符，如果光标前面没有字符，则不进行操作。

右移功能：格式为“R n”，将光标 向右移动 n个字符，如果光标后面没有字符，则不进行操作。

现在编辑器中有一段长度为N的初始文本，并给定光标的起始位置，求经过M个操作后编辑器中的文本。

编程要求
补全右侧代码区中的String solver(String s,int p,List<Operation> ops)函数，完成挑战任务中提出的要求：返回操作后的文本。

如果需要，你可以在solver函数外添加其它代码，但是 不要 改变Task类的名字、solver函数的定义以及Operation类的实现。

函数参数说明如下：

String s：编辑器中已有的文本，长度记为N。
int p：初始光标位置，0 <= p <= N，表示在第p个字符之后，0表示在第一个字符之前。
List<Operation> ops：表示要进行的操作，操作个数记为M。（1 <= M <= 100000）
数据保证，初始字符串长度和所有“I”操作插入的字符串长度之和不超过200000，所有“B”和“D”操作的总删除字符数不超过100000，所有“L”和“R”操作的总移动字符数不超过100000。初始字符串和“I”操作插入的字符串中的所有字符均为小写字母。

测试说明
样例输入：

s = "whatsyourproblem";
p = 5;
ops = {
  {'L', '', 2},
  {'D', '', 1},
  {'R', '', 4},
  {'I', 'abcdef', 0},
  {'L', '', 3},
  {'B', '', 2}
};
样例输出：

whasyouadefrproblem

*/

package step1;
import java.util.List;
public class Task {

public static String solver(String s,int p,List<Operation> ops) {
        /**********   Begin  **********/
        StringBuffer s1 = new StringBuffer(s);
        int lenop = ops.size();
        Operation tmp;
        int lens1;
        for(int i = 0;i < lenop;i++) {
        	tmp = ops.get(i);
        	lens1 = s1.length();
        	if(tmp.t.equals("L")) {
        		if(p - tmp.l < 0) {
	        		p = 0;
        		}
        		else
        		    p = p - tmp.l;
        	}
        	else if(tmp.t.equals("R")) {
        		if(p + tmp.l >= lens1) {
        			p = lens1;
        		}
        		else
        		    p = p + tmp.l;
        	}
        	else if(tmp.t.equals("D")) {
        		if(p + tmp.l >= lens1) {
        			s1 = s1.delete(p, lens1);
        		}
        		else 
        		    s1 = s1.delete(p, p + tmp.l);
        		
        	}
        	else if(tmp.t.equals("I")) {
        		s1 = s1.insert(p, tmp.s);
        		p = p + tmp.s.length();
        	}
        	else if(tmp.t.equals("B")) {
        		if(p - tmp.l < 0) {
        			s1 = s1.delete(0, p);
	        		p = 0;
        		}
        		else {
	        		s1 = s1.delete(p - tmp.l, p);
	        		p = p - tmp.l;
        		}	
        	}
        }

        return s1.toString();	
        /**********   End  **********/
    }
    static class Operation {
        String t;
        String s;
        int l;
    }
}
