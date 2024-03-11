
# imaxV8
纯净v8 dll，可以运行js代码

# 起因
由于本人需要使用32位dll跑js代码，但是去网上找了一圈都没有看到一个开源的32位v8dll，于是自己百度研究研究，自己编译了一个32位v8引擎，在这，本着开源奉献的精神，分享给大家。

# 代码示例
```javascript
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
$ .\python-3.12.0-embed-win32\python.exe main.py

# 运行结果
$ 代码执行时间： 0.008009195327758789 Result: hello world
```

# 代码地址
```javascript
// 项目地址
https://github.com/GitHub-ZC/imaxV8
```

# 免责声明
本项目中提供的V8 DLL（动态链接库）是基于个人编译的版本，仅供参考和学习之用。作者尽力确保其准确性和稳定性，但不对其适用性、可靠性或完整性作任何明示或暗示的保证。因使用该 DLL 而造成的任何直接或间接损失，包括但不限于数据丢失、利润损失等，作者概不负责。任何基于该 DLL 进行的修改、二次开发或应用需自行承担风险。使用者应自行评估并遵守相关法律法规，对于任何因使用本项目而产生的法律责任，作者概不承担。