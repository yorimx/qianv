import os
import subprocess
import ctypes
from distutils.command.register import register

from comtypes.client import CreateObject
import win32com.client
from win32com.client.dynamic import CDispatch

from dm import dm

"""
我们要使用ldconsole.exe
我们需要把ldconsole.exe这个文件目录加到系统环境变量中
才可以直接去操作他

"""
class ControlLd:
    def __init__(self,path):
        os.putenv('Path',path)
    #把调用cmd的命令放在一个管道里，来调用使用
    def run_command(self,command):
        """  运行cmd命令"""
        pipe=subprocess.Popen(args=command,stdout=subprocess.PIPE,shell=True,encoding='gbk')
        pipe = pipe.stdout.read()
        return pipe

    #ldconsole.exe 单独封装一个 方便调用
    #外部调用只需要调用这个
    def info_ld(self):
        """ 获取雷电模拟器的信息"""
        return self.run_command('ldconsole.exe list2')

    #启动模拟器
    def start_ld(self,num):
        """ <UNK>"""
        self.run_command('ldconsole.exe launch --index '+ str(num))
    def stop_ld(self,num):
         self.run_command('ldconsole.exe quit --index '+ str(num))

    def restart_ld(self,num):
        self.run_command('ldconsole.exe reboot --index '+ str(num))

    def sort_windows(self):
         self.run_command('ldconsole.exe sortWnd')



class DM:
    def __init__(self):
        self.dm=None

    def register(self):
        try:
            dm = win32com.client.Dispatch('dm.dmsoft')
            print('本机系统中已经安装大漠插件，版本为:', dm.ver())
        except:
            print('本机并未安装大漠，正在免注册调用')
            dms = ctypes.windll.LoadLibrary('RegDll.dll')
            location_dmreg = os.getcwd() + '\dm.dll'
            dms.SetDllPathW(location_dmreg, 0)
            dm = CreateObject(r'dm.dmsoft')
            self.dm = dm

    def newDM(self):
        return CreateObject(r'dm.dmsoft')


if __name__ == '__main__':
    cld=ControlLd(r'D:\leidian')
    # damo=DM()
    result=cld.info_ld()#在指定目录里运行指令
    dm.MoveTo(422,867)
    dm.LeftClick()
