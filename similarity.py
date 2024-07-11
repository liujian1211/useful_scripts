import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_excel('D:/AkyPower/20240628_0630.xlsx')
df_target = pd.read_excel('D:/AkyPower/20240701.xlsx')

# df = pd.DataFrame({
#     'AT':['AT'],
#     'GHI':['GHI'],
#     'pac':['pac']
# })
scaler = StandardScaler()
def preprocess_data(df):
    #DataFrame中的日期时间列被转换为DatetimeIndex才能使用resample方

    # 将日期时间转换为索引，并按天分组
    # df.set_index('time', inplace=True)
    # df = df.resample('H').mean()  # 假设我们只需要日均值，这里可以根据需要调整
    df['hour'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.hour

    # 划分5min时段
    time_clusters = KMeans(n_clusters=50, random_state=0).fit(df['hour'].values.reshape(-1, 1))
    df['time_cluster'] = time_clusters.labels_

    # 标准化特征
    # scaler = StandardScaler()
    df[['AT', 'GHI']] = scaler.fit_transform(df[['AT', 'GHI']])

    return df

def cal_similarity(df,target_day):
    #欧式距离
    euclidean = euclidean_distances(df[['AT','GHI']],target_day)

    #余弦距离
    cosine = cosine_similarity(df[['AT','GHI']],target_day)

    # 赋予权值并整合
    alpha = 0.5  # 权值，可根据需要调整
    similarity = alpha * (1 - (euclidean / np.max(euclidean))) + (1 - alpha) * (cosine / np.max(cosine))

    return similarity

def predict_tomorrow(df,target_day):
    similarity_scores = cal_similarity(df,target_day)
    most_similar_5min_index = np.argmax(similarity_scores)

    return most_similar_5min_index

def get_result(df,index):
    most_similar_5min = df.iloc[index]
    # 预测的AT和GHI
    predcted_AT = most_similar_5min['AT']
    predcted_GHI = most_similar_5min['GHI']

    return predcted_AT, predcted_GHI

# df = preprocess_data(df)
flag = False
#遍历要预测的50条数据（即5min数据）
for i in range(50):
    # df_target[['AT', 'GHI']] = scaler.fit_transform(df_target[['AT', 'GHI']])
    target_5min = df_target.iloc[4480 + i][['AT', 'GHI']].values.reshape(1, -1)  # reshape为(1,2)，且使用和df一样的标准化

    # df[['AT', 'GHI']] = scaler.fit_transform(df[['AT', 'GHI']])

    index = predict_tomorrow(df,target_5min)

    # 反归一化，只执行一次
    # if flag==False:
    #     df[['AT', 'GHI']] = scaler.inverse_transform(df[['AT', 'GHI']])
    #     flag=True

    predicted_AT,predicted_GHI = get_result(df,index)

    print(f'预测的AT和GHI为{predicted_AT}、{predicted_GHI}')