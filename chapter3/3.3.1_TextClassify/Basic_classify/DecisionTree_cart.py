#创建原始的cart树即T0
def createTree(dataSet, leafType=regLeaf, errType=regErr, ops=(1,4)): #递归函数 树构建
	 """ 
	:param dataSet: 数据集 
	:param leafType: 对创建叶节点的函数的引用 
	:param errType: 对误差计算函数的引用 
	:param ops: 用于树构建所需其他参数的元组 
	:return: """
#chooseBestSplit 用gini系数去计算最优分割特征
feat, val = chooseBestSplit(dataSet, leafType, errType, ops) 
if feat == None: return val #满足停止条件时返回叶节点值 
retTree = {} 
retTree['spInd'] = feat 
retTree['spVal'] = val 
#按照分割的特征将数据分割，分割后的左右树数据，分别为下个节点的输入数据
leftSet, rightSet = dataSplit(dataSet, feat, val) 
#递归直至树分割结束
retTree['left'] = createTree(lelftSet, leafType, errType, ops)
retTree['right'] = createTree(rightSet, leafType, errType, ops) 

