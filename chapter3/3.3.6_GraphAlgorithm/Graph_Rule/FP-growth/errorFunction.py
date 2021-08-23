#encoding=utf-8
'''
Created on 2017年11月8日

@author: zhaoh
'''
def errorType(value):
    if value == 1:
        return 'UN_define'
    elif value == 2:
        return 'KeyError'
    elif value == 3:
        return 'IndexError'
    elif value == 4:
        return 'StackError'
    elif value == 5:
        return 'FormulaError'
    elif value == 6:
        return 'UnicodeError'
    elif value ==7:
        return 'FormatError'
    return 'No Error'
def main():
    return 0
if __name__ == '__main__':
    pass