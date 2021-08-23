lgbm_model.py

light GBM 的 效果展示代码，数据为本书的标准数据

需要注意的时，调用时，应该保证lgm_model_path 为真实有效路径。
model相关的下载链接可以直接访问微软官方网站



params = {
    "task": "train",        #任务目标
    "boosting": "gbdt",       #boosting方式
    "objective": "binary",  #目标  二分类
    "tree_learner": "serial",   #树的组合方式
    "metric": ['auc','binary_logloss'], #评价方法
    "training_metric": True,
    "train_data": './../../../data/train_data.txt',  #训练文档路径
    "test_data":  './../../../data/test_data.txt',  #验证文档路径
    "header": "true",   #文档中是否存在属性头
    "label_column": "name:target",   #标签列
    #"weight_column": "name:weight", #权重列，可以调整训练数据对于结果的影响
    "ignore_column" : "name:applicantFirst", #无视列
    "categorical_feature": '',  #类别列 请特别声明当前类的属性
    "num_trees": 100,  #  弱分类器数量
    "learning_rate": 0.225, #学习率
    "num_leaves": 64,   #叶节点数量
    "feature_fraction": 0.8, #随机丢弃比例
    "min_data_in_leaf": 100, # 分叶最小数据量
    "num_threads": 12, #并发数量 【注意 boost算法只支持特征级别的并发，不支持弱分类器级别的并发】
    "convert_model_language": "cpp",  #转存cpp文件，
    "output_model": "model.md",
    "output_result":"gbm_pre.txt"
    }


结果：
