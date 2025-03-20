from mootdx.quotes import Quotes
import mootdx.consts as consts   
from mootdx.reader import Reader
from mootdx.tools import tdx2csv


# 创建客户端（推荐通过 MarketType 指定市场）
client = Quotes.factory(
    market='std',
    server="119.147.212.81",
    port=7709,
    timeout=5,  # 超时时间优化
    verbose=False  # 关闭冗余日志
)

# 查询贵州茅台（代码需带市场后缀）
quote = client.quotes(symbol="600519")  # 上海股票需加 .sh 后缀
print(quote)
print(f"最新价: {quote['price']}, 成交量(手): {quote['volume']}")
# print(f"涨跌幅: {quote['percent']}%, 换手率: {quote['turnover']}%")  # 扩展输出字段

symbolSH = client.stocks(market=consts.MARKET_SH)
  #symbol[~symbol['decimal_point'].isin([3,4])]    #symbol['decimal_point'].isin([1])    
filtered_symbolALL = symbolSH[symbolSH['code'].str.startswith(('6', '0'))]    
# 重置索引（可选）
filtered_symbolALL = filtered_symbolALL.reset_index(drop=True)
# print(symbol)
# print(filtered_symbol)

# filtered2_symbol = symbol[~symbol['code'].str.startswith(('6', '0'))]  
# filtered2_symbol = filtered2_symbol.reset_index(drop=True)
# filtered2_symbol.to_excel('symbolBlock.xls', index=False) 

filtered2_symbol006 = symbolSH[symbolSH['code'].str.startswith(('6', '00'))]
filtered2_symbol006 = filtered2_symbol006.reset_index(drop=True)
filtered2_symbol006.to_excel('symbolBlock006.xls', index=False) 


#----------------离线数据--------------------------
reader = Reader.factory(market='std', tdxdir='C:/new_tdx')

# 读取日线数据
daily = reader.daily(symbol='600036')
# print(daily)

#读取板块信息
block = reader.block(symbol='block_zs', group=False)
# print(block)

    # 分组格式
# from mootdx.reader import Reader
# reader = Reader.factory(market='std', tdxdir='c:/new_tdx')

# reader.block(symbol='block_zs', group=True)



# 可以获取该api服务器可以使用的市场列表，类别等信息
# clientExt = Quotes.factory(market='ext')
# mark = clientExt.markets()
# print(mark)