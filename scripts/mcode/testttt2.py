from mootdx.quotes import Quotes
import mootdx.consts as consts   
from mootdx.reader import Reader


# 创建客户端（推荐通过 MarketType 指定市场）
client = Quotes.factory(
    market= consts.MARKET_SH,  # 上海市场
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

reader = Reader.factory(market='std', tdxdir='C:/new_tdx')

# 读取日线数据
daily = reader.daily(symbol='600036')
print(daily)

# 可以获取该api服务器可以使用的市场列表，类别等信息
clientExt = Quotes.factory(market='ext')
mark = clientExt.markets()
print(mark)