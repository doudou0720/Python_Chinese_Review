import flask
import logging

class ToExts:
    """
    传入拓展的参数集合
    """
    def __init__(self,app:flask.Flask,FileHandler:logging.FileHandler,StreamHandler:logging.StreamHandler) -> None:
        """
        绑定数据
        app : Flask App
        FileHandler : logging 文件流
        StreamHandler : logging 输出流
        """
        self.app = app
        self.FileHandler = FileHandler
        self.StreamHandler = StreamHandler
        # self.run_dir = run_dir
    
    def create_logger(self,ext_name:str,level = logging.INFO) -> logging.Logger:
        """
        生成logger
        ext_name:拓展名
        level:Logger等级
        """
        tmp = logging.getLogger('EXT('+ext_name+')')
        tmp.setLevel(level)
        tmp.addHandler(self.FileHandler)
        tmp.addHandler(self.StreamHandler)

        return tmp

    def GetSubLogger(self,parent_logger:logging.Logger,subname:str,level=None) -> logging.Logger:
        """
        生成子logger
        parent_logger:父Logger
        subname:子模块名称
        level:Logger等级
        """
        tmp = logging.getLogger('EXT('+parent_logger.name[4:-1]+')-Sub('+subname+')')
        if level == None:
            level = parent_logger.level
        tmp.setLevel(level)
        tmp.addHandler(self.FileHandler)
        tmp.addHandler(self.StreamHandler)

        return tmp
