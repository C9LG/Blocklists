import os
import subprocess
import time


# 删除当前目录下所有的.txt文件
subprocess.run("rm ./data/rules/*.txt", shell=True)

# 创建临时文件夹
os.makedirs("./tmp/", exist_ok=True)

# 复制补充规则到tmp文件夹
#subprocess.run("cp ./data/mod/adblock.txt ./tmp/adblock01.txt", shell=True)
#subprocess.run("cp ./data/mod/whitelist.txt ./tmp/allow01.txt", shell=True)


# 拦截规则
adblock = [
  "https://raw.githubusercontent.com/C9LG/DNS-Blocklists/main/rules/adblockdns.txt", #C9LG_DNS-Blocklists
  "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_Base/filter.txt", #AdguardTeam_Base
  "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_224_Chinese/filter.txt", #AdguardTeam_Chinese
  "https://github.com/AdguardTeam/FiltersRegistry/raw/master/filters/filter_11_Mobile/filter.txt", #AdguardTeam_Mobile
  "https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt", #damengzhu_banad
  "https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt", #xinggsf_MV
  "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_3_Spyware/filter.txt", #AdguardTeam_TrackingProtection
  "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_14_Annoyances/filter.txt", #AdguardTeam_Annoyances
  "https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt", #cjx82630_CJX-Annoyances
  "https://secure.fanboy.co.nz/fanboy-annoyance.txt", #ryanbr_Fanboy-Annoyances
  "https://raw.githubusercontent.com/Noyllopa/NoAppDownload/master/NoAppDownload.txt", #Noyllopa_NoAppDownload
  "https://easylist.to/easylist/easyprivacy.txt", #EasyList_EasyPrivacy
  "https://easylist-downloads.adblockplus.org/antiadblockfilters.txt", #EasyList_AdblockWarningRemovalList
  "https://malware-filter.gitlab.io/malware-filter/phishing-filter-ag.txt" #malware-filter_Phishing URL Blocklist
]

# 白名单规则
allow = [
]

# 下载
for i, adblock_url in enumerate(adblock):
    subprocess.Popen(f"curl -m 60 --retry-delay 2 --retry 5 -k -L -C - -o tmp/adblock{i}.txt --connect-timeout 60 -s {adblock_url} | iconv -t utf-8", shell=True).wait()
    time.sleep(1)

for j, allow_url in enumerate(allow):
    subprocess.Popen(f"curl -m 60 --retry-delay 2 --retry 5 -k -L -C - -o tmp/allow{j}.txt --connect-timeout 60 -s {allow_url} | iconv -t utf-8", shell=True).wait()
    time.sleep(1)
    
print('规则下载完成')
