## Python Module for This Seg-Sys

### 1.Installation   
```sh
python setup.py build
sudo python setup.py install 
```   

### 2. How to use 
   
将训练好的模型数据放入安装目录中
e.g. /usr/local/lib/python3.5/dist-packages/mecab   
   
代码实例
```pycon
>>>import mecab
>>>parse = mecab.parse("使用WordEmbedding思想来构造文本摘要的一些思路，其中包括一种异常简单的文本摘要实现思路")
>>>parse
>>>'使用 Word Embedding 思想 来 构造 文本 摘要 的 一些 思路 ， 其中 包括 一种 异常 简单 的 文本 摘要 实现 思路 \n'
```
   
### 3. 关键词提取
   
在分词、词性标注、拼音转换和繁简转换功能的基础上，拓展了关键词提取的功能   
基于Tf-Idf算法的关键词提取
* mecab.extract_tags(sentence,option, topK=20, withWeight=False, allowPOS=())
  * sentence 为待提取的文本
  * option 为选择是否标注词性, 选择mecab.POS 为词性标注, 选择mecab.WAKATI不进行词性标注
  * topK 为返回几个 TF/IDF 权重最大的关键词，默认值为 20
  * withWeight 为是否一并返回关键词权重值，默认值为 False
  * allowPOS 仅包括指定词性的词，默认值为空，即不筛选
代码实例
```pycon
>>>import mecab
>>>tags = mecab.tfidf("使用WordEmbedding思想来构造文本摘要的一些思路，其中包括一种异常简单的文本摘要实现思路", mecab.WAKATI, top_k=5)
>>>tags
>>>['文本', '摘要', '思路', 'Word', 'Embedding']
```
基于Text-Rank算法的关键词提取
* mecab.text_rank(sentence, option, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v')) 直接使用，接口相同，注意默认过滤词性。
* mecab.TextRank() 新建自定义 TextRank 实例
