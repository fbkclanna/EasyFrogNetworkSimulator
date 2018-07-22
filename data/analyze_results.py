import sys
import pandas as pd
# import seaborn as sns
import os
import glob
import numpy as np
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as patches
from sklearn.cluster import KMeans
from scipy import stats
import seaborn as sns

# from IPython.display import display, HTML


df_list = []
for i in range(100):
    file = 'SensorNode' + str(i) + '.csv'
    if os.path.exists(file):
        df = pd.read_csv(file, index_col=0)
        # time	data_amount	send_data_len	energy	state	tiredness	fsc_state
        del df['data_amount']
        del df['send_data_len']
        del df['energy']
        del df['state']
        # del df['fsc_state']
        df_list.append(df)
        print file, ' is loaded'
        # print df.head
    else:
        break

fig = plt.figure()
'''
ax = fig.add_subplot(211)

#fig = plt.figure()

ax.hold(True)
for i, df in enumerate(df_list):
    #df.rename(index = {'tiredness': 'node' + str(i)})
    name = 'node' + str(i)
    df.plot(x = 'time', y = 'tiredness',  ax = ax , label = name)
'''
ax = fig.add_subplot(111)
ax.hold(True)
for i, df in enumerate(df_list):
    name = 'node' + str(i)
    print df.head
    df.plot(x='time', y='fsc_state', ax=ax, label=name)
    ax.set_yticks([0, 1, 1.1])
    ax.set_ylabel('isActive')

fig.show()
fig.savefig('result_fatigue.png')
input("enter to close")

# fig.savefig('result_heatmap.png')
# sns.plt.savefig('result_heatmap.png')
# sns.plt.close()


'''

for i, row in df.iterrows():
    RMSE = 0
    if (row.x, row.y) not in processed_list:
        processed_list.append((row.x, row.y))
        processed_list_x.append(row.x)
        processed_list_y.append(row.y)
        tmp_df = df[df.x.values  == row.x]
        tmp_df = tmp_df[tmp_df.y.values  == row.y]

        for i, row2 in tmp_df.iterrows():
            #if not math.isnan(row.error):
            RMSE += ((row2.estimation_x - row2.x)  ** 2 + (row2.estimation_y - row2.y) ** 2)
        if tmp_df.empty:
            continue
        print '(', row2.x, ',', row2.y, ')'
        print '(', tmp_df.estimation_x.mean(), ',', tmp_df.estimation_y.mean(), ')'
        print 'error', math.sqrt((row.x - tmp_df.estimation_x.mean())**2 + (row.y- tmp_df.estimation_y.mean()) **2 )
        print 'RMSE,\t', math.sqrt(RMSE / len(tmp_df))
        print 'ave,\t', tmp_df['error'].mean()
        print 'var,\t', tmp_df['error'].var()
        
        analyzed_df = analyzed_df.append({'x': row.x, 'y': row.y, 'estimation_x': tmp_df.estimation_x.mean(), 'estimation_y':tmp_df.estimation_y.mean(), 'error':math.sqrt((row.x - tmp_df.estimation_x.mean())**2 + (row.y- tmp_df.estimation_y.mean()) **2 ) }, ignore_index = True)

analyzed_df.to_csv('alalyzed_result.csv')



df = analyzed_df
#df = pd.read_csv(file, names = ('x', 'y', 'estimation_x', 'estimation_y', 'error'))
df.rename(columns={'x': 'x [m]', 'y': 'y [m]'}, inplace=True)
data_pivot = pd.pivot_table(data = df, values = 'error', columns = 'x [m]', index = 'y [m]', aggfunc = np.mean)
ax = sns.heatmap(data_pivot, annot = False, vmin = 0, vmax = 2, cbar_kws={'label': 'error [m]'})

'''
