##Python Module for This Seg-Sys

###1.Installation   
```sh
python setup.py build
sudo python setup.py install 
```   

###2. How to use 
   
将训练好的模型数据放入安装目录中
e.g. /usr/local/lib/python3.5/dist-packages/mecab   
   
代码实例
```pycon
>>>import mecab
>>>parse = mecab.parse("结婚的和尚未结婚的")
>>>parse
>>>"结婚 的 和 尚未 结婚 的 \n"
```
