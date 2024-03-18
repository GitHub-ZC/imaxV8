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