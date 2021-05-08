import datetime
import json
import os
import shutil

from apkutils2 import APK
from apkutils2.apkfile import BadZipFile


class Ditem:
    def __init__(self, dirname):
        self.dirname = dirname
        self.isData = True
        self.isfailed = False
        self.ver = ''

        apk = APK(dirname)

        try:
            m_dict = apk.get_manifest()
        except:
            self.isfailed = True
            return

        if not m_dict:
            self.isData = False
            return

        self.package = m_dict['@package']
        if '@android:versionName' in m_dict:
            self.ver=m_dict['@android:versionName']
        elif '@versionName' in m_dict:
            self.ver=m_dict['@versionName']
        elif '@versionCode' in m_dict:
            self.ver=m_dict['@android:versionCode']

        if '@android:label' in m_dict['application']:
            self.label=m_dict['application']['@android:label']
        elif '@label' in m_dict:
            self.label=m_dict['application']['@label']

        statbuf = os.stat(dirname)
        self.mtime = statbuf.st_mtime

def showFile(dirname):
    apk = APK(dirname)

    # m_xml = apk.get_org_manifest()
    # print(m_xml)

    # m_dict = apk.get_manifest()
    # print(json.dumps(m_dict, indent=1))
    #
    # f = open('phone-result.json', 'w', encoding="utf-8")
    # f.write(json.dumps(m_dict, indent=1))
    # f.close()

    item= Ditem(dirname)

    # get any item you want from dict
    print('package:', item.package)
    print('android:versionName:', item.ver)
    print('label:', item.label)

apkdict = {}

def processDir(mypath):
    for (dirpath, dirnames, filenames) in os.walk(mypath):
        count=0
        for x in filenames:
            count=count+1
            if not x.lower().endswith('.apk'):
                moveFile(dirpath+x,'done')
                continue
            # processFile(dirpath+x)
            print('{} : {}'.format(count,x))
            item= Ditem(dirpath+x)

            if not item:
                moveFile(dirpath+x,'delete')
                continue

            if item.isfailed:
                # os.remove(item.dirname)
                moveFile(dirpath+x,'delete')
                continue

            if not item.isData:
                moveFile(dirpath+x,'delete')
                continue

            if not item.package in apkdict:
                apkdict[item.package]= [item]
            else:
                apkdict[item.package].append(item)
        break

    f = open('phone-result.txt', 'w', encoding="utf-8")

    for package in apkdict:
        items = apkdict[package]
        if len(items)<2:
            moveFile(items[0].dirname,'done')
            continue

        items.sort(key=lambda x: x.mtime, reverse=True)
        items.sort(key=lambda x: x.ver, reverse=True)

        # items.sort(key = lambda obj: ([(-ord(c) for c in obj.ver)], -obj.mtime))
        f.write('@@{}\n'.format(package))
        fstr = '{}@{}@{}\n'
        isfirst =True
        for item in items:
            f.write(fstr.format(item.ver,datetime.datetime.fromtimestamp(item.mtime),item.dirname))
            if isfirst:
                fstr = '@'+fstr
                isfirst = False
        f.write('\n')

    f.close()

def moveFile(dirname,dir):
    dirname = dirname.strip()
    org_path = os.path.dirname(dirname)
    dst_path = org_path+'/'+dir+ '/'+os.path.basename(dirname)

    print(dirname)
    print(dst_path)
    try:
        os.replace(dirname, dst_path)
    except:
        pass


def processResult():
    filepath = 'phone-result.txt'
    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            if len(line.strip())==0:
                continue
            if line.startswith('@@'):
                continue
            if line.startswith('@'):
                print("Line {}: {}".format(cnt, line))
                print(line.split('@')[-1])
                moveFile(line.split('@')[-1],'delete')
            else:
                moveFile(line.split('@')[-1],'done')

def processDirAPKName(mypath):
    for (dirpath, dirnames, filenames) in os.walk(mypath):
        count=0
        for x in filenames:
            count=count+1
            if not x.lower().endswith('.apk'):
                continue
            # processFile(dirpath+x)
            print('{} : {}'.format(count,x))
            item= Ditem(dirpath+x)

            if not item:
                continue

            if item.isfailed:
                continue

            if not item.isData:
                continue

            newname = item.label+" "+item.ver+'.apk'
            if not newname.startswith('@'):
                os.rename(dirpath+x,dirpath+newname)
        break


# showFile('/download/00000jd/000ph/Manager APK.v8.1.0.p.apk')
# processDir('/download/00000jd/000ph/')
processResult()
# processDirAPKName('/download/00000jd/000ph/')
