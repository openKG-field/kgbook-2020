#encoding=utf-8
# -*- coding:utf-8 -*-

# python ʵ��N��������������(�ѿ������㷨)
class Cartesian():
    # ��ʼ��
    def __init__(self, datagroup):
        self.datagroup = datagroup
        # ��ά����Ӻ���ǰ�±�ֵ
        self.counterIndex = len(datagroup)-1
        # ÿ�����������ֵ���±�ֵ����(��ʼ��Ϊ0)
        self.counter = [0 for i in range(0, len(self.datagroup))]

    # �������鳤��
    def countlength(self):
        i = 0
        length = 1
        while(i < len(self.datagroup)):
            length *= len(self.datagroup[i])
            i += 1
        return length

    # �ݹ鴦������±�
    def handle(self):
        # ��λ����±����鿪ʼ�����һλ����
        self.counter[self.counterIndex]+=1
        # �ж϶�λ�������һλ�Ƿ񳬹����ȣ��������ȣ���һ�����һλ�ѱ�������
        if self.counter[self.counterIndex] >= len(self.datagroup[self.counterIndex]):   

            # ����ĩλ�±�
            self.counter[self.counterIndex] = 0
            # ���counter��ǰһλ
            self.counterIndex -= 1
            # �����λ���ڵ���0���ݹ����
            if self.counterIndex >= 0:
                self.handle()
            # ���ñ��
            self.counterIndex = len(self.datagroup)-1

    # ����������
    def assemble(self):
        resultList = []
        length = self.countlength()
        i = 0
        while(i < length):
            attrlist = []
            j = 0
            while(j<len(self.datagroup)):
                attrlist.append(self.datagroup[j][self.counter[j]])
                j += 1
            #print attrlist
            resultList.append(attrlist)
            self.handle()
            i += 1
        return resultList