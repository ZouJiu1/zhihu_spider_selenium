# c++ set运算符重载

<br>
```
#include<iostream>
#include<set>
#include<vector>
using namespace std;
int main(void) {
    int i, j, k, N, M, K;
    vector<int>  v ={10, 6, 11, 0, 100, -1};
    set<int> te;
    for(i = 0; i < v.size(); i++) {
        te.insert(v[i]);
        printf("no reload operation: ");
        for(auto it:te) printf("%d ", it);
        printf("\n");
    }

    struct nod{
        int val;
        bool operator < (const nod &a) const{
            return val > a.val;
        }
    };
    set<nod> tk;
    for(i = 0; i < v.size(); i++) {
        tk.insert({v[i]});
        printf("after reload operation < : ");
        for(auto ti:tk) printf("%d ", ti.val);
        printf("\n");
    }
    return 0;
}
```
<br><br>

[https://zhuanlan.zhihu.com/p/605710105](https://zhuanlan.zhihu.com/p/605710105)<br>



