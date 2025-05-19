#免注册调用方法
import ctypes
import os
from comtypes.client import CreateObject
import win32com.client

try:
    dm = win32com.client.Dispatch('dm.dmsoft')
    print('本机系统中已经安装大漠插件，版本为:', dm.ver())
except:
    print('本机并未安装大漠，正在免注册调用')
    dms = ctypes.windll.LoadLibrary('RegDll.dll')
    location_dmreg = os.getcwd()+'\dm.dll'
    dms.SetDllPathW(location_dmreg, 0)
    dm = CreateObject(r'dm.dmsoft')
    print('免注册调用成功 版本号为:',dm.Ver())



# import ctypes
# import win32com.client
# # 免注册调用
# obj = ctypes.windll.LoadLibrary(r"E:\PyWorks\qianv\RegDll.dll")
# obj.SetDllPathW(r"E:\PyWorks\qianv\dm.dll", 0)
#
# # 创建大漠对象
# dm = win32com.client.DispatchEx("dm.dmsoft")
# # 注册大漠
# res = dm.Reg(reg_code, ver_info)
# print("大漠注册返回值: {}".format(res))
#
# # 获取大漠版本号
# print(dm.Ver())




    # print('免注册调用成功 版本号为:', dm.Ver())
    # def __init__(self):
    #     self.dm = None
    # #
    # # # 加载大漠插件DLL文件
    # def register(self):
    #     dmreg_dll_path = os.path.join(os.path.dirname(__file__), 'RegDll.dll')
    #     dm_dll_path = os.path.join(os.path.dirname(__file__), 'dm.dll')
    #     dm = win32com.client.Dispatch("dm.dmsoft")
    #     self.dm = dm
