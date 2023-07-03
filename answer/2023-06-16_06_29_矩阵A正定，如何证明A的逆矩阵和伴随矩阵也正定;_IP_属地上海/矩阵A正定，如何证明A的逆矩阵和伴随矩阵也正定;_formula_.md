# 矩阵A正定，如何证明A的逆矩阵和伴随矩阵也正定?

<br>


# answer： <br>
存在正交矩阵 $P$ ，使得 $P^{-1}AP=\Lambda$ ，特征值是 $\lambda$ ，特征向量是x，所以 $Ax=\lambda x$
对A的逆矩阵， $x=\lambda A^{-1}x$ ，所以 $A^{-1}x=\frac{1}{\lambda}x$ ，特征值是倒数，特征向量和 $A$ 的相同
所以 $A$ 和 $A^{-1}$ 的正交矩阵也相同都是 $P$ ，则 $P^{-1}A^{-1}P=\Lambda^{-1}$

$\Lambda=diag\{\lambda_1,\lambda_2,...,\lambda_n\}$ ， $\Lambda  ^{-1}=diag\{\frac{1}{\lambda_1},\frac{1}{\lambda_2},...,\frac{1}{\lambda_n}\}$
所以A的逆矩阵 $A^{-1}$ 也是正定的 
<br>

根据伴随矩阵的定义： $AA^*=|A|E$ ，所以 $A^*=|A|A^{-1}$
上面已经推的： $A^{-1}x=\frac{1}{\lambda}x$ ，所以 $A^*x=|A|A^{-1}x=\frac{|A|}{\lambda}x$
矩阵A的伴随矩阵 $A^*$ ，特征值是倒数然后乘以|A|，特征向量和A的相同
所以 $A$ 和$A^*$的正交矩阵也相同都是 $P$ ，则 $P^{-1}A^{*}P=|A|\Lambda^{-1}$
 这里的      $|A|\Lambda^{-1}=diag\{\frac{|A|}{\lambda_1},\frac{|A|}{\lambda_2},...,\frac{|A|}{\lambda_n}\}$
所以A的伴随矩阵 $A^*$ 也是正定的
<br>

[https://www.zhihu.com/question/605881267/answer/3075609886](https://www.zhihu.com/question/605881267/answer/3075609886)<br>



Created: 2023-06-16_06_29・IP_属地上海
Modified: 2023-06-15T22_29_10_000Z
