import sys
import argparse
from datetime import datetime
import os

def process_file(fileName):
    strTIMESN = datetime.now().strftime("%Y%m%d.%H%M%S")

    if fileName:
        print("准备处理模板文件：" + fileName)
        try:
            with open(fileName, 'r', encoding='utf-8') as file:
                # 获取文件路径
                cfgPath = os.path.dirname(fileName) + "/"
                fnameSMARTINI = cfgPath + "smart_config.ini"

                # 创建并写入索引文件
                with open(fnameSMARTINI, 'w', encoding='utf-8') as fileSMARTINI:
                    fileSMARTINI.write("BEGIN LSW\n[GLOBAL CONFIG]\n")
                    fileSMARTINI.write(f"TIMESN={strTIMESN}\n")
                    fileSMARTINI.write("AUTODELFILE=YES\nACTIVEMODE=DEFAULT\n")
                    print("索引文件全局配置写入完成")

                lineNO = 0
                devSEQ = 0
                indexSYSNAME = 0
                indexESN = 0
                indexSOFTWARE = 0
                indexSYSPAT = 0
                indexMAC = 0
                indexCFGTEMPLET = 0
                listTitle = []

                # 逐行读取CSV文件
                for line in file:
                    lineNO += 1
                    print(f"{lineNO}: {line.strip()}")

                    strLine = line.strip()
                    listItems = strLine.split(",")
                    if len(listItems) > 4:
                        if lineNO == 1:  # 处理表头
                            print("处理表头：" + strLine)
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
                                print("表头内容校验完毕!")
                                listTitle = strLine.split(",")
                            else:
                                print("表头内容不正确!")
                        else:  # 处理数据行
                            print("处理数据行：" + strLine)
                            listData = strLine.split(",")
                            if len(listData) == len(listTitle):
                                print(f"处理设备型号：{listData[2]} SYSNAME: {listData[indexSYSNAME]}")
                                fNameSYS = cfgPath + listData[indexCFGTEMPLET].lower()
                                print("准备打开设备配置模板：" + fNameSYS)

                                try:
                                    with open(fNameSYS, 'r', encoding='utf-8') as fileSYS:
                                        strSYS = fileSYS.read()
                                        for idx in range(3, len(listData)):
                                            if idx == indexSOFTWARE or idx == indexSYSPAT or idx == indexCFGTEMPLET:
                                                continue

                                            if listTitle[idx].startswith("#"):
                                                if len(listData[idx]) == 0:
                                                    print("字段：" + listTitle[idx] + " 值为空！")
                                                elif listTitle[idx] in strSYS:
                                                    print(f"替换：{listTitle[idx]} 为：{listData[idx]}")
                                                    strSYS = strSYS.replace(listTitle[idx], listData[idx])
                                                else:
                                                    print(f"在配置模板内找不到匹配项：{listTitle[idx]}")

                                        strSYSCONFIG = f"{listData[indexSYSNAME].lower()}_{listData[indexESN].lower()}.cfg"
                                        fNameNewCfg = cfgPath + strSYSCONFIG
                                        print("准备生成配置文件：" + fNameNewCfg)

                                        with open(fNameNewCfg, 'w', encoding='utf-8') as fileNewCfg:
                                            fileNewCfg.write(strSYS)
                                            print("配置文件写入完成")

                                        with open(fnameSMARTINI, 'a', encoding='utf-8') as fileSMARTINI:
                                            fileSMARTINI.write(f"[DEVICE{devSEQ} DESCRIPTION]\n")
                                            fileSMARTINI.write(f"ESN={listData[indexESN].lower()}\n")
                                            fileSMARTINI.write(f"MAC={listData[indexMAC].upper()}\n")
                                            fileSMARTINI.write(f"SYSTEM-SOFTWARE={listData[indexSOFTWARE]}\n")
                                            fileSMARTINI.write(f"SYSTEM-PAT={listData[indexSYSPAT]}\n")
                                            fileSMARTINI.write(f"SYSTEM-CONFIG={strSYSCONFIG}\n")

                                        devSEQ += 1
                                except FileNotFoundError:
                                    print("配置模板文件打开失败：" + fNameSYS)
                                    return
                            else:
                                print("数据行与表头行数据不一致，可能存在空值!")
        except FileNotFoundError:
            print("模板文件打开失败：" + fileName)
            return

        with open(fnameSMARTINI, 'a', encoding='utf-8') as fileSMARTINI:
            fileSMARTINI.write("END LSW\n")

def main():
    parser = argparse.ArgumentParser(description="处理CSV文件并生成配置文件和索引文件。")
    parser.add_argument("file", help="要处理的CSV文件路径")
    args = parser.parse_args()

    process_file(args.file)

if __name__ == "__main__":
    main()