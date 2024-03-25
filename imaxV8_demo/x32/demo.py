import ctypes
import time

def runJs():
    # 加载 DLL
    mymodule = ctypes.CDLL("./imaxV8_demo/x32/imaxV8.dll")

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
