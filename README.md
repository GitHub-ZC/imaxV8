# imaxV8
纯净v8 dll 多线程版 运行js代码

# 起因
由于本人需要使用32位dll跑js代码，但是去网上找了一圈都没有看到一个开源的32位v8dll，并且找不到支持 es6 语法的dll，导致很多js代码无法执行，为了能支持 **es6 语法**，于是自己百度研究研究，自己编译了一个32位v8引擎，在这，本着开源奉献的精神，分享给大家。

# 更新
上周已经开源了一个[v8 32位 dll(点击跳转)](https://mp.weixin.qq.com/s/6SrIM8WoFCxmMTYyBiVEMg)，但是由于在这一周的使用情况来看，确实有着很多的不足，我给出的示例是python写的，但是我去尝试了其他的编程语言，发现还是有一些使用兼容的问题。于是通过我的不懈努力(哈哈哈哈哈)，重新编译了一份v8 32 dll，能更好的支持多线程的运行，更好的兼容其他编程语言，以下给出一些编程示例。

# 代码示例
## imaxV8_mul.dll 多线程版
### python
```python
import ctypes

# 加载 DLL
v8_dll = ctypes.cdll.LoadLibrary("./imaxV8_mul.dll")

# 导出函数
runJs_func = v8_dll.__getattr__('_runJs@12')
runJs_func.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
runJs_func.restype = None
# 导出函数
createIsolate_func = v8_dll.__getattr__('_createIsolate@0')
createIsolate_func.restype = ctypes.c_int
createIsolate_func.argtypes = []

# 创建一个运行实例，这一步是必须的，创建的实例是有限制的，需要和对应的线程一一对应
isolate_index = createIsolate_func()
# 创建一个缓冲区用于存储结果
result_buffer = ctypes.create_string_buffer(2048)


def runJs(js_code):
    # 运行 JavaScript 代码，需要传入一个运行实例
    runJs_func(js_code.encode(), result_buffer, isolate_index)
    return result_buffer.value.decode()


if __name__ == '__main__':
    js_code = r"""
        'hello, ' + 'world'
    """
    for i in range(3):
        res = runJs(js_code)
        print("JavaScript 执行结果:", res)
```

### 易语言
```
项目根目录下面：/imaxV8_mul_demo/demo.e 文件，运行此实例，需要将imaxV8_mul.dll放置同一个目录下
```
## imaxV8.dll
### python
```python
import ctypes
import time

def runJs():
    # 加载 DLL
    mymodule = ctypes.CDLL("./imaxV8.dll")

    # 初始化 V8
    mymodule.initializeV8()

    # 准备 JavaScript 代码
    js_code = r'''
        'hello' + ' world';
    '''

    # 调用 runJs 函数执行 JavaScript 代码
    result_ptr = mymodule.runJs(js_code.encode("utf-8"))

    if result_ptr:
        # 将返回的字符串指针转换为 Python 字符串
        result = ctypes.string_at(result_ptr).decode("utf-8")
        # 释放返回结果的内存
        mymodule.free_result(result_ptr)

    # 销毁 V8
    mymodule.disposeV8()

    # 释放DLL, 不释放会报错
    if hasattr(ctypes, 'windll'):
        # Windows平台上使用Win32 API FreeLibrary()
        kernel32 = ctypes.windll.kernel32
        kernel32.FreeLibrary(mymodule._handle)
    return result


if __name__ == '__main__':
    for i in range(1):
        start_time = time.time() # 记录开始时间
        result = runJs()
        end_time = time.time()   # 记录结束时间
        print("代码执行时间：", end_time - start_time, "Result:", result)

```

# 运行示例
```shell
$ .\python-3.12.0-embed-win32\python.exe .\imaxV8_mul_demo\demo.py

# 运行结果
$ JavaScript 执行结果: hello, world
$ JavaScript 执行结果: hello, world
$ JavaScript 执行结果: hello, world
```

# 说明
imaxV8.dll 是第一版打包的dll，单线程运行，对于某些编程语言可能有兼容性问题。

imaxV8_mul.dll 是第二版打包的dll，支持多线程执行，目前给出了两种编程范例，当然由于python本身多线程一个限制，示例只写出来单线程调用，具体多线程写法同单线程类似，大家可以自己研究一下，后续有其他编程范例会更新到项目中。

两个版本都支持 **es6 语法**

# 代码地址
```javascript
// 项目地址
https://github.com/GitHub-ZC/imaxV8
```

# 交流群
## 加好友（备注交流群）

![请添加图片描述](./vx.jpg)


# 免责声明
本项目中提供的V8 DLL（动态链接库）是基于个人编译的版本，仅供参考和学习之用。作者尽力确保其准确性和稳定性，但不对其适用性、可靠性或完整性作任何明示或暗示的保证。因使用该 DLL 而造成的任何直接或间接损失，包括但不限于数据丢失、利润损失等，作者概不负责。任何基于该 DLL 进行的修改、二次开发或应用需自行承担风险。使用者应自行评估并遵守相关法律法规，对于任何因使用本项目而产生的法律责任，作者概不承担。

