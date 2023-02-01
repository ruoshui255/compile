# python 实现的语言：

- 手写递归下降处理表达式的优先级和结合性，解析变量声明、函数声明、类声明、枚举声明等语句
- 使用静态分析手段检测代码中部分错误，运行时再类型检查
- 使用 AST-walking 方法直接对抽象语法树进行解释执行

## 运行

- 安装 python3.8 及以上版本

- windows
  - 在目录下直接运行 `windows_run.bat` 即可进入交互式解释器模式
- Linux
  - 在目录下直接运行 `make run` 即可进入交互式解释器模式

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

## demos
```
// control flow 
for(var i = 0; i < 10; i = i+1) {
    if (i == 3) {
    continue;
    }

    if (i > 6) {
      break;
    }

    print(i);
}
// break;
// continue;
//
// var i = 0;
// while (i < 10) {
//     i = i+1;
//     if (i==3) {
//         continue;
//     }
//
//     if (i > 6) {
//     break;
//     }
//     print(i);
// }
```
```
// closure
fun makeCounter() {
    var i = 0;
    fun count() {
        i = i + 1;
        print(i);
    }

    return count;
}

var counter = makeCounter();
counter(); // 1
counter(); // 2
```

```
// enum, block
enum { ColorRed, ColorBlue, ColorGreen}

var a = "global";
var color1 = ColorRed;

{
    enum { ColorRed, ColorBlue, ColorGreen}

    fun showA() {
        print(a);
    }

    showA(); // global
    var a = "block";
    showA(); // global

    var color2 = ColorRed;
    print(color1 == color2); // False
}
```

```
// class statement
class A {
    init(b){
        this.a = "water";
        this.b = b;
    }
    log() {
        print(this.b);
    }

    test() {
        print("A test " + this.b);
    }

    method() {
        print("A method");
    }
}

class B < A {
    log() {
        print("B log " + this.a);
    }

    method() {
        print("\ntest call super");
        super.method();
    }
}


var b = B("hello");
b.log();    // B log water
b.test();   // A test hello
b.method(); // \ntest call super\nA method
```