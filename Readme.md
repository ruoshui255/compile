# 基于 python 实现的编程语言

- 手写递归下降处理表达式的优先级和结合性，解析变量声明、函数声明、类声明、枚举声明等语句
- 使用静态分析手段检测代码中部分错误，运行时再类型检查
- 使用 AST-walking 方法直接对抽象语法树进行解释执行

## 使用
 
- 安装 python3.10 及以上版本
- windows
  - 在目录下直接运行 `windows_run.bat` 即可进入交互式解释器模式
  - 按 `Ctrl+Z` 退出
- Linux
  - 在目录下直接运行 `sh ./linux_run.sh` 即可进入交互式解释器模式
  - 按 `Ctrl+D` 退出
- 读取文件执行
```
# linux
export PYTHONPATH=$(pwd)
python3 src/main.py demo/block.txt
```
![](./img/运行文件.gif)

## 实现的功能

- 基本类型
  - 数字
  - 字符串
  - 布尔值
  - 枚举
- 控制语句
  - if...else...
  - for/while
    - break/continue
- 词法作用域
- 声明
  - 变量声明
    - 变量为动态类型，可以赋值给任意类型给变量
  - 函数声明
    - 函数是一等公民，支持闭包
  - 类声明
    - 支持继承, 多态