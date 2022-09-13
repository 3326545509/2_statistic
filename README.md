# 2_statistic
It's used to statistical processed data.

## 运行文件：为下一阶段工作处理数据 && 统计
* 1.creat_csv.py:  
  把目标路径（形如：./4-6/20120409144544/test.sac）里的sac文件统计成csv。  
  <_**输出**_>: csv文件夹，里面33to25.csv,25to20.csv等不同频段文件
* 2.errortime.py:  
  挑一个频道的csv文件，统计其和catlog在发震位置相同时，记录的发震时刻的差值.
  ç: 2.errortime.png
* 3.merge_csv.py:  
  将震源位置相同，发震时刻差8h（记录时间的标准不同导致）的数据csv文件和catlog文件匹配合并
  <_**输出**_>: mergecsv文件夹，里面有3.merge.33to25.csv等文件
* 4.statistic.py  
  <_**输出**_>：./4.statistic/4.statistic33to25.png等。png中红点是全部数据，黑点是3sigma以内的数据，曲线拟合的是黑点，黑点<10黑色，反之蓝线
* 5.healthCheckSta.py  
  <_**输出**_>：5.health/3.health33to25.csv 5.health33to25.png，用以台站的质量检测，调用5.exclude_cold.sh剔除掉csv中质量差的台站并生成新的csv文件
  
  **至此本阶段数据处理工作结束，1235是处理，4是初步的统计，考察该区域“是否有饼吃”,希望振幅随震中距增大而减小，即dist-amp曲线k<0**
