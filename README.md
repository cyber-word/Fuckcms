# Fuckcms
用python写一个自己的多线程web指纹扫描器，提升自己开发安全小工具的能力
# 目录结构
Fuckcms为主文件
# 命令格式
# 批量扫描 
python3 fuckcms.py -t 10 -d all -f urls.txt
表示线程数量为10，指纹数据库采用所有，扫描的网站文件是urls.txt,扫描成功的结果默认输出到同目录下fuckurl.txt中
# 单个url扫描
python3 fuckcms.py -u url地址 对单个url进行扫描,当不指定t和d时线程默认是10，指纹库默认采用所有指纹库(all)
# 参数选项
-d 可以指定 -d cms 或者 -d tide 或者 -d all
# 结果输出
结果输出时，由于MD5计算需要等待，如果采用了CMS这个指纹库识别的话，大致在命令行中会在所有结果运行完后才会识别出一些cms，这就导致了有的识别结果会穿插在另一些扫描结果中，不过整体来说
不影响阅读，为了方便识别出cms以后的下一步检测，默认会将扫描成功的结果输入到同目录下的fuckurl.txt中
# 公众号
 剑南道极客，安全圈新手，大佬们带带我
# 扫描速度
采用了多线程扫描，大致一个网站启用所有指纹库的扫描速度在35s左右
# 参考项目
Tidefinger
# 运行结果
![image](https://user-images.githubusercontent.com/67416400/145021161-b72f0fec-ba4b-4445-a200-1d2d47976e87.png)
# 免责声明
未经授权许可使用Fuckcms攻击目标是非法的
本程序应仅用于授权的安全测试与研究目的
