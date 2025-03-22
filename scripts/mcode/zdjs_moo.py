from mootdx.quotes import Quotes
import mootdx.consts as consts   
from mootdx.reader import Reader
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FixedLocator  # 正确导入 FixedLocator
from datetime import datetime, timedelta

# 间隔天数 until 当前  
recentDays = 20

# 创建客户端（推荐通过 MarketType 指定市场）
client = Quotes.factory(
    market='std',
    server="119.147.212.81",
    port=7709,
    timeout=5,  # 超时时间优化
    verbose=False  # 关闭冗余日志
)

# symbolSH = client.stocks(market=consts.MARKET_SH)
# filtered_symbolSH = symbolSH[symbolSH['code'].str.startswith(('6'))]  

# symbolSZ = client.stocks(market=consts.MARKET_SZ)
# filtered_symbolSZ = symbolSZ[symbolSZ['code'].str.startswith(('00'))]  

# filtered_symbolSH.to_excel('excels/symbolSH.xls', index=False) 
# filtered_symbolSZ.to_excel('excels/symbolSZ.xls', index=False) 

# bars 获取k线数据
# frequency -> K线种类 0 => 5分钟K线 => 5m 1 => 15分钟K线 => 15m 2 => 30分钟K线 => 30m 3 => 小时K线 => 1h 4 => 日K线 (小数点x100) => days 5 => 周K线 => week 6 => 月K线 => mon 7 => 1分钟K线(好像一样) => 1m 8 => 1分钟K线(好像一样) => 1m 9 => 日K线 => day 10 => 季K线 => 3mon 11 => 年K线 => year
stock_test = client.bars(symbol='600036', frequency=9, offset=recentDays)

#  index查询指数K线行情》涨跌家数
# * 参数说明: **
# frequency: K线种类
# market: 市场代码. 0 - 深圳, 1 - 上海 (可以使用常量 MARKET_SZ, MARKET_SH 代替)
# start: 开始位置
# offset: 用户要请求的 K 线数目，最大值为 800
zdjs_data = client.index(frequency=9, market= consts.MARKET_SH, symbol='880005', start=0, offset=recentDays)


# print(stock_test)
# print(zdjs_data)

# stock_test.to_excel('excels/stock_test.xls', index=False) 
# zdjs_data.to_excel('excels/zdjs_data.xls', index=False) 

#-----------------转换数据-----------------------------
# 解决中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示异常

data_list = []
for row in  zdjs_data.itertuples():
    # try:
        # stock_test[1]
            
            
            data_list.append({
                'trade_date': pd.to_datetime(row.datetime),
                'up_count': row.up_count,
                'down_count': row.down_count
            })
    # except Exception as e:
        # print(f"Error fetching {zdjs_data[i]}: {str(e)}")

#-----------------绘制---------------
# 创建DataFrame[1,4](@ref)
trend_data = pd.DataFrame(data_list)
trend_data.sort_values('trade_date', inplace=True)
 
plt.figure(figsize=(14,7))

# 确保数据按日期排序
trend_data = trend_data.sort_values('trade_date')

# 生成索引作为X轴数值（0,1,2,...）
x = range(len(trend_data))

# 提取格式化后的日期标签（如 '02-07', '02-10'）
date_labels = trend_data['trade_date'].dt.strftime('%m-%d').tolist()

# 在现有trend_data创建后添加均线计算
trend_data['up_5ma'] = trend_data['up_count'].rolling(window=5).mean()

# 绘制数据（X轴使用索引）
plt.plot(x, trend_data['up_count'], 
        label='上涨家数', color='#d62728', linewidth=2)
plt.plot(x, trend_data['down_count'],
        label='下跌家数', color='#2ca02c', linestyle='--')
plt.plot(x, trend_data['up_5ma'], 
        label='5日上涨均线', color='#1f77b4', linestyle='-.', linewidth=2.5)  # 新增

# 设置X轴刻度和标签
plt.xticks(ticks=x, labels=date_labels, rotation=45, ha='right')


now = datetime.now()
# 格式化为 "YYYYMMDD" 字符串
start_date = (now - timedelta(recentDays)).strftime("%Y%m%d")
end_date = now.strftime("%Y%m%d")

plt.title(f'A股市场涨跌家数趋势（{start_date}至{end_date}）', fontsize=14)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

