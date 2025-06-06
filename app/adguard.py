import os
from typing import List, Set, Dict

from loguru import logger

from app.base import APPBase

class AdGuard(APPBase):
    def __init__(self, blockList:List[str], unblockList:List[str], filterDict:Dict[str,str], filterList:List[str], filterList_var:List[str], ChinaSet:Set[str], fileName:str, sourceRule:str):
        super(AdGuard, self).__init__(blockList, unblockList, filterDict, filterList, filterList_var, ChinaSet, fileName, sourceRule)

    def generate(self, isLite=False):
        try:
            if isLite:
                logger.info("generate adblock AdGuard Lite...")
                fileName = self.fileNameLite
                filterList = self.filterListLite
            else:
                logger.info("generate adblock AdGuard...")
                fileName = self.fileName
                filterList = self.filterList
            
            if os.path.exists(fileName):
                os.remove(fileName)
            
            # 生成规则文件
            with open(fileName, 'a') as f:
                f.write("!\n")
                if isLite:
                    f.write("! Title: AdBlock Filter Lite\n")
                    f.write("! Description: 适用于 AdGuard 的去广告合并规则。Lite 版仅针对国内域名拦截。\n")
                else:
                    f.write("! Title: AdBlock Filter\n")
                    f.write("! Description: 适用于 AdGuard 的去广告合并规则。\n")
                f.write("! Homepage: %s\n"%(self.homepage))
                f.write("! Source: %s/%s\n"%(self.source, os.path.basename(fileName)))
                f.write("! Version: %s\n"%(self.version))
                f.write("! Last modified: %s\n"%(self.time))
                f.write("! Blocked Filters: %s\n"%(len(filterList)))
                f.write("!\n")
                for fiter in self.filterList_var:
                    f.write("%s\n"%(fiter))
                for fiter in filterList:
                    f.write("%s\n"%(fiter))
            
            if isLite:
                logger.info("adblock AdGuard Lite: block=%d"%(len(filterList)))
            else:
                logger.info("adblock AdGuard: block=%d"%(len(filterList)))
        except Exception as e:
            logger.error("%s"%(e))
