# qinglong_auto_tools

自用工具，写的烂勿喷。

本仓库遵循自写自用原则，我自己不需要的东西大概率不会去写，慎重提交issues，合理的建议我会采纳。

目录结构：

| 文件名字 | 用途 |
|  ----  | ----  |
| 2288 | 2.2和2.8青龙批量上传ck脚本 |
| Script | 个人修改的一些py脚本，自用，勿喷 |
| qq | qq相关脚本，自用 |
| tg | tg相关脚本，自用 |
| trs_stream.py | 本地转换stream抓到的headers为json格式，使用方法详见注释 |
| ck_auto_select.py | ck本地去重小工具，用法看注释 |  
| cks_push_alql.py | 多容器ck分发工具，方便多容器管理，用法详见注释 |
| cks_merge_alql.py | 多容器ck合并工具，方便多容器管理，用法详见注释 |
| cks_sync_able.py | 多容器同步环境变量状态及备注，方便多容器管理，使用方法详见注释 |
| tasks_sync_able.py | 多容器同步任务启用禁用脚本，方便多容器管理，使用方法详见注释 |
| tasks_sync_scripts_able.py | 多容器同步已启用的脚本文件，方便多容器脚本更新管理，使用方法详见注释 |
| tasks_sync_all.py | 多容器无脑同步所有脚本文件和任务，方便多容器脚本迁移管理，使用方法详见注释 |
| scripts_check_nets.py | 单容器查询自己脚本文件中的网络链接，查询脚本中含有的链接，使用方法详见注释 |
| ~~scripts_purge_keys.py~~ | ~~单容器清除屏蔽词脚本，屏蔽脚本中含有的屏蔽词，使用方法详见注释~~ 有bug待修复 |
| scripts_check_dependence.py | 单容器依赖文件修复脚本，使用方法详见注释 |
| scripts_check_error.py  | 单容器监控脚本运行状态脚本，使用方法详见注释 |
| scripts_trigger_ckorder.py | 单容器随机ck顺序脚本，可指定头几个顺序不变，使用方法详见注释 |
| scripts_rearblack.py | 单容器检索任务日志标注黑号自动后置脚本，使用方法详见注释和运行后的该任务日志 |
| scripts_polltask.py | 单容器自动尝试运行禁用任务，若日志不报错自动启用脚本，使用方法详见注释和运行后的该任务日志 |
| scripts_restore_env.py | 单容器还原环境变量，专门还原顺序脚本和后置黑号脚本打乱的环境变量顺序，需要还原只要运行即可|
| ec_config.txt | 多容器脚本脚本的配置文件，请按照脚本提示填写 |


### 多容器相关脚本 

**仅支持公网IP能访问的版本2.9.0以上的青龙，至多到2.10.13已适配**

| 文件名字 | 用途 |
|  ----  | ----  |
| ec_config.txt | 多容器脚本和单容器脚本的配置文件，请按照对应脚本注释提示填写 |
| cks_push_alql.py | 多容器ck分发工具，方便多容器管理，用法详见注释 |
| cks_merge_alql.py | 多容器ck合并工具，方便多容器管理，用法详见注释 |
| cks_sync_able.py | 多容器同步环境变量状态及备注，方便多容器管理，使用方法详见注释 |
| tasks_sync_able.py | 多容器同步任务启用禁用脚本，方便多容器管理，使用方法详见注释 |
| tasks_sync_scripts_able.py | 多容器同步已启用的脚本文件，方便多容器脚本更新管理，使用方法详见注释 |
| tasks_sync_all.py | 多容器无脑同步所有脚本文件和任务，方便多容器脚本迁移管理，使用方法详见注释 |

青龙拉取命令：

环境变量相关：

```bash
ql repo https://jihulab.com/spiritlhl/qinglong_auto_tools.git "cks_"
```

任务相关：

```bash
ql repo https://jihulab.com/spiritlhl/qinglong_auto_tools.git "tasks_"
```

### 单容器相关脚本

仅支持云服务器部署的2.9.0以上的青龙，至多到2.10.13已适配

| 文件名字 | 用途 |
|  ----  | ----  |
| scripts_check_nets.py | 单容器查询自己脚本文件中的网络链接，查询脚本中含有的链接，使用方法详见注释 |
| scripts_check_dependence.py | 单容器依赖文件修复脚本，使用方法详见注释 |
| scripts_check_error.py  | 单容器监控脚本运行状态脚本，使用方法详见注释 |
| scripts_trigger_ckorder.py | 单容器随机ck顺序脚本，可指定可指定头几个顺序不变，使用方法详见注释 |
| scripts_rearblack.py | 单容器检索任务日志标注黑号自动后置脚本，使用方法详见注释和运行后的该任务日志 |
| scripts_polltask.py | 单容器自动尝试运行禁用任务，若日志不报错自动启用脚本，使用方法详见注释和运行后的该任务日志 |
| scripts_restore_env.py | 单容器还原环境变量，专门还原顺序脚本和后置黑号脚本打乱的环境变量顺序，需要还原只要运行即可|
| ~~b_script_purge_keys.py~~ | ~~单容器清除屏蔽词脚本，屏蔽容器脚本中含有的屏蔽词，使用方法详见注释~~ 有bug待修复 |

青龙拉取命令：

```bash
ql repo https://jihulab.com/spiritlhl/qinglong_auto_tools.git "scripts_"
```

### 容器相关脚本使用说明(小白必看)

脚本使用：

**首先，事先声明，你的qinglong应用ID和secretkey就相当于你的登陆用户名和密码，请勿随意泄露，如果是他人帮你搭建的，请及时删除已有的应用再创建新的应用，避免他人盗取数据。**

先看一张图，了解大概

![大概流程](https://s2.loli.net/2021/12/25/zGAZyVkjTvJnciS.png)

#### 1.先说环境变量相关

成功使用ql命令拉环境变量相关脚本取后，在”青龙“里使用脚本管理右上角新建文本(如果是新青龙在对应仓库文件夹，如果是单拉或者旧青龙在根目录创建)，命名"ec_config.txt"，然后在里面粘贴本仓库对应文件的内容，按照注释填写信息，然后保存，注意对应变量！！！

![脚本管理图](https://i.loli.net/2021/10/29/cyK9R8IwjP1WA7U.png)

ps:别在服务器里创建并修改ec_config.txt文件，青龙识别不到没用的，一定要用青龙的“脚本管理”创建并填写信息！！！

#### 2.脚本 cks_push_alql.py，也就是任务 二叉树分发ck ，会从主青龙里取出不含wskey的ck，按顺序转发到副的容器(青龙)里，每个容器默认40个号，最后会整合所有不含wskey的ck，转发到备份容器(青龙)里，备份容器(青龙)就是主青龙没有wskey的副本。

![分发效果图](https://i.loli.net/2021/10/29/25LarSXgqpTKPs6.png)

该脚本分发不识别是否启用禁用ck！默认全转发(含禁用的)！如若其余的青龙(容器)没有对应pin值的ck，会自动添加到该容器(青龙)的环境变量最后！

第一个副青龙(容器)里使用任务相关脚本，统合管理其余的副青龙(容器)，这个后面再说怎么配置。

副青龙(容器)专门拿来跑不需要互助，或者互助人数少的脚本。备份容器(青龙)是单独的容器，专门拿来跑需要所有ck的脚本。

第一次运行分发脚本运行后，转发到其他容器(青龙)后，其他容器(青龙)的ck位置可以手动调整，下次分发到其他容器(青龙)时，ck不会改变你调整的位置。这个规律也适用于备份容器(青龙)，第一次分发后再调整备份容器(青龙)的ck位置，后面再分发不会改变位置！

#### 3.脚本 cks_sync_able.py，也就是 二叉树环境变量状态同步 ，会同步ck的备注信息，同步ck启用禁用情况，在 二叉树分发ck 后使用。

顺序上来说，主青龙的脚本运行顺序应该是 

wskey转ck  早于  二叉树分发ck  早于  环境变量状态同步

#### 4.主青龙配置完毕，该配置跑脚本的第一个副青龙(容器)了

“跑脚本的第一个副青龙(容器)”成功使用ql命令拉取任务相关后，在”青龙“里使用脚本管理右上角新建文本，命名"ec_config.txt"，然后在里面粘贴本仓库对应文件的内容，按照注释填写信息，然后保存，注意对应变量！！！

配置好"ec_config.txt"后，就能使用对应脚本了。注意，这里的任务相关的脚本配置，主青龙是指的是跑脚本的第一个容器，不是前面环境变量相关的那个拿来转码的主青龙，这一点别搞混了。

看到这里，如果你同步脚本的其他青龙不是空容器，事先有跑过脚本，那么下面这几行字就不用看了，看步骤5去吧，下面是给空容器(青龙)准备的。

首先，如果你是给空容器同步，第一次使用的应该是 tasks_sync_all.py ，也就是 二叉树无脑同步 。该脚本会无脑同步你配置的第一个副青龙(容器)到别的容器(青龙里)。

它会自动给空容器添加脚本和对应任务，忽略脚本是否被禁用的同步。这个操作只能运行“一次”，多次运行会多次添加任务的，所以别重复运行，任务相关的日常使用的脚本只有步骤5那两个。

如果是空容器，运行完上一步后，除了以文件夹形式存储的依赖，都应该已经同步了，注意那些npm和python依赖还是得命令行装，因为脚本不会同步这些东西。

#### 5.跑脚本的第一个副青龙(容器)需要必装的两个脚本

tasks_sync_scripts_able.py 和 tasks_sync_able.py。它们分别是 二叉树同步脚本文件 和 二叉树同步任务启用禁用 。

脚本运行顺序是先同步文件，再同步任务启用禁用。注意这里的两个脚本对应主青龙(容器)是跑脚本的第一个容器(青龙)，不是转码那个。

粗略解释一下运作原理，首先从主青龙中取得启用任务对应的脚本，然后检索被同步的其他青龙，如果已有的(任务对应的)脚本有更改，会把脚本更改同步到其他青龙里去。

如果任务不存在，会自动新增任务和对应脚本，检索判断是 名字+命令 是否有相同的存在，不存在就会新增，存在就只检索脚本是否有区别需要更新。

二叉树同步任务启用禁用 这个任务则会检索青龙(容器)，同步任务的状态，是启用还是禁用。(这里的检索条件是任务名字，如果有相同名字，可能无法同步)

#### 6.接下来说说单文件脚本

相信经过上面的配置，应该懂怎么配置了，注意配置对应的注释和变量，别填错地方就行。

scripts_check_nets.py ，也就是 二叉树查网络链接 ，配置好后运行会查询仓库脚本的网络链接，还有其中含有屏蔽词的有几个，有需要可以试试。

清除屏蔽词的另一个脚本暂时有bug，有时间我修好再用吧，现在你们应该拉不到，忽略它。

scripts_check_dependence.py，也就是二叉树修复依赖文件脚本，拉取后运行一次，可以查查自己有啥脚本依赖文件没装的，在配置文件中配置，可以修补缺失文件(jdCookie.js那种)，不建议开启内置的依赖更新，那个有魔改的只适用于对应的config--->https://jihulab.com/spiritlhl/dependence_config/

最后贴个效果图吧。

![](https://i.loli.net/2021/10/30/gcsyT8Wa1QJmn2E.png)

![](https://i.loli.net/2021/10/30/m4eHKVof2A1SqbT.png)

![](https://i.loli.net/2021/11/01/T8Z5bvwOn7J2jXE.png)

### 统一回答一些易错点

1.配置文件在容器中创建或本地上传，导致编码不一致青龙识别了也没发读取变量，内容存在乱码

错误截图如下：

![](https://i.loli.net/2021/11/05/L8P31e5arigEUwN.png)

解决方法：在青龙中创建而不是其他方式创建配置文件。

2.没计算好分发数量，导致容器分发溢出的，默认分发每个容器40个，只能少不能多，如果你的```主容器(青龙)变量总数```超过```40×分容器(青龙)数量```，那么分发会溢出报错

错误截图如下：

![](https://i.loli.net/2021/11/05/xzuwjvdQoXR25rK.png)

解决方法：在配置文件ec_config.txt中配置```cks_push_alql_N_c```变量自定义分发数量，默认是40，或增加分容器(副青龙)数量使数据不溢出

3.分发的默认变量```不含关键字```，需要在环境变量管理中查询```关键字```，然后勾选全部禁用，再刷新页面，剩下启用的就是```不含关键字```的导致分发报错的变量，需要剔除才能进行分发

4.分容器(青龙)中自身含环境变量，后续增加导致那个容器(青龙)环境变量超过40个(默认配置)，分发前请清空分容器变量，避免分发的变量和原有变量出现混合，记得做好备份

5.配置的txt文件里少了```/```后缀，正常链接应该是 http://xxxxx:xxxx/ 而不是 http://xxxx:xxxx

暂时写到这，有时间再补充。

### 更新说明 



更新日志：

```
    2022.2.7
    有新项目玩了，本人如无大需求本仓库大概率不会更新了，年中可能回来看看。
    2022.3.8
    Github再也不用了，为了首页老是弹出来的公告对线封我号了，外国平台终究是屁股歪。
```

转载起码保留作者名谢谢

### 通知&交流

频道：https://t.me/qinglong_auto_tools

群组：https://t.me/qinglong_auto_tools_chat

# 免责声明

* 代码仅供学习
* 不可用于商业以及非法目的,使用本代码产生的一切后果, 作者不承担任何责任.

## Special statement:

Any unlocking and decryption analysis scripts involved in the Script project released by this warehouse are only used for testing, learning and research, and are forbidden to be used for commercial purposes. Their legality, accuracy, completeness and effectiveness cannot be guaranteed. Please make your own judgment based on the situation. .

All resource files in this project are forbidden to be reproduced or published in any form by any official account or self-media.

This warehouse is not responsible for any script problems, including but not limited to any loss or damage caused by any script errors.

Any user who indirectly uses the script, including but not limited to establishing a VPS or disseminating it when certain actions violate national/regional laws or related regulations, this warehouse is not responsible for any privacy leakage or other consequences caused by this.

Do not use any content of the Script project for commercial or illegal purposes, otherwise you will be responsible for the consequences.

If any unit or individual believes that the script of the project may be suspected of infringing on their rights, they should promptly notify and provide proof of identity and ownership. We will delete the relevant script after receiving the certification document.

Anyone who views this item in any way or directly or indirectly uses any script of the Script item should read this statement carefully. This warehouse reserves the right to change or supplement this disclaimer at any time. Once you have used and copied any relevant scripts or rules of the Script project, you are deemed to have accepted this disclaimer.

## Stargazers over time

[![Stargazers over time](https://starchart.cc/spiritLHL/qinglong_auto_tools.svg)](https://starchart.cc/spiritLHL/qinglong_auto_tools/)
