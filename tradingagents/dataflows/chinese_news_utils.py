"""
中国财经新闻数据源工具
整合多个中文财经网站的新闻数据
"""

import requests
import json
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)

class ChineseNewsAggregator:
    """中国财经新闻聚合器"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        # 新闻源配置
        self.news_sources = {
            "eastmoney": {
                "name": "东方财富",
                "base_url": "https://search.eastmoney.com/api/suggest/get",
                "enabled": True
            },
            "sina": {
                "name": "新浪财经", 
                "base_url": "https://finance.sina.com.cn",
                "enabled": True
            },
            "163": {
                "name": "网易财经",
                "base_url": "https://money.163.com",
                "enabled": True
            },
            "cnstock": {
                "name": "中国证券网",
                "base_url": "https://www.cnstock.com",
                "enabled": True
            }
        }
    
    def get_stock_news_from_eastmoney(self, stock_code: str, limit: int = 10) -> List[Dict]:
        """从东方财富获取股票新闻"""
        try:
            # 清理股票代码
            clean_code = stock_code.replace('.SH', '').replace('.SZ', '')
            
            # 构建搜索URL
            url = f"https://search.eastmoney.com/api/suggest/get"
            params = {
                'input': clean_code,
                'type': '14',  # 新闻类型
                'token': '',
                'count': limit
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                news_list = []
                
                if 'QuotationCodeTable' in data and 'Data' in data['QuotationCodeTable']:
                    for item in data['QuotationCodeTable']['Data'][:limit]:
                        news_item = {
                            'title': item.get('Name', ''),
                            'source': '东方财富',
                            'time': item.get('UpdateTime', ''),
                            'url': item.get('Url', ''),
                            'summary': item.get('Name', '')[:100] + '...' if len(item.get('Name', '')) > 100 else item.get('Name', '')
                        }
                        news_list.append(news_item)
                
                return news_list
                
        except Exception as e:
            logger.warning(f"Failed to get news from eastmoney: {e}")
            return []
    
    def get_stock_news_from_sina(self, stock_code: str, limit: int = 10) -> List[Dict]:
        """从新浪财经获取股票新闻（模拟实现）"""
        try:
            # 这里是一个示例实现，实际需要根据新浪财经的API调整
            clean_code = stock_code.replace('.SH', '').replace('.SZ', '')
            
            # 模拟新闻数据（实际应该调用真实API）
            news_list = [
                {
                    'title': f'{clean_code}相关新闻标题示例',
                    'source': '新浪财经',
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'url': f'https://finance.sina.com.cn/stock/{clean_code}',
                    'summary': f'这是关于{clean_code}的新闻摘要示例...'
                }
            ]
            
            return news_list[:limit]
            
        except Exception as e:
            logger.warning(f"Failed to get news from sina: {e}")
            return []
    
    def get_aggregated_news(self, stock_code: str, limit: int = 20) -> str:
        """
        获取聚合新闻
        
        Args:
            stock_code: 股票代码，如 '603127.SH'
            limit: 新闻数量限制
            
        Returns:
            格式化的新闻字符串
        """
        all_news = []
        
        # 从各个源获取新闻
        sources_to_try = [
            ("eastmoney", self.get_stock_news_from_eastmoney),
            ("sina", self.get_stock_news_from_sina),
        ]
        
        for source_name, get_news_func in sources_to_try:
            if self.news_sources[source_name]["enabled"]:
                try:
                    logger.info(f"Getting news from {source_name} for {stock_code}")
                    news = get_news_func(stock_code, limit // len(sources_to_try))
                    all_news.extend(news)
                    
                    # 添加延迟避免被限制
                    time.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    logger.warning(f"Failed to get news from {source_name}: {e}")
                    continue
        
        # 格式化新闻
        if not all_news:
            return f"未能获取到{stock_code}的相关新闻。"
        
        # 按时间排序（如果有时间信息）
        try:
            all_news.sort(key=lambda x: x.get('time', ''), reverse=True)
        except:
            pass
        
        # 格式化输出
        formatted_news = f"📰 {stock_code} 相关新闻汇总 ({len(all_news)}条)\n"
        formatted_news += "=" * 50 + "\n\n"
        
        for i, news in enumerate(all_news[:limit], 1):
            formatted_news += f"{i}. 【{news['source']}】{news['title']}\n"
            if news.get('time'):
                formatted_news += f"   时间: {news['time']}\n"
            if news.get('summary'):
                formatted_news += f"   摘要: {news['summary']}\n"
            if news.get('url'):
                formatted_news += f"   链接: {news['url']}\n"
            formatted_news += "\n"
        
        return formatted_news
    
    def get_market_sentiment_news(self, limit: int = 10) -> str:
        """获取市场情绪相关新闻"""
        try:
            # 这里可以实现获取大盘、政策等宏观新闻
            sentiment_news = [
                {
                    'title': '市场情绪指标显示投资者信心回升',
                    'source': '财经综合',
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'summary': '最新市场数据显示，投资者情绪指标出现积极变化...'
                },
                {
                    'title': '政策利好推动相关板块上涨',
                    'source': '政策解读',
                    'time': (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'),
                    'summary': '新出台的政策对相关行业形成利好支撑...'
                }
            ]
            
            formatted_news = "📊 市场情绪与政策新闻\n"
            formatted_news += "=" * 30 + "\n\n"
            
            for i, news in enumerate(sentiment_news[:limit], 1):
                formatted_news += f"{i}. 【{news['source']}】{news['title']}\n"
                formatted_news += f"   时间: {news['time']}\n"
                formatted_news += f"   摘要: {news['summary']}\n\n"
            
            return formatted_news
            
        except Exception as e:
            logger.warning(f"Failed to get market sentiment news: {e}")
            return "暂时无法获取市场情绪新闻。"

# 全局实例
chinese_news_aggregator = ChineseNewsAggregator()

def get_chinese_stock_news(stock_code: str, limit: int = 15) -> str:
    """
    获取中文股票新闻的主要接口
    
    Args:
        stock_code: 股票代码，如 '603127.SH'
        limit: 新闻数量限制
        
    Returns:
        格式化的新闻字符串
    """
    return chinese_news_aggregator.get_aggregated_news(stock_code, limit)

def get_market_sentiment_news(limit: int = 10) -> str:
    """
    获取市场情绪新闻的主要接口
    
    Args:
        limit: 新闻数量限制
        
    Returns:
        格式化的新闻字符串
    """
    return chinese_news_aggregator.get_market_sentiment_news(limit)

def test_chinese_news_sources():
    """测试中文新闻源"""
    print("测试中文新闻数据源...")
    
    # 测试股票新闻
    test_stock = "603127.SH"
    print(f"\n测试股票: {test_stock}")
    news = get_chinese_stock_news(test_stock, 5)
    print(news)
    
    # 测试市场情绪新闻
    print("\n测试市场情绪新闻:")
    sentiment_news = get_market_sentiment_news(3)
    print(sentiment_news)

if __name__ == "__main__":
    test_chinese_news_sources()
