# -*- coding: utf-8 -*-
# author: elvin


import requests
import subprocess
import re
from config import index_url, download_url, chrome_location


class DriverUpdater(object):

    def __init__(self):

        self.get_version()

    def get_version(self):

        for part in chrome_location:

            cmd = r'wmic datafile where name="{}" get Version /value'
            cmd = cmd.format(part)
            output = subprocess.getoutput(cmd)

            if "=" in output:
                self.current_version = output.strip().split("=")[1]
                print("Chrome Location: {}\nChrome Version: {}".format(
                    part, self.current_version))
                break

    def download_driver(self):

        global download_url

        r = requests.get(index_url) # 获取版本号列表
        pattern = re.compile(r'{}[0-9\.]+'.format(self.current_version.split('.')[0])) # 根据当前浏览器版本号匹配驱动版本号
        driver_version = pattern.findall(r.text)[-1]
        print("Driver Version: {}".format(driver_version))

        target_url = download_url.format(driver_version)
        # print(target_url)
        r = requests.get(url=target_url)

        with open("chromedriver_win32.zip", "wb") as file:
            print("开始下载...", end="")
            file.write(r.content)
            print("下载完成")


def main():
    updater = DriverUpdater()
    updater.download_driver()

    subprocess.Popen("pause", shell=True)


if __name__ == "__main__":
    main()
