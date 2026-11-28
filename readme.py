import re
import os
from typing import List

from loguru import logger

class Rule(object):
    def __init__(self, name:str, type:str, url:str, latest:str, update:bool=False):
        self.name = name
        self.filename = self.name.replace(' ', '_') + '.txt'
        self.type = type
        self.url = url
        self.latest = latest
        self.update = update

# redme文件操作
class ReadMe(object):
    def __init__(self, filename:str):
        self.filename = filename
        self.ruleList:List[Rule] = []
        self.proxyList = [
            "",
            "https://gh-proxy.com",
            "https://ghfast.top",
            "https://github.boki.moe"
        ]

    def getRules(self) -> List[Rule]:
        logger.info("resolve readme...")
        self.ruleList = []
        with open(self.filename, "r") as f:
            for line in f:
                line = line.replace('\r', '').replace('\n', '')
                if line.find('|')==0 and line.rfind('|')==len(line)-1:
                    rule = list(map(lambda x: x.strip(), line[1:-1].split('|')))
                    if rule[2].find('(') > 0 and rule[2].find(')') > 0 and rule[1].find('(') < 0:
                        url = rule[2][rule[2].find('(')+1:rule[2].find(')')]
                        matchObj1 = re.match(r'(http|https)://[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?', url)
                        if matchObj1:
                            self.ruleList.append(Rule(rule[0], rule[1], url, rule[-1]))
        return self.ruleList

    def getRulesNames(self) -> str:
        names = ""

        for rule in self.ruleList:
            names += rule.name + '、'

        return names[:-1]

    def setRules(self, ruleList:List[Rule]):
        self.ruleList = ruleList

    def __subscribeLink(self, fileName:str, tag:str, url:str=None):
        link = ""

        if tag == "rule":
            link += " [原始链接](https://raw.githubusercontent.com/C9LG/Blocklists/dist/%s) |" % (fileName)

            for i in range(1, len(self.proxyList)):
                proxy = self.proxyList[i]
                link += " [加速链接%d](%s/https://raw.githubusercontent.com/C9LG/Blocklists/dist/%s) |" % (i, proxy, fileName)
        else:
            if url:
                link += " [原始链接](%s) |" % (url)
            else:
                link += " [原始链接](https://github.com/C9LG/Blocklists/releases/download/%s/%s) |" % (tag, fileName)

            for i in range(1, len(self.proxyList)):
                proxy = self.proxyList[i]
                link += " [加速链接%d](%s/https://github.com/C9LG/Blocklists/releases/download/%s/%s) |" % (i, proxy, tag, fileName)

        return link

    def regenerate(self):
        logger.info("regenerate readme...")
        if os.path.exists(self.filename):
            os.remove(self.filename)

        with open(self.filename, 'a') as f:
            f.write("## 订阅链接\n")
            f.write("1. 规则 x′ 为规则 x 的 Lite 版，仅拦截国内域名，体积较小\n")
            f.write("2. AdGuard 等浏览器插件应使用“规则1 + 规则2”；规则2 为规则1 的补充，仅适用于浏览器插件\n")
            f.write("\n")
            tmp = "| 规则 | 原始链接 |"
            for i in range(1, len(self.proxyList)):
                tmp += " 加速链接%d |" % (i)
            tmp += " 适配说明 |\n"
            f.write(tmp)
            tmp = "|" + ":-|" * ( 2 + len(self.proxyList)) + "\n"
            f.write(tmp)
            f.write("| 规则1 |" + self.__subscribeLink("adblockdns.txt", "rule") + " AdGuard、AdGuard Home 等 |\n")
            f.write("| 规则1' |" + self.__subscribeLink("adblockdnslite.txt", "rule") + " AdGuard、AdGuard Home 等 |\n")
            f.write("| 规则2 |" + self.__subscribeLink("adblockfilters.txt", "rule") + " AdGuard 等 |\n")
            f.write("| 规则2' |" + self.__subscribeLink("adblockfilterslite.txt", "rule") + " AdGuard 等 |\n")
            # f.write("| 规则3 |" + self.__subscribeLink("adblockdomain.txt", "rule") + " InviZible Pro、personalDNSfilter |\n")
            # f.write("| 规则3' |" + self.__subscribeLink("adblockdomainlite.txt", "rule") + " InviZible Pro、personalDNSfilter |\n")
            # f.write("| 规则4 |" + self.__subscribeLink("adblockdnsmasq.txt", "rule") + " DNSMasq |\n")
            # f.write("| 规则4' |" + self.__subscribeLink("adblockdnsmasqlite.txt", "rule") + " DNSMasq |\n")
            # f.write("| 规则5 |" + self.__subscribeLink("adblocksmartdns.conf", "rule") + " SmartDNS |\n")
            # f.write("| 规则5' |" + self.__subscribeLink("adblocksmartdnslite.conf", "rule") + " SmartDNS |\n")
            # f.write("| 规则6 |" + self.__subscribeLink("adblockclash.list", "rule") + " Shadowrocket |\n")
            # f.write("| 规则6' |" + self.__subscribeLink("adblockclashlite.list", "rule") + " Shadowrocket |\n")
            # f.write("| 规则7 |" + self.__subscribeLink("adblockshadowrocket.sgmodule", "rule") + " Shadowrocket Module |\n")
            # f.write("| 规则7' |" + self.__subscribeLink("adblockshadowrocketlite.sgmodule", "rule") + " Shadowrocket Module |\n")
            # f.write("| 规则8 |" + self.__subscribeLink("adblockqx.conf", "rule") + " QuantumultX |\n")
            # f.write("| 规则8' |" + self.__subscribeLink("adblockqxlite.conf", "rule") + " QuantumultX |\n")
            # f.write("| 规则9 |" + self.__subscribeLink("adblockmihomo.yaml", "rule") + " Clash Meta(Mihomo) yaml |\n")
            # f.write("| 规则9' |" + self.__subscribeLink("adblockmihomolite.yaml", "rule") + " Clash Meta(Mihomo) yaml |\n")
            # f.write("| 规则10 |" + self.__subscribeLink("adblockmihomo.mrs", "rule") + " Clash Meta(Mihomo) mrs |\n")
            # f.write("| 规则10' |" + self.__subscribeLink("adblockmihomolite.mrs", "rule") + " Clash Meta(Mihomo) mrs |\n")
            # f.write("| 规则11 |" + self.__subscribeLink("adblockhosts.txt", "rule") + " Hosts |\n")
            # f.write("| 规则11' |" + self.__subscribeLink("adblockhostslite.txt", "rule") + " Hosts |\n")
            # f.write("| 规则12 |" + self.__subscribeLink("adblocksingbox.json", "rule") + " sing-box 1.12+ json |\n")
            # f.write("| 规则12' |" + self.__subscribeLink("adblocksingboxlite.json", "rule") + " sing-box 1.12+ json |\n")
            # f.write("| 规则13 |" + self.__subscribeLink("adblocksingbox.srs", "rule") + " sing-box 1.12+ srs |\n")
            # f.write("| 规则13' |" + self.__subscribeLink("adblocksingboxlite.srs", "rule") + " sing-box 1.12+ srs |\n")
            # f.write("| 规则14 |" + self.__subscribeLink("adblockloon.list", "rule") + " Loon |\n")
            # f.write("| 规则14' |" + self.__subscribeLink("adblockloonlite.list", "rule") + " Loon |\n")
            # f.write("| 规则15 |" + self.__subscribeLink("adblocksurge.list", "rule") + " Surge |\n")
            # f.write("| 规则15' |" + self.__subscribeLink("adblocksurgelite.list", "rule") + " Surge |\n")
            # f.write("| 规则16 |" + self.__subscribeLink("adblockmosdns.txt", "rule") + " MosDNS |\n")
            # f.write("| 规则16' |" + self.__subscribeLink("adblockmosdnslite.txt", "rule") + " MosDNS |\n")
            f.write("| 规则17 |" + self.__subscribeLink("adblockv2ray.dat", "rule") + " V2ray、Xray(category-ads-all) |\n")
            f.write("| 规则17' |" + self.__subscribeLink("adblockv2raylite.dat", "rule") + " V2ray、Xray(category-ads-all) |\n")
            f.write("\n")

            f.write("## 上游规则源\n")
            f.write("\n")

            tmp = "| 规则 | 类型 | 原始链接 |"
            for i in range(1, len(self.proxyList)):
                tmp += " 加速链接%d |" % (i)
            tmp += " 更新日期 |\n"
            f.write(tmp)
            tmp = "|" + ":-|" * ( 2 + len(self.proxyList) + 1) + "\n"
            f.write(tmp)
            for rule in self.ruleList:
                f.write("| %s | %s |%s %s |\n" % (rule.name, rule.type, self.__subscribeLink(rule.filename, "source", rule.url), rule.latest))
            f.write("\n")
