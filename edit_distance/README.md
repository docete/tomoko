问题描述：

把两个字符串变成相同的基本操作定义如下：
1.修改一个字符（如把 a 变成 b）
2.增加一个字符 (如 abed 变成 abedd)
3.删除一个字符（如 bjwilly 变成 bjwill）
我们把从字符串A转换成字符串B，前面3种操作所执行的最少次数称为AB相似度。

通常用DP解决，由俄羅斯科學家Vladimir Levenshtein在1965年提出這個概念。
故也称为Levenshtein距离