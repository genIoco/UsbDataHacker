import sys
import os
import numpy as np
import matplotlib.pyplot as plt


class MouseDataHacker:
    def __init__(self) -> None:
        self.pcapFilePath = "./example/usb_raw.pcapng"
        self.action = "LEFT"
        self.X = []
        self.Y = []
        self.fieldValue = "usb.capdata"
        self.fieldValue = "usbhid.data"
        self.dataFile = "./example/usbdata.txt"

    def GetData(self) -> None:
        cmd = "\"C:\\Program Files\\Wireshark\\tshark\" -r %s -T fields -e %s > %s" % (
            self.pcapFilePath, self.fieldValue,self.dataFile)
        print(cmd)
        os.system(cmd)

    def AnalyzeData(self) -> None:
        mousePositionX = 0
        mousePositionY = 0
        with open(self.dataFile, 'r') as f:
            for line in f:
                if line =="":
                    continue
                line= line.strip()
                # tshark版本原因，导出数据格式可能会带有':'
                if ':' in line:
                    Bytes=line.split(':')
                else:
                    Bytes = [line[i:i+2] for i in range(0,len(line),2)]
                if len(Bytes) == 9:
                    horizontal = 3  # -
                    vertical = 5  # |
                elif len(Bytes) == 6:
                    horizontal = 1  # -
                    vertical = 3  # |
                elif len(Bytes) == 4:
                    horizontal = 1  # -
                    vertical = 2  # |
                else:
                    continue
                offsetX = int(Bytes[horizontal], 16)
                offsetY = int(Bytes[vertical], 16)
                if offsetX > 127:
                    offsetX -= 256
                if offsetY > 127:
                    offsetY -= 256
                mousePositionX += offsetX
                mousePositionY += offsetY
                if Bytes[1] == "01":
                    print("[+] Left butten.")
                    if self.action == "LEFT":
                        # draw point to the image panel
                        self.X.append(mousePositionX)
                        self.Y.append(-mousePositionY)
                elif Bytes[1] == "02":
                    print("[+] Right Butten.")
                    if self.action == "RIGHT":
                        # draw point to the image panel
                        self.X.append(mousePositionX)
                        self.Y.append(-mousePositionY)
                elif Bytes[1] == "00":
                    print("[+] Move.")
                    if self.action == "MOVE":
                        # draw point to the image panel
                        self.X.append(mousePositionX)
                        self.Y.append(-mousePositionY)
                else:
                    print("[-] Known operate.")
                    
                if self.action == "ALL":
                    # draw point to the image panel
                    self.X.append(mousePositionX)
                    self.Y.append(-mousePositionY)

    def ShowData(self):
        """
        根据坐标，展示鼠标轨迹
        """
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.set_title('[%s]-[%s]' % (self.pcapFilePath, self.action))
        ax1.scatter(self.X, self.Y, c='r')
        plt.show()

#TODO #1
class KeyDataHacker:
    def __init__(self) -> None:
        #Keyboard Traffic Dictionary
        self.normalKeys = {"04": "a", "05": "b", "06": "c", "07": "d", "08": "e", "09": "f", "0a": "g", "0b": "h", "0c": "i", "0d": "j", "0e": "k", "0f": "l", "10": "m", "11": "n", "12": "o", "13": "p", "14": "q", "15": "r", "16": "s", "17": "t", "18": "u", "19": "v", "1a": "w", "1b": "x", "1c": "y", "1d": "z", "1e": "1", "1f": "2", "20": "3", "21": "4", "22": "5", "23": "6", "24": "7", "25": "8", "26": "9",
                           "27": "0", "28": "<RET>", "29": "<ESC>", "2a": "<DEL>", "2b": "\t", "2c": "<SPACE>", "2d": "-", "2e": "=", "2f": "[", "30": "]", "31": "\\", "32": "<NON>", "33": ";", "34": "'", "35": "<GA>", "36": ",", "37": ".", "38": "/", "39": "<CAP>", "3a": "<F1>", "3b": "<F2>", "3c": "<F3>", "3d": "<F4>", "3e": "<F5>", "3f": "<F6>", "40": "<F7>", "41": "<F8>", "42": "<F9>", "43": "<F10>", "44": "<F11>", "45": "<F12>"}

        #Press shift
        self.shiftKeys = {"04": "A", "05": "B", "06": "C", "07": "D", "08": "E", "09": "F", "0a": "G", "0b": "H", "0c": "I", "0d": "J", "0e": "K", "0f": "L", "10": "M", "11": "N", "12": "O", "13": "P", "14": "Q", "15": "R", "16": "S", "17": "T", "18": "U", "19": "V", "1a": "W", "1b": "X", "1c": "Y", "1d": "Z", "1e": "!", "1f": "@", "20": "#", "21": "$", "22": "%", "23": "^", "24": "&", "25": "*",
                          "26": "(", "27": ")", "28": "<RET>", "29": "<ESC>", "2a": "<DEL>", "2b": "\t", "2c": "<SPACE>", "2d": "_", "2e": "+", "2f": "{", "30": "}", "31": "|", "32": "<NON>", "33": "\"", "34": ":", "35": "<GA>", "36": "<", "37": ">", "38": "?", "39": "<CAP>", "3a": "<F1>", "3b": "<F2>", "3c": "<F3>", "3d": "<F4>", "3e": "<F5>", "3f": "<F6>", "40": "<F7>", "41": "<F8>", "42": "<F9>", "43": "<F10>", "44": "<F11>", "45": "<F12>"}



def main():
    m=MouseDataHacker()
    m.GetData()
    m.AnalyzeData()
    m.ShowData()


if __name__ == "__main__":
    main()
