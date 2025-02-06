import logging
from multiprocessing import context
import string
import alive_progress

class Installer :
    DataBase = 0
    Static = 1
    Templates = 2
    Data = 3
    Python_package = 4
    Json = 5

    package_name = "none.none"

    context={
        
    }

    def __init__(self,name:string):
        """
        name:软件包名
        """
        self.package_name = name
    
    def install(type:int,s:string,logger:logging):
        """
        type : 类型
        s : 内容
        logger : logger 日志
        """
        pass

