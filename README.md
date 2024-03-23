背景：Rust编写的模块，编译成dll -> pyd文件后，在python程序里面调用。
Rust模块位于目录libriichi下，以下命令编译成pyd文件（即dll文件套壳在python里可调用）
编译libriichi:
```
cargo build -p libriichi --lib --release
cp target/release/riichi.dll libriichi/libriichi.pyd
```


问题描述：
Rust代码中，libriichi.mjai.bot文件中 (https://github.com/latorc/mortal_test/blob/main/libriichi/src/mjai/bot.rs)

struct Bot下有一个clone方法，目的是用于深度拷贝/克隆这个对象（递归拷贝所有子对象/变量），提供一个状态完全一样的对象复制。
这个clone方法需要在python中可以调用。现在的代码，在python中调用clone()方法会导致卡住，不返回。
测试代码：test.py

需求：修改rust代码（可能需要修改其他相关的文件），给struct Bot实现一个有效的，并且可以在Python中调用的clone方法

