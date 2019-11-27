# 挑战任务
# 现在有一些由气象站提供的每日降雨数据，我们需要根据历史降雨数据来预测明天会下雨的概率。

# 数据说明
# 为了完成本次挑战，你需要处理两种类型的数据，第一：训练集数据，第二：测试集数据，最后根据提供的两种数据生成预测结果文件，关于这三种数据文件的说明如下：

# 训练集数据文件
# 本关涉及到的训练集数据train.csv的部分数据如下：

# Date	Location	MinTemp	MaxTemp	Rainfall	Evaporation	Sunshine	WindGustDir	WindGustSpeed	WindDir9am	WindDir3pm	WindSpeed9am	WindSpeed3pm	Humidity9am	Humidity3pm	Pressure9am	Pressure3pm	Cloud9am	Cloud3pm	Temp9am	Temp3pm	RainToday	RISK_MM	RainTomorrow
# 2008/12/1	Albury	13.4	22.9	0.6	NA	NA	W	44	W	WNW	20	24	71	22	1007.7	1007.1	8	NA	16.9	21.8	No	0	No
# 2008/12/2	Albury	7.4	25.1	0	NA	NA	WNW	44	NNW	WSW	4	22	44	25	1010.6	1007.8	NA	NA	17.2	24.3	No	0	No
# 2008/19/26	Albury	12.9	25.7	0	NA	NA	WSW	46	W	WSW	19	26	38	30	1007.6	1008.7	NA	2	21	23.2	No	0	No
# 2008/11/9	Albury	9.2	28	0	NA	NA	NE	24	SE	E	11	9	45	16	10017.6	1012.8	NA	NA	18.1	26.5	No	1	No
# 2008/7/20	Albury	17.5	32.3	1	NA	NA	W	41	ENE	NW	7	20	82	33	1010.8	1006	7	NA	8	29.7	No	0.2	No
# 各个特征描述如下：

# 特征名称	意义	取值范围
# Date	日期	字符串
# Location	气象站的地址	字符串
# MinTemp	最低温度	实数
# MaxTemp	最高温度	实数
# Rainfall	降雨量	实数
# Evaporation	蒸发量	实数
# Sunshine	光照时间	实数
# WindGustDir	最强的风的方向	字符串
# WindGustSpeed	最强的风的速度	实数
# WindDir9am	早上9点的风向	字符串
# WindDir3pm	下午3点的风向	字符串
# WindSpeed9am	早上9点的风速	实数
# WindSpeed3pm	下午3点的风速	实数
# Humidity9am	早上9点的湿度	实数
# Humidity3pm	下午3点的湿度	实数
# Pressure9am	早上9点的大气压	实数
# Pressure3pm	早上3点的大气压	实数
# Cloud9am	早上9点的云指数	实数
# Cloud3pm	早上3点的云指数	实数
# Temp9am	早上9点的温度	实数
# Temp3pm	早上3点的温度	实数
# RainToday	今天是否下雨	No，Yes
# RainTomorrow	明天是否下雨	No，Yes
# 测试集数据文件
# 本关涉及到的测试集数据test.csv与train.csv的格式完全相同，但其RainTomorrow未给出，为预测变量。

# 预测结果文件
# 你需要根据上述训练集文件与测试集文件预测明天会下雨的概率。

# 根据训练集和测试集生成的预测结果数据需要保存在test_prediction.csv文件中，并且需要存放在./output/目录下，编码采用无 BOM 的 UTF-8，每行记录表示根据当天的数据预测明天会下雨的概率。

# 提交文件格式参考如下：

# Date, Location, RainTomorrow

# 2008/11/11, MountGinini, 0.91

# 2008/11/12, MountGinini, 0.04

# 2008/11/13, MountGinini, 0.66

# 2008/11/14, MountGinini, 0.77

# ……

# 注意:大小写敏感。

# 请在完成评测后，点击“查看效果”获取你的成绩，示例如下：


import pandas as pd
import numpy as np
import datetime
import warnings

warnings.filterwarnings('ignore')
#********** Begin *********#
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class LogisticRegression:
    def __init__(self, penalty="l2", gamma=0, fit_intercept=True):
        err_msg = "penalty must be 'l1' or 'l2', but got: {}".format(penalty)
        assert penalty in ["l2", "l1"], err_msg
        self.beta = None
        self.gamma = gamma
        self.penalty = penalty
        self.fit_intercept = fit_intercept

    def fit(self, X, y, lr=0.01, tol=1e-7, max_iter=1e7):
        if self.fit_intercept:
            X = np.c_[np.ones(X.shape[0]), X]

        l_prev = np.inf
        self.beta = np.random.rand(X.shape[1])
        for _ in range(int(max_iter)):
            y_pred = sigmoid(np.dot(X, self.beta))
            loss = self._NLL(X, y, y_pred)
            if l_prev - loss < tol:
                return
            l_prev = loss
            self.beta -= lr * self._NLL_grad(X, y, y_pred)

    def _NLL(self, X, y, y_pred):
        N, M = X.shape
        order = 2 if self.penalty == "l2" else 1
        nll = -np.log(y_pred[y == 1]).sum() - np.log(1 - y_pred[y == 0]).sum()
        penalty = 0.5 * self.gamma * np.linalg.norm(self.beta, ord=order) ** 2
        return (penalty + nll) / N

    def _NLL_grad(self, X, y, y_pred):
        N, M = X.shape
        p = self.penalty
        beta = self.beta
        gamma = self.gamma
        l1norm = lambda x: np.linalg.norm(x, 1)
        d_penalty = gamma * beta if p == "l2" else gamma * l1norm(beta) * np.sign(beta)
        return -(np.dot(y - y_pred, X) + d_penalty) / N

    def predict(self, X):
        if self.fit_intercept:
            X = np.c_[np.ones(X.shape[0]), X]
        return sigmoid(np.dot(X, self.beta))



train = pd.read_csv("./input/train.csv")
test = pd.read_csv("./input/test.csv")

data = pd.concat([train, test], sort=True)

data['Date'] = pd.to_datetime(data['Date'])

'''
第一步 通过数据分析发现 对于同一个地区某一天的天气 使用该地区上一天的天气作为预测结果效果很好
'''

data = data.sort_values(['Location','Date']).reset_index(drop=True)

data['RainTomorrow'] = list(data['RainToday'][1:]) + ['No']

def mapping(now):
    year = str(int(now.strftime('%Y')))
    month = str(int(now.strftime('%m')))
    day = str(int(now.strftime('%d')))
    return year+'/'+month+'/'+day

data['Date'] = data['Date'].apply(mapping)

result = pd.merge(left=test[['Date','Location']], right=data[['Date','Location','RainTomorrow']], how='left', on=['Date','Location'])

result['RainTomorrow'] = result['RainTomorrow'].fillna('No')

def bool_to_int(x):
    if x == 'Yes':
        return 0.9999
    elif x == 'No':
        return 0.0001
    else:
        return 0.5

result['RainTomorrow'] = result['RainTomorrow'].apply(bool_to_int)

def minmax(x):
    max_ = max(x)
    min_ = min(x)
    delta = max_ - min_
    return [a - min_ / delta for a in x]

feature  = [x for x in data.columns if x not in ['Date','Location','WindGustDir','WindDir3pm','Cloud3pm','Cloud9am','WindDir9am','train','RainTomorrow','RainToday']]

data['Pressure3pm'] = data['Pressure3pm'] - 1000
data['Pressure9am'] = data['Pressure9am'] - 1000

for i in feature:
    data[i] = minmax(data[i])

'''
第二步 对于某个地区上一天天气未知的情况 进行建模预测
'''

test_new = data[pd.isna(data['RainTomorrow'])]

train_new = data[~pd.isna(data['RainTomorrow']) & ~pd.isna(data['RainToday'])]
    
model = LogisticRegression()
train_new = train_new.dropna()
model.fit(train_new[feature], train_new['RainTomorrow'].apply(lambda x: 1 if x == 'Yes' else 0))

a = model.predict(test_new[feature])

test_new['result'] = a

test_new['result'] = test_new['result'].fillna(0.5)

result_new = test_new[['Date','Location','result']]

result = pd.merge(left=result, right=result_new, how='left', on=['Date','Location'])

result.loc[~pd.isna(result['result']), 'RainTomorrow'] = (result.loc[~pd.isna(result['result']), 'RainTomorrow'] + result.loc[~pd.isna(result['result']), 'result']) / 2



result[['Date','Location','RainTomorrow']].to_csv('./output/test_prediction.csv', index=False)
#********** End *********#