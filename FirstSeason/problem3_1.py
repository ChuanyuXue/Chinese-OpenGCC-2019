# 挑战任务
# 现在有一些由学生的基础信息和两门考试成绩所组成的数据，需要你根据这些数据来预测学生的数学成绩。

# 数据说明
# 为了完成本次挑战，你需要处理两种类型的数据，第一：训练集数据，第二：测试集数据，最后根据提供的两种数据生成预测结果文件，关于这三种数据文件的说明如下：

# 训练集数据文件
# 本关涉及到的训练集数据train.csv的部分数据如下：

# id	gender	race/ethnicity	parental level of education	lunch	test preparation course	reading score	writing score	math score
# 838	female	group B	bachelor's degree	standard	none	72	74	72
# 98	female	group C	some collegd	standard	completed	90	88	69
# 258	female	group B	master's degree	standard	none	95	93	90
# 189	male	group A	associate's degree	free/reduced	none	57	44	47
# 370	male	group C	some college	standard	none	78	75	76
# 各个特征描述如下：

# 特征名称	意义	取值范围
# id	学生ID	实数
# gender	性别	male，female
# race/ethnicity	种族	group A，group B，group C，group D，group E
# parental level of education	父母的教育水平	some college，associate's degree，high school，some high school，bachelor's degree，master's degree
# lunch	午餐	standard，free/reduced
# test preparation course	预备课程测试	none，completed
# reading score	阅读分数	实数
# writing score	写作分数	实数
# math score	数学分数(标签)	实数
# 测试集数据文件
# 本关涉及到的测试集数据test.csv与train.csv的格式完全相同，但其math score未给出，为预测变量。

# 预测结果文件
# 你需要根据上述训练集文件与测试集文件预测学生的数学分数。

# 根据训练集和测试集生成的预测结果数据需要保存在test_prediction.csv文件中，并且需要存放在./output/目录下，编码采用无 BOM 的 UTF-8，每行记录表示对某个学生的数学分出的预测。

# 提交文件格式参考如下：

# id, math score

# 311, 15.77

# 675, 92.689

# 797, 29.12

# 64, 37.777

# ……

# 注意:大小写敏感。

# 评估指标
# 本关的预测结果评估指标为:R² score，该值越接近于1表示预测越精准。R² score的计算公式如下：


# 其中pp为某个样本的预测结果，yy为某个样本的真实标签，y_{mean}y 
# mean
# ​	
#  表示所有测试样本标签值的均值。

# 本关会根据你的R² score的值来计算你的总得分，总得分(score)的计算公式如下：
 

# 编程要求
# 请补全右侧编辑器中的代码，实现对学生数学成绩的预测，并将预测结果生成在./output/目录下，命名为test_prediction.csv。

# 参考思路：

# 读取./input/train.csv和 ./input/test.csv文件；
# 数据探索；
# 数据预处理；
# 特征工程；
# 构建模型；
# 调参；
# 生成预测结果文件；
# 提交评测；
# 持续优化以提高 R² score 指标。
# 你可以通过如下链接下载本关涉及到的数据文件：

# https://forge.educoder.net/attachments/download/377881/input.zip

# 注意：本环境不提供机器学习框架，需要自己实现相关算法。

# 通关之后，你可以通过弹出的页面查看得分，该成绩即为你本关卡的成绩：


import pandas as pd
import numpy as np

#********** Begin *********#
class RidgeRegression:
    def __init__(self, alpha=1, fit_intercept=True):
        """
        A ridge regression model fit via the normal equation.
        Parameters
        ----------
        alpha : float (default: 1)
            L2 regularization coefficient. Higher values correspond to larger
            penalty on the l2 norm of the model coefficients
        fit_intercept : bool (default: True)
            Whether to fit an additional intercept term in addition to the
            model coefficients
        """
        self.beta = None
        self.alpha = alpha
        self.fit_intercept = fit_intercept

    def fit(self, X, y):
        # convert X to a design matrix if we're fitting an intercept
        if self.fit_intercept:
            X = np.c_[np.ones(X.shape[0]), X]

        A = self.alpha * np.eye(X.shape[1])
        pseudo_inverse = np.dot(np.linalg.inv(X.T @ X + A), X.T)
        self.beta = pseudo_inverse @ y

    def predict(self, X):
        # convert X to a design matrix if we're fitting an intercept
        if self.fit_intercept:
            X = np.c_[np.ones(X.shape[0]), X]
        return np.dot(X, self.beta)

train = pd.read_csv("./input/train.csv")

test = pd.read_csv("./input/test.csv")

data = pd.concat([train, test],sort=True).reset_index(drop=True)

data.columns = [x.replace(' ','_').replace('/','_') for x in data.columns]

data['average_score'] = (data['writing_score'] + data['reading_score']) / 2

data['std_score'] = ((data['writing_score'] - data['average_score'])**2 + (data['reading_score'] - data['average_score'])**2)/2

data['dev_score'] = abs(data['writing_score'] - data['reading_score'])

def decrete(feature):
    features = set(feature)
    mapping = dict(zip(features, range(len(features))))
    feature = feature.apply(lambda x: mapping[x])
    return feature

decrete_features = ['gender','lunch','parental_level_of_education','race_ethnicity','test_preparation_course']

for col in decrete_features:
    data.loc[:, col] = decrete(data[col])

def onehot(feature):
    return np.eye(len(set(np.array(feature))))[np.array(feature)]

for i in decrete_features:
    temp = pd.DataFrame(onehot(data[i]))
    temp.columns = [i + '_' + str(x) for x in temp.columns]
    data = pd.concat([data, temp], axis=1)

train = data[~np.isnan(data['math_score'])].reset_index(drop=True)
test = data[np.isnan(data['math_score'])].reset_index(drop=True)

features = [x for x in train.columns if x not in decrete_features + ['math_score', 'id']]

model = RidgeRegression()

model.fit(np.array(train[features]), np.array(train['math_score']))

test.loc[:, 'math_score'] = model.predict(np.array(test[features]))
result = test[['id','math_score']]
result.columns = ['id','math score']
result.to_csv('./output/test_prediction.csv', index=False)

#********** End *********#