# import sys
# print(sys.path)

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from datetime import datetime
# import re
import time
import json
import os
import shutil

class Seashell0daydownW:
    def __init__(self, stopurl):
        self.stopurl = stopurl
        self.done = False
        self.pt = 3
        self.ditems = []

    # def obj_dict(obj):
    #     return obj.__dict__

    def process(self):

        options = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--headless")
        # options.binary_location = "C:/Users/seashell/Desktop/cr-stable/bin/chrome.exe"
        driver = webdriver.Chrome(options=options)
        drv = webdriver.Chrome(options=options)

        driver.implicitly_wait(self.pt)
        drv.implicitly_wait(self.pt)

        f = open('urls-0daydown-Windows.txt', 'a', encoding="utf-8")
        fb = open('urls-0daydown-Windows1.txt', 'a', encoding="utf-8")

        i = 1
        while not self.done:
            start_i = "https://www.0daydown.com/category/software/windows/page/" + str(i)
            print("\n")
            print(start_i)
            driver.get(start_i)
            elems = driver.find_elements_by_class_name("thumbnail")

            if len(elems) == 0:
                break

            for elem in elems:

                url = elem.get_attribute('href')
                if url == self.stopurl:
                    self.done = True
                    print("Meet last done")
                    break

                # print(elem.get_attribute("href"))

                self.processitem(drv, elem, f, fb)
                time.sleep(0.5)
            i += 1

        f.close()
        drv.close()
        driver.close()

        fb = open('urls-0daydown-Windows.json', 'a', encoding="utf-8")
        fb.write(json.dumps([ob.__dict__ for ob in self.ditems], ensure_ascii=False))
        fb.close()

    def processitem(self, driver, elem, f, fb):
        ditem = Ditem()

        itemurl = elem.get_attribute("href")
        driver.get(itemurl)

        title = elem.find_element_by_css_selector('img').get_attribute('alt')
        f.write('*' * 50 + '\n')
        f.write(title)
        f.write('\n')
        f.write(itemurl)
        f.write('\n' + '*' * 50 + '\n')

        ditem.title = title
        ditem.url = itemurl

        print(title)

        elems = driver.find_elements_by_class_name("external")

        for e in elems:
            dlink = e.get_attribute("href")

            if "pan.baidu.com" in dlink:
                f.write('###\n\n')
                # rstr = e.find_element_by_xpath('..').text \
                #     .replace("Download 百度云", "\n") \
                #     .replace("链接: ", "\n") \
                #     .replace(" 密码: ", "\n")\
                #     .replace(" 提取码: ", "\n")
                rstr = e.find_element_by_xpath('..').text \
                    .replace("Download 百度云", "")
                f.write(rstr.strip())
                f.write('\n\n###')
                if ditem.bdurl == "":
                    ditem.bdurl = rstr.strip()
                    fb.write(rstr.strip())
                    fb.write("\n")
            else:
                f.write(dlink)
                if ("nitroflare.com" in dlink) and (ditem.bdurl == ""):
                    ditem.filenames.append(dlink.split('/')[-1])
            f.write('\n')
        f.write('\n')
        self.ditems.append(ditem)


class Ditem:
    DEST = "/download/@@@@@@MMMMMM/batch/111/"

    def __init__(self):
        self.title = ""
        self.url = ""
        self.bdurl = ""
        self.filenames = []

    @staticmethod
    def folderfiles(mypath):
        with open('urls-0daydown-Windows.json', 'rb') as json_file:
            data = json.load(json_file)
            for i in data:
                if (len(i['filenames']) > 0) and (len(i['bdurl']) > 0):
                    directory = mypath + i['title'].replace("/", " ")
                    for j in i['filenames']:
                        if os.path.exists(mypath + j):
                            if not os.path.exists(directory):
                                os.makedirs(directory)
                            os.rename(mypath + j, directory + "/" + j)
                        j = j.replace("_", " ")
                        if os.path.exists(mypath + j):
                            if not os.path.exists(directory):
                                os.makedirs(directory)
                            os.rename(mypath + j, directory + "/" + j)

    @staticmethod
    def folderunfolderfiles(mypath):
        for (dirpath, dirnames, filenames) in os.walk(mypath):
            for x in filenames:
                # print(x)
                # print(os.path.splitext(x)[0])

                nx = x.replace("_Getintopc.com_", "").replace("[FTUApps.com] -", "").replace("_Downloadly.ir", "").strip()
                directory = mypath + os.path.splitext(nx)[0]
                directory = directory.replace("_", ".") \
                    .replace("Downloadly.ir", "") \
                    .replace("[FileCR]", "").strip()
                # directory += " _"

                if not os.path.exists(directory):
                    os.makedirs(directory)
                os.rename(mypath + x, directory + "/" + nx)
            break

    @staticmethod
    def replaceinfolder(mypath, oldstr, newstr):
        for subdir, dirs, files in os.walk(mypath):
            for diritem in dirs:
                newname = diritem.replace(oldstr, newstr).strip()
                if diritem != newname:
                    os.rename(mypath + diritem, mypath + newname)

    @staticmethod
    def movefolde2folder(sourcepath,destpath):
        filenames= os.listdir(sourcepath)
        print(f"count: {len(filenames)}")

        count = 0
        for f in filenames:

            # print(f"{count}: {sourcepath+f}")
            cpt = sum([len(d) for r, d, f in os.walk(sourcepath+f)])
            if cpt==0:
                count=count+1
                print(f"{count}: {sourcepath+f}")
                filenames= os.listdir(sourcepath+f)
                print(os.path.splitext(filenames[0])[0])
                shutil.move(sourcepath+f, destpath+os.path.splitext(filenames[0])[0])

            # for file in os.listdir((sourcepath+f)):
            #
            #     cpt = sum([len(d) for r, d, f in os.walk("G:\CS\PYTHONPROJECTS")])
            #     print(f"{count}: {sourcepath+f+'/'+file}")


            #
            # if cpt ==1:
                # print(sourcepath+f)
                # for r, d, files in os.walk(sourcepath+f):
                #     if len(files)>0:
                #         print(files)
                # shutil.move(sourcepath+f, destpath+f)


                # if len(dirs)==0 and len(files)==1 :
                #     print(sourcepath+f+"/"+files[0])
                #     os.rename(sourcepath+f+"/"+files[0], destpath + files[0])
                # break



        # for (dirpath, dirnames, filenames) in os.walk(sourcepath):
        #     for dir in dirnames:
        #         print(dir)
            #
            # # print(f"d:{len(dirnames)}, f:{len(filenames)}")
            # if len(dirnames)==0 and len(filenames)==1 :
            #     print(dirpath+filenames[0])
            #     # os.rename(sourcepath + filenames[0], destpath + filenames[0])

# mob = Seashell0daydownW("https://www.0daydown.com/02/1001971.html")
# mob.process()
# ff = Ditem()
# ff.folderfiles("/download/@@@@@@MMMMMM/batch/")
# ff.folderUnFolderFiles('/download/0days/')
# Ditem.movefolde2folder('/download/00000jd/000book/@@@@NulledPremium.com/','/download/00000jd/000day/@@@@@SSSSSSSSS/')
Ditem.folderunfolderfiles('/download/00000jd/000day/@@@@@SSSSSSSSS/')
