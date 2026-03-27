#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{

    ui->setupUi(this);

    connect(ui->actionOpenFile, SIGNAL(triggered()), this, SLOT(slot_pro_openfile()));
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::slot_pro_openfile()
{
    QString strTIMESN = QDateTime::currentDateTime().toString("yyyymmdd.hhmmss");

    //    ui->info->appendPlainText("摸鱼");
    QString fileName = QFileDialog::getOpenFileName(this, tr("打开配置模板文件"),
                                                    "",
                                                    tr("moudle (*.csv)"));
    if(fileName.size() >= 5)
    {
        ui->info->appendPlainText("准备处理模板文件：" + fileName);
        QFile file(fileName);
        if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
        {
            ui->info->appendPlainText("模板文件打开失败：" + fileName);
            return;
        }

        QFileInfo fileInfo(fileName);
        QString cfgPath=fileInfo.absolutePath() + "/";
        QString fnameSMARTINI = cfgPath + "smart_config.ini";
        QFile fileSMARTINI(fnameSMARTINI);
        if (!fileSMARTINI.open(QIODevice::WriteOnly | QIODevice::Text | QIODevice::Truncate))
        {
            ui->info->appendPlainText("创建索引文件失败：" + fnameSMARTINI);
            return;
        }else{
            QString str2write;
            str2write="BEGIN LSW\n[GLOBAL CONFIG]\n";
            fileSMARTINI.write(str2write.toLocal8Bit());

            str2write = "TIMESN="+strTIMESN+"\n";
            fileSMARTINI.write(str2write.toLocal8Bit());

            str2write = "AUTODELFILE=YES\nACTIVEMODE=DEFAULT\n";
            fileSMARTINI.write(str2write.toLocal8Bit());


            ui->info->appendPlainText("索引文件全局配置写入完成");
        }

        int lineNO=0;
        int devSEQ=0;
        int indexSYSNAME=0;
        int indexESN=0;
        int indexSOFTWARE=0;
        int indexSYSPAT=0;
        int indexMAC=0;
        int indexCFGTEMPLET=0;
        QStringList listTitle;

        while (!file.atEnd()) {
            QByteArray line = file.readLine();
            lineNO+=1;
            ui->info->appendPlainText(QString::number(lineNO) + ":" + QString(line) );

            QString strLine(line);
            QStringList listItems = strLine.split(",");
            if (listItems.size() > 4)
            {
                if(1 == lineNO)
                {
                    ui->info->appendPlainText("处理表头：" + strLine);
                    indexSYSNAME = listItems.indexOf("#SYSNAME#");
                    indexESN = listItems.indexOf("#ESN#");
                    indexMAC = listItems.indexOf("#MAC-ADDRESS#");
                    indexSOFTWARE = listItems.indexOf("#SYSTEM-SOFTWARE#");
                    indexSYSPAT = listItems.indexOf("#SYSTEM-PAT#");
                    indexCFGTEMPLET = listItems.indexOf("#CFGTEMPLET#");


                    if((listItems.at(0).trimmed() == "#ORDER#")
                            && (listItems.at(1).trimmed() == "#TIMESN#")
                            && (listItems.at(2).trimmed() == "#SWITCH_MODEL#")
                            && (indexSYSNAME > 0)
                            && (indexESN > 0)
                            && (indexMAC > 0)
                            && (indexSOFTWARE > 0)
                            && (indexSYSPAT > 0)
                            && (indexCFGTEMPLET > 0)
                            )

                    {
                        ui->info->appendPlainText("表头内容校验完毕!"  );
                        listTitle=strLine.split(",",QString::SkipEmptyParts);


                    }else{
                        ui->info->appendPlainText("表头内容不正确!"  );
                    }
                }
                else
                {
                    ui->info->appendPlainText("处理数据行：" + strLine);
                    QStringList listData = strLine.split(",",QString::SkipEmptyParts);
                    if(listData.size() == listTitle.size())
                    {
                        //                        QString strTIMESN = QDateTime::currentDateTime().toString("yyyymmdd.hhmmss");
                        ui->info->appendPlainText("处理设备型号：" + listData.at(2)
                                                  + " SYSNAME:" + listData.at(indexSYSNAME) );
                        QString fNameSYS = cfgPath + listData.at(indexCFGTEMPLET).toLower();
                        ui->info->appendPlainText("准备打开设备配置模板：" + fNameSYS  );


                        QFile fileSYS(fNameSYS);

                        if (!fileSYS.open(QIODevice::ReadOnly | QIODevice::Text))
                        {
                            ui->info->appendPlainText("配置模板文件打开失败：" + fNameSYS);
                            return;
                        }else{
                            QString strSYS(fileSYS.readAll());
                            for (int idx = 3 ; idx < listData.size(); ++idx )
                            {
                                if(idx == indexSOFTWARE)
                                    continue;
                                if(idx == indexSYSPAT)
                                    continue;
                                if(idx == indexCFGTEMPLET )
                                    continue;


                                if(listTitle.at(idx).left(1) == "#")
                                {
                                    if(listData.at(idx).size() == 0)
                                    {
                                        ui->info->appendPlainText("字段：" + listTitle.at(idx) + " 值为空！");
                                    }
                                    else if(strSYS.contains(listTitle.at(idx)))
                                    {

                                        ui->info->appendHtml( QString("<p>")
                                                              + "替换：" +
                                                              QString("<span style='color: blue;'>") + listTitle.at(idx) + QString("</span>")
                                                              + " 为：" +
                                                              QString("<span style='color: green;'>") + listData.at(idx)  + QString("</span>")
                                                              + QString("</p>"));
                                        strSYS.replace(listTitle.at(idx),listData.at(idx));

                                    }else
                                    {
                                        //ui->info->appendPlainText("在配置模板内找不到匹配项：" + listTitle.at(idx));
                                        ui->info->appendHtml( QString("<span style='color: red;'>") + "在配置模板内找不到匹配项：" + listTitle.at(idx) + QString("</span>") );
                                    }
                                }
                            }


                            QString strSYSCONFIG =  listData.at(indexSYSNAME).toLower()
                                    + "_"
                                    + listData.at(indexESN).toLower() + ".cfg";
                            QString fNameNewCfg = cfgPath + strSYSCONFIG;
                            ui->info->appendPlainText("准备生成配置文件：" + fNameNewCfg );

                            QFile fileNewCfg(fNameNewCfg);
                            if (!fileNewCfg.open(QIODevice::WriteOnly | QIODevice::Text | QIODevice::Truncate))
                            {
                                ui->info->appendPlainText("打开配置文件失败：" + fNameNewCfg);
                                return;
                            }else{
                                fileNewCfg.write(strSYS.toLocal8Bit());
                                fileNewCfg.close();
                                ui->info->appendPlainText("配置文件写入完成");
                            }



                            if(fileSMARTINI.isOpen())
                            {
                                QString str2write;
                                str2write="[DEVICE"+ QString::number(devSEQ) + " DESCRIPTION]\n";
                                fileSMARTINI.write(str2write.toLocal8Bit());

                                str2write="ESN=" + listData.at(indexESN).toLower() + "\n";
                                fileSMARTINI.write(str2write.toLocal8Bit());

                                str2write="MAC=" + listData.at(indexMAC).toUpper() + "\n";
                                fileSMARTINI.write(str2write.toLocal8Bit());

                                str2write="SYSTEM-SOFTWARE=" + listData.at(indexSOFTWARE) + "\n";
                                fileSMARTINI.write(str2write.toLocal8Bit());

                                str2write="SYSTEM-PAT=" + listData.at(indexSYSPAT) + "\n";
                                fileSMARTINI.write(str2write.toLocal8Bit());

                                str2write="SYSTEM-CONFIG=" + strSYSCONFIG + "\n";
                                fileSMARTINI.write(str2write.toLocal8Bit());
                            }

                            devSEQ+=1;
                        }

                    }else{
                        ui->info->appendPlainText("数据行与表头行数据不一致，可能存在空值!"  );
                    }

                }
            }




            qApp->processEvents();
            QThread::usleep(200*1000);
        }


        {
            QString str2write;
            str2write="END LSW\n";
            fileSMARTINI.write(str2write.toLocal8Bit());
        }
    }

}
