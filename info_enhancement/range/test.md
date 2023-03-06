论文笔记：[《ReDeBug: Finding Unpatched Code Clones in Entire OS Distributions》精读_Elwood Ying的博客-CSDN博客](https://blog.csdn.net/yalecaltech/article/details/107040553)

代码复现：[ReDeBug简单使用_Elwood Ying的博客-CSDN博客](https://blog.csdn.net/yalecaltech/article/details/107226303)



## 测试

#### 操作记录

```shell
pip install bitarray python-magic argparse

-- 如有关于python-magic的报错，可尝试卸载再安装
pip uninstall python-magic
pip install python-magic-bin==0.4.14

-- Download redebug.py
git init 
git clone https://github.com/dbrumley/redebug.git

```



测试腾讯文档去年已找到漏洞补丁的漏洞

### CVE-2021-36161

漏洞影响的组件版本: Dubbo 2.7.0 to 2.7.12

漏洞修复的组件版本: Dubbo 2.7.13

测试版本：2.7.13 

```
python redebug.py  D:\2023Spring\供应链项目\2.5.5\test\diff\CVE-2021-36161.diff D:\2023Spring\供应链项目\2.5.5\test\dubbo-dubbo-2.7.13\dubbo-common\src\main\java\org\apache\dubbo\common\utils
```

```
[+] traversing patch files
[+] 6 patches ... 0.3s

[+] traversing source files
[+] 4 possible matches ... 0.7s

[+] performing an exact matching test
[+] 4 exact matches ... 0.0s

[+] generating a report
[+] "output.html" ... 0.0s

[+] 4 matches given 6 patches ... 0.9s
```

测试2.7.12

```
python redebug.py  D:\2023Spring\供应链项目\2.5.5\test\diff\CVE-2021-36161.diff   D:\2023Spring\供应链项目\2.5.5\test\dubbo-dubbo-2.7.12\dubbo-common\src\main\java\org\apache\dubbo\common\utils
```

结果

```
[+] traversing patch files
[+] 6 patches ... 0.3s

[+] traversing source files
[+] 6 possible matches ... 0.7s

[+] performing an exact matching test
[+] 6 exact matches ... 0.0s

[+] generating a report
[+] "output.html" ... 0.0s

[+] 6 matches given 6 patches ... 0.9s
```

### CVE-2021-43297

影响版本（网站）：Apache Dubbo 2.6.0  -  2.6.12 ； 2.7.0 - 2.7.15 ； 3.0.0 -3.0.5

修复版本（网站）：Apache Dubbo 2.6.13  -  2.6.14 ；3.0.6  -  3.0.8

测试版本2.6.12

```
python redebug.py D:\2023Spring\供应链项目\2.5.5\test\diff\CVE-2021-43297.diff D:\2023Spring\供应链项目\2.5.5\test\dubbo-dubbo-2.6.12\dubbo-common\src\main\java\com\alibaba\dubbo\common\utils
```

```
[+] traversing patch files
[+] 8 patches ... 0.3s

[+] traversing source files
[+] 0 possible matches ... 0.4s

[!] no match to be checked
```

测试修复版本3.0.0

```
python redebug.py D:\2023Spring\供应链项目\2.5.5\test\diff\CVE-2021-43297.diff D:\2023Spring\供应链项目\2.5.5\test\dubbo-dubbo-3.0.0\dubbo-common\src\main\java\org\apache\dubbo\common\utils
```

```
[+] traversing patch files
[+] 8 patches ... 0.3s

[+] traversing source files
[+] 0 possible matches ... 0.6s

[!] no match to be checked
```

测试版本3.0.4

```
python redebug.py D:\2023Spring\供应链项目\2.5.5\test\diff\CVE-2021-43297.diff D:\2023Spring\供应链项目\2.5.5\test\dubbo-dubbo-3.0.4\dubbo-common\src\main\java\org\apache\dubbo\common\utils
```

```
[+] traversing patch files
[+] 8 patches ... 0.3s

[+] traversing source files
[+] 0 possible matches ... 0.6s

[!] no match to be checked
```

