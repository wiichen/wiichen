import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import QDateTime, QFile, QFileInfo, QIODevice, QThread
from PyQt5.QtGui import QTextCursor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("MainWindow")
        self.setGeometry(100, 100, 800, 600)

        # Assuming you have a QPlainTextEdit widget named 'info' in your UI
        self.info = self.findChild(QPlainTextEdit, "info")

        # Assuming you have a QAction named 'actionOpenFile' in your UI
        self.actionOpenFile = self.findChild(QAction, "actionOpenFile")
        self.actionOpenFile.triggered.connect(self.slot_pro_openfile)

    def slot_pro_openfile(self):
        strTIMESN = QDateTime.currentDateTime().toString("yyyyMMdd.hhmmss")

        fileName, _ = QFileDialog.getOpenFileName(self, "打开配置模板文件", "", "moudle (*.csv)")
        if fileName:
            self.info.appendPlainText("准备处理模板文件：" + fileName)
            file = QFile(fileName)
            if not file.open(QIODevice.ReadOnly | QIODevice.Text):
                self.info.appendPlainText("模板文件打开失败：" + fileName)
                return

            fileInfo = QFileInfo(fileName)
            cfgPath = fileInfo.absolutePath() + "/"
            fnameSMARTINI = cfgPath + "smart_config.ini"
            fileSMARTINI = QFile(fnameSMARTINI)
            if not fileSMARTINI.open(QIODevice.WriteOnly | QIODevice.Text | QIODevice.Truncate):
                self.info.appendPlainText("创建索引文件失败：" + fnameSMARTINI)
                return
            else:
                str2write = "BEGIN LSW\n[GLOBAL CONFIG]\n"
                fileSMARTINI.write(str2write.encode())
                str2write = "TIMESN=" + strTIMESN + "\n"
                fileSMARTINI.write(str2write.encode())
                str2write = "AUTODELFILE=YES\nACTIVEMODE=DEFAULT\n"
                fileSMARTINI.write(str2write.encode())
                self.info.appendPlainText("索引文件全局配置写入完成")

            lineNO = 0
            devSEQ = 0
            indexSYSNAME = 0
            indexESN = 0
            indexSOFTWARE = 0
            indexSYSPAT = 0
            indexMAC = 0
            indexCFGTEMPLET = 0
            listTitle = []

            while not file.atEnd():
                line = file.readLine()
                lineNO += 1
                self.info.appendPlainText(str(lineNO) + ":" + line.data().decode())

                strLine = line.data().decode()
                listItems = strLine.split(",")
                if len(listItems) > 4:
                    if lineNO == 1:
                        self.info.appendPlainText("处理表头：" + strLine)
                        indexSYSNAME = listItems.index("#SYSNAME#")
                        indexESN = listItems.index("#ESN#")
                        indexMAC = listItems.index("#MAC-ADDRESS#")
                        indexSOFTWARE = listItems.index("#SYSTEM-SOFTWARE#")
                        indexSYSPAT = listItems.index("#SYSTEM-PAT#")
                        indexCFGTEMPLET = listItems.index("#CFGTEMPLET#")

                        if (listItems[0].strip() == "#ORDER#"
                                and listItems[1].strip() == "#TIMESN#"
                                and listItems[2].strip() == "#SWITCH_MODEL#"
                                and indexSYSNAME > 0
                                and indexESN > 0
                                and indexMAC > 0
                                and indexSOFTWARE > 0
                                and indexSYSPAT > 0
                                and indexCFGTEMPLET > 0):
                            self.info.appendPlainText("表头内容校验完毕!")
                            listTitle = strLine.split(",", maxsplit=-1)
                        else:
                            self.info.appendPlainText("表头内容不正确!")
                    else:
                        self.info.appendPlainText("处理数据行：" + strLine)
                        listData = strLine.split(",", maxsplit=-1)
                        if len(listData) == len(listTitle):
                            self.info.appendPlainText("处理设备型号：" + listData[2]
                                                    + " SYSNAME:" + listData[indexSYSNAME])
                            fNameSYS = cfgPath + listData[indexCFGTEMPLET].lower()
                            self.info.appendPlainText("准备打开设备配置模板：" + fNameSYS)

                            fileSYS = QFile(fNameSYS)
                            if not fileSYS.open(QIODevice.ReadOnly | QIODevice.Text):
                                self.info.appendPlainText("配置模板文件打开失败：" + fNameSYS)
                                return
                            else:
                                strSYS = fileSYS.readAll().data().decode()
                                for idx in range(3, len(listData)):
                                    if idx == indexSOFTWARE or idx == indexSYSPAT or idx == indexCFGTEMPLET:
                                        continue

                                    if listTitle[idx].startswith("#"):
                                        if len(listData[idx]) == 0:
                                            self.info.appendPlainText("字段：" + listTitle[idx] + " 值为空！")
                                        elif listTitle[idx] in strSYS:
                                            self.info.appendHtml("<p>替换：<span style='color: blue;'>" + listTitle[idx] + "</span> 为：<span style='color: green;'>" + listData[idx] + "</span></p>")
                                            strSYS = strSYS.replace(listTitle[idx], listData[idx])
                                        else:
                                            self.info.appendHtml("<span style='color: red;'>在配置模板内找不到匹配项：" + listTitle[idx] + "</span>")

                                strSYSCONFIG = listData[indexSYSNAME].lower() + "_" + listData[indexESN].lower() + ".cfg"
                                fNameNewCfg = cfgPath + strSYSCONFIG
                                self.info.appendPlainText("准备生成配置文件：" + fNameNewCfg)

                                fileNewCfg = QFile(fNameNewCfg)
                                if not fileNewCfg.open(QIODevice.WriteOnly | QIODevice.Text | QIODevice.Truncate):
                                    self.info.appendPlainText("打开配置文件失败：" + fNameNewCfg)
                                    return
                                else:
                                    fileNewCfg.write(strSYS.encode())
                                    fileNewCfg.close()
                                    self.info.appendPlainText("配置文件写入完成")

                                if fileSMARTINI.isOpen():
                                    str2write = "[DEVICE" + str(devSEQ) + " DESCRIPTION]\n"
                                    fileSMARTINI.write(str2write.encode())
                                    str2write = "ESN=" + listData[indexESN].lower() + "\n"
                                    fileSMARTINI.write(str2write.encode())
                                    str2write = "MAC=" + listData[indexMAC].upper() + "\n"
                                    fileSMARTINI.write(str2write.encode())
                                    str2write = "SYSTEM-SOFTWARE=" + listData[indexSOFTWARE] + "\n"
                                    fileSMARTINI.write(str2write.encode())
                                    str2write = "SYSTEM-PAT=" + listData[indexSYSPAT] + "\n"
                                    fileSMARTINI.write(str2write.encode())
                                    str2write = "SYSTEM-CONFIG=" + strSYSCONFIG + "\n"
                                    fileSMARTINI.write(str2write.encode())

                                devSEQ += 1
                        else:
                            self.info.appendPlainText("数据行与表头行数据不一致，可能存在空值!")

                QApplication.processEvents()
                QThread.usleep(200 * 1000)

            str2write = "END LSW\n"
            fileSMARTINI.write(str2write.encode())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())