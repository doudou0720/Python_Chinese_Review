import flask
import logging

class ToExts:
    """
    传入拓展的参数集合
    """
    def __init__(self,app:flask.Flask,FileHandler:logging.FileHandler,StreamHandler:logging.StreamHandler) -> None:
        self.app = app
        self.FileHandler = FileHandler
        self.StreamHandler = StreamHandler
        # self.run_dir = run_dir
        formatter = logging.Formatter("%(asctime)s - %(filename)s(%(name)s)[line:%(lineno)d] - %(levelname)s: %(message)s")
        self.FileHandler.setFormatter(formatter)
        self.StreamHandler.setFormatter(formatter)
    
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