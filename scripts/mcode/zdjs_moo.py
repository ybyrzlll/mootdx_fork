from mootdx.quotes import Quotes
import mootdx.consts as consts   
from mootdx.reader import Reader

# 创建客户端（推荐通过 MarketType 指定市场）
client = Quotes.factory(
    market='std',
    server="119.147.212.81",
    port=7709,
    timeout=5,  # 超时时间优化
    verbose=False  # 关闭冗余日志
)

symbolSH = client.stocks(market=consts.MARKET_SH)
filtered_symbolSH = symbolSH[symbolSH['code'].str.startswith(('6'))]  

symbolSZ = client.stocks(market=consts.MARKET_SZ)
filtered_symbolSZ = symbolSZ[symbolSZ['code'].str.startswith(('00'))]  

filtered_symbolSH.to_excel('excels/symbolSH.xls', index=False) 
filtered_symbolSZ.to_excel('excels/symbolSZ.xls', index=False) 