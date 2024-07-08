# 使用Forgejo和Trello来实现团队的开发进度管理
## 介绍
1. 如题，本项目是使用Forgejo和Trello来开发的
2. Forgejo用于管理代码控制项目质量，Trello用于管理项目的进度和实现团队间的合作。
3. 本项目适合用于使用敏捷开发中的kanban类型的团队,希望可以达成“单线程异步团队开发”的效果

## 安装方法
1. 非全docker（forgejo --> docker）模式
   1. 
2. 全docker模式

## 使用方法
1. 请先自行创建Trello Board
2. 把Trello的配置信息放置在文件`.trello_settings`中


## 开发计划
1. Trello需要本人在Trello上创建board
2. 需要有个地方放置Trello的配置
3. Forgejo需要使用docker来创建
4. 也需要有个地方来放置Forgejo的配置，最好放在和Trello同级的目录下。
5. 在页面上创建forgejo的webhook，并获取forgejo的配置
6. 在trello中自己创建一些label
7. 在forgejo中也可以自己创建一些label
8. 在trello中自己创建一些成员
9. 在forgejo中也自己创建一些成员
10. 在admin-vue中可以管理和匹配labels
11. 在admin-vue中可以管理和匹配成员
12. 使用redis把数据整理进去
   ```json
   {
      "trello_lables": {
        "low": "xxxxxx",
        "middel": "xxxxxx",
        "high": "xxxxxx"
      },
      "forgejo_lables": {
        "easy": "aaaaa",
        "normal": "aaaaa",
        "hard": "aaaaa"
      },
      "trello_members": {
        "palm zhang": "xxxxxx",
        "peom wang": "xxxxxx",
        "Lili": "xxxxxx"
      },
      "forgejo_members": {
        "PalmZhang": "aaaaa",
        "PompeoZhang": "aaaaa",
        "Li li": "aaaaa"
      }
   }
   ```
13. 匹配之后的数据应该是这样的
    ```json
    {
      "lables_relation": {
        "low": ["xxxx", "aaaaa"],
        "middle": ["xxxx", "aaaaa"],
        "high": ["xxxx", "aaaaa"]
      },
      "members_relation": {
        "palm zhang": ["xxxxx", "aaaaaa"],
        "peom wang": ["xxxxx", "aaaaaa"],
        "Lili": ["xxxxx", "aaaaaa"]
      }
    }
    ```
14. 