#logging 一共有6个级别，NOTSET值为0、DEBUG值为10、INFO值为20、WARNING值为30、ERRO值为40、CRITICAL值为50，这些级别用处在于，logging模块发出
#信息级别高于定义的级别，将在标准输出（屏幕）显示出来。发出的信息级别低于定义级别则略过。若未定义级别，则默认级别WARNING。
#这个函数指定的参数有：
# filename,filemode(缺省为a\w),format,datefmt,level,stream(用于指定stream创建streamhandler，
#                                   指定输出到sys.stderr,sys.stdout，或者文件，默认为sys.stderr)
# %(name)s Logger的名字
# %(levelno)s 数字形式的日志级别
# %(levelname)s 文本形式的日志级别
# %(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
# %(filename)s 调用日志输出函数的模块的文件名
# %(module)s 调用日志输出函数的模块名|
# %(funcName)s 调用日志输出函数的函数名|
# %(lineno)d 调用日志输出函数的语句所在的代码行
# %(created)f 当前时间，用UNIX标准的表示时间的浮点数表示|
# %(relativeCreated)d 输出日志信息时的，自Logger创建以来的毫秒数|
# %(asctime)s 字符串形式的当前时间。默认格式是“2003-07-08 16:49:45,896”。逗号后面的是毫秒
# %(thread)d 线程ID。可能没有
# %(threadName)s 线程名。可能没有
# %(process)d 进程ID。可能没有
# %(message)s 用户输出的消息


import logging
import getpass
import sys

class TestLogging(object):
    def __init__(self):
        logFormat='%(asctime)-12s %(levelname)-8s %(name)-10s %(message)-12s'
        logFileName='./testLog.txt'

        logging.basicConfig(level=logging.INFO,format=logFormat,filename=logFileName,filemode='w')

        logging.debug('debug message')
        logging.info('info.message')
        logging.warning('warning message')
        logging.error('erro message')
        logging.critical('critical message')

#自定义我的log类

class MyLog(object):
    '''这个类用于创建一个自用的log'''
    def __init__(self,logFile):
        user=getpass.getuser()
        self.logger=logging.getLogger(user)
        self.logger.setLevel(logging.DEBUG)
        # self.logFile=logFile
        # logFile='./'+sys.argv[0][0:-3]+'.log' #日志文件名
        # logFile=input('input log_file:')
        
        formatter=logging.Formatter('%(asctime)-12s %(levelname)-8s %(name)-10s %(message)-12s')
        '''日志显示到屏幕上并输出到日志文件内'''
        logHand=logging.FileHandler(logFile)
        logHand.setFormatter(formatter)

        logHand.setLevel(logging.ERROR) #只有错误才会被记录到logfile中

        logHandSt=logging.StreamHandler()
        logHandSt.setFormatter(formatter)
        self.logger.addHandler(logHand)
        self.logger.addHandler(logHandSt)

    def debug(self,msg):
        self.logger.debug(msg)
    
    def info(self,msg):
        self.logger.info(msg)

    def warn(self,msg):
        self.logger.warn(msg)

    def error(self,msg):
        self.logger.error(msg)

    def critical(self,msg):
        self.logger.critical(msg)

def main():
    logFile=input('log_file: ')
    mylog=MyLog()
    mylog.debug("I'm debug")
    mylog.info("I'm info")
    mylog.warn("I'm warn")
    mylog.error("I'm erro")
    mylog.error('I\'m twice')
    mylog.critical("I'm critical")

if __name__ == '__main__':
    main()
    