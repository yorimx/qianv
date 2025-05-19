import time
from cgitb import handler

from Game import Ui_Form
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from util import  ControlLd,DM
from  PyQt5.Qt import QTableWidgetItem
import  sys

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        self.ld=ControlLd(r'D:\leidian')

        self.dm=DM()
        self.dms={}
        self.threads={}



    def refresh_emulate(self):
        #将两个方法链接一起
        # self.ld是引入control这个类 然后使用里面的方法
        #控件和方法链接到一起
        lines=self.ld.info_ld().splitlines()#将输出的信息切分成一行一行的
        i=0
        for line in lines:
            items=line.split(',')
            j=0
            for item in items:
                self.ui.tableWidget.setItem(i,j,QTableWidgetItem(item))
                j+=1
            i += 1

    def  start_emulate(self):
        # num=self.ui.lineEdit.text()
        # for i in range(int(num)):
        #     self.ld.start_ld(i)
        num=self.ui.tableWidget.currentRow() #currentRow()获取当前行 获取序号
        self.ui.tableWidget.setItem(num,7,QTableWidgetItem('stop'))
        self.ui.tableWidget.setItem(num,8,QTableWidgetItem('登录'))  #初始是空 否则不能写入信息 这里给一个登录信息
        self.ld.start_ld(num)
        print("启动模拟器：",num)
        time.sleep(3)
        self.refresh_emulate()

    def stop_emulate(self):
        num = self.ui.tableWidget.currentRow()  # currentRow()获取当前行 获取序号
        self.ld.stop_ld(num)
        print("关闭模拟器：", num)
        time.sleep(1)
        self.refresh_emulate()

    def restart_emulate(self):
        num = self.ui.tableWidget.currentRow()  # currentRow()获取当前行 获取序号
        self.ld.restart_ld(num)
        print("重开模拟器：", num)
        time.sleep(3)
        self.refresh_emulate()

    def start_all_emulate(self):
        emu_num=len(self.ld.info_ld().splitlines())
        for i in range(emu_num):
            self.ld.start_ld(i)
        time.sleep(3)
        self.refresh_emulate()



    def start_num_emulate(self):
        line=int(self.ui.lineEdit.text())
        for i in range(line):
            self.ld.start_ld(i)
        print("开启模拟器数量：",line)

    def sort_emulate(self):
        self.ld.sort_windows()

    def start_game(self):

        try:
            row = self.ui.tableWidget.currentRow()  # 取出当前行
            handle = int(self.ui.tableWidget.item(row, 3).text())  # 取到句柄     (row,3) 这个行的第三个  因为是从0数起
            thread_flag = self.ui.tableWidget.item(row, 7).text()  # 取出线程状态
            ini_data = self.ui.tableWidget.item(row, 8).text()  # 取出状态

            if thread_flag == 'stop':  # 只有线程是关闭的才会给他开启
                dm_handle = self.dms.get(row, None)
                if dm_handle:
                    # 我们之前启动过，只需要吧之前线程句柄拿出来继续就可以了
                    bindret = dm_handle.BindWindowEx(handle, "gdi", "normal", "normal", "", 0)
                    if bindret == 1:
                        print('绑定窗口成功')
                        # 获取对应多线程然后开始
                        # 这里需要把线程句柄传入到对应的线程中去
                        # qt开启多线程去执行对应操作
                        # 保存线程句柄
                        self.ui.tableWidget.setItem(row, 7, QTableWidgetItem('run'))
                    else:
                        print('绑定窗口失败')
                else:
                    # 之前没启动过，第一次启动
                    # 给他创建一个大漠实例
                    new_dm = self.dm.newDM()
                    self.dms[row] = new_dm
                    # 修复这里的参数问题，确保参数格式与上面一致
                    bindret = new_dm.BindWindowEx(handle, 'gdi', 'normal', 'normal', '', 0)
                    if bindret == 1:
                        print('绑定窗口成功')
                        # qt开启多线程去执行对应操作
                        # 保存线程句柄
                        self.ui.tableWidget.setItem(row, 7, QTableWidgetItem('run'))
                    else:
                        print('绑定窗口失败')
        except Exception as e:
            print(e)

    def start_all_game(self):
        pass

    def stop_game(self):
        try:
            row = self.ui.tableWidget.currentRow()  # 取出当前行
            # handle = int(self.ui.tableWidget.item(row, 3).text())  # 取到句柄     (row,3) 这个行的第三个  因为是从0数起
            thread_flag = self.ui.tableWidget.item(row, 7).text()  # 取出线程状态

            if thread_flag == 'run':
                dm_handle=self.dms[row].get(row,None)
                dm_ret= dm_handle.UnBindWindow() #解出窗口绑定

                if dm_ret==1:
                    print('窗口解绑成功')
                    cur_thread=self.threads.get(row,None)
                    if cur_thread!=None:
                        #如果线程存在就停止
                        cur_thread.terminate() #暂停线程
                    self.ui.tableWidget.setItem(row, 7, QTableWidgetItem('stop'))

                else:
                    print('窗口解绑失败')

            else:
                print('游戏未启动！')
        except Exception as e:
            print(e)

    def stop_all_game(self):
        pass


if __name__ == '__main__':
    app=QApplication(sys.argv) #把控制器的参数传进来
    win=MainWindow()
    win.show()
    sys.exit(app.exec_())  #控制器退出
