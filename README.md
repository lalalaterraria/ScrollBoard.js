# README

实现爬取青岛大学OJ滚榜数据，并且滚榜  
其中滚榜程序修改于：<https://github.com/qinshaoxuan/ScrollBoard.js>

第一步修改crawl.py中的参数，其中登录账户必须是管理员账户避免输入密码  
第二步修改index.html中的题数，奖牌数，起始时间和封榜时间  
第三步（可选），使用change.py  

    将nickname改为realname，数据来自test.csv
    如果有非法数据，也可剔除(含字符*的队伍必须剔除)

然后index.html即为自动生成的滚榜
