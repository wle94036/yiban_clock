# 易班一键打卡<br>
## 脚本由Python编写<br/>
* <strong>exe编译使用方法</strong>
> 1.注册ttshitu.com账号，替换YB.py中的第45行获取验证码部分账号密码<br/>
> <br/>
> 2.安装pyinstaller后执行pyinstall --onfile main.py编译成exe<br/>
> <br/>
> 3.在bat文件中添加一条记录，start main.exe <你的学号>点击一次可以帮全帮同学打卡<br/>
> <br/>
> 4.运行bat文件
* <strong>Linux服务器源码直接使用方法</strong>
> 1.注册ttshitu.com账号，替换YB.py中的第45行获取验证码部分账号密码<br/>
> <br/>
> 2.在crontab命令中中添加一条记录，sudo python main.py <你的学号><br/>
> <br/>
> 3.无需人工服务器到点自动打卡
