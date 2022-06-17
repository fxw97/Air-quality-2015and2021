# 整理2021年珠三角数据
import pandas as pd
import glob
pd.set_option('display.max_columns',100)
pd.set_option('display.width',1000)
# 站点信息
df = pd.read_excel('珠三角城市群空气质量站点列表.xlsx')
new_clos = ['date','hour','type']+df['监测点编码'].tolist()
files = glob.glob('2021站点数据/*.csv')
data_PM = pd.DataFrame()
data_O3 = pd.DataFrame()
for file in files:
    data = pd.read_csv(file)
    data = data.loc[:,new_clos]
    datetime = data['date'].apply(str) +' '+ data['hour'].apply(lambda x: str(x)+':00')
    data['datetime'] = pd.to_datetime(datetime)
    data = data.set_index('datetime')
    data.drop(columns=['date','hour'],inplace=True)
    # 按照城市名对列进行重命名
    data.columns = ['type']+\
                   ['GZ'+str(x) for x in range(1,11,1)]+\
                   ['SZ'+str(x) for x in range(1,12,1)]+\
                   ['FS'+str(x) for x in range(1,9,1)]+\
                   ['ZS'+str(x) for x in range(1,5,1)]+\
                   ['HZ'+str(x) for x in range(1,6,1)]+\
                   ['DG'+str(x) for x in range(1,6,1)]+\
                   ['ZH'+str(x) for x in range(1,5,1)]+\
                   ['JM'+str(x) for x in range(1,5,1)]+\
                   ['ZQ'+str(x) for x in range(1,4,1)]
    data_PM_temp = data[data['type']=='PM2.5']
    data_O3_temp = data[data['type']=='O3']
    data_PM = pd.concat([data_PM,data_PM_temp],axis=0)
    data_O3 = pd.concat([data_O3,data_O3_temp],axis=0)
    print(file[-12:-4],' 整理完毕!!!')
    print('****'*5)

data_PM.to_csv('3.2021年珠三角城市站点PM.csv')
data_O3.to_csv('4.2021年珠三角城市站点O3.csv')