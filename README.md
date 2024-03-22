编译libriichi:
```
cargo build -p libriichi --lib --release
cp target/release/riichi.dll libriichi/libriichi.pyd
```


问题描述：
libriichi这个rust程序编译成pyd文件后，在python里面调用。

libriichi.mjai.bot中： (https://github.com/latorc/mortal_test/blob/main/libriichi/src/mjai/bot.rs)
struct Bot下添加了一个clone方法，用于深度拷贝这个对象，供python中调用。

问题：
但是现在python中调用clone()方法会导致卡住，不返回。
测试代码：test.py