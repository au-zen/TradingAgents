"""
增强的数据源管理器
支持多数据源、故障转移、数据融合和缓存
"""

import logging
import pandas as pd
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, timedelta
import hashlib
import json
import os

from .data_source_manager import DataSourceManager
from . import akshare_utils
from . import finnhub_utils
from . import googlenews_utils
from . import yfin_utils
from . import reddit_utils

# 导入新的A股数据源
try:
    from .china_stock_data_sources import (
        china_stock_manager,
        get_china_stock_data,
        get_china_company_info
    )
    CHINA_STOCK_SOURCES_AVAILABLE = True
except ImportError as e:
    logger.warning(f"China stock data sources not available: {e}")
    CHINA_STOCK_SOURCES_AVAILABLE = False

logger = logging.getLogger(__name__)

class EnhancedDataSourceManager(DataSourceManager):
    """增强的数据源管理器，支持多数据源融合和智能故障转移"""
    
    def __init__(self, cache_dir: str = None):
        super().__init__()
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), "data_cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # 数据源优先级配置
        self.data_source_priority = {
            "cn_market": {
                "stock_data": ["china_enhanced", "akshare", "yfin"],  # 新增china_enhanced作为首选
                "company_info": ["china_enhanced", "akshare"],  # 新增china_enhanced
                "news": ["akshare", "googlenews"],
                "financials": ["china_enhanced", "akshare", "finnhub"],  # 新增china_enhanced
                "social_sentiment": ["reddit", "googlenews"]
            },
            "us_market": {
                "stock_data": ["yfin", "finnhub"],
                "company_info": ["finnhub", "yfin"],
                "news": ["finnhub", "googlenews", "reddit"],
                "financials": ["finnhub", "yfin"],
                "social_sentiment": ["reddit", "googlenews"]
            }
        }
    
    def _get_cache_key(self, method: str, **kwargs) -> str:
        """生成缓存键"""
        key_data = f"{method}_{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """获取缓存文件路径"""
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def _is_cache_valid(self, cache_path: str, max_age_hours: int = 24) -> bool:
        """检查缓存是否有效"""
        if not os.path.exists(cache_path):
            return False
        
        file_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        return datetime.now() - file_time < timedelta(hours=max_age_hours)
    
    def _save_to_cache(self, cache_path: str, data: Any):
        """保存数据到缓存"""
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                if isinstance(data, pd.DataFrame):
                    json.dump(data.to_dict('records'), f, ensure_ascii=False, indent=2)
                else:
                    json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")
    
    def _load_from_cache(self, cache_path: str) -> Any:
        """从缓存加载数据"""
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list) and data:
                    # 尝试转换为DataFrame
                    return pd.DataFrame(data)
                return data
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}")
            return None
    
    def get_stock_data_enhanced(self, symbol: str, start_date: str, end_date: str, 
                               use_cache: bool = True, max_cache_age: int = 6) -> Optional[pd.DataFrame]:
        """
        增强的股票数据获取，支持多数据源和缓存
        
        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            use_cache: 是否使用缓存
            max_cache_age: 缓存最大年龄（小时）
        """
        # 检查缓存
        if use_cache:
            cache_key = self._get_cache_key("stock_data", symbol=symbol, 
                                          start_date=start_date, end_date=end_date)
            cache_path = self._get_cache_path(cache_key)
            
            if self._is_cache_valid(cache_path, max_cache_age):
                cached_data = self._load_from_cache(cache_path)
                if cached_data is not None:
                    logger.info(f"Using cached stock data for {symbol}")
                    return cached_data
        
        # 确定市场和数据源优先级
        market = self.get_market_for_symbol(symbol)
        data_sources = self.data_source_priority[market]["stock_data"]
        
        # 尝试多个数据源
        for source in data_sources:
            try:
                logger.info(f"Trying {source} for stock data: {symbol}")

                if source == "akshare" and market == "cn_market":
                    df = akshare_utils.get_stock_zh_a_daily(symbol, start_date, end_date)
                elif source == "china_enhanced" and market == "cn_market" and CHINA_STOCK_SOURCES_AVAILABLE:
                    # 使用新的A股数据源（JQData、Tushare、Alltick）
                    df = get_china_stock_data(symbol, start_date, end_date)
                elif source == "yfin":
                    df = yfin_utils.get_stock_data(symbol, start_date, end_date)
                elif source == "finnhub":
                    df = self.get_stock_data(symbol, start_date, end_date)  # 使用父类方法
                else:
                    continue
                
                if df is not None and not df.empty:
                    # 保存到缓存
                    if use_cache:
                        self._save_to_cache(cache_path, df)
                    
                    logger.info(f"Successfully got stock data from {source}")
                    return df
                    
            except Exception as e:
                logger.warning(f"Failed to get stock data from {source}: {e}")
                continue
        
        logger.error(f"Failed to get stock data for {symbol} from all sources")
        return None
    
    def get_company_info_enhanced(self, symbol: str, use_cache: bool = True) -> Optional[Dict]:
        """
        增强的公司信息获取
        """
        if use_cache:
            cache_key = self._get_cache_key("company_info", symbol=symbol)
            cache_path = self._get_cache_path(cache_key)
            
            if self._is_cache_valid(cache_path, 24):  # 24小时缓存
                cached_data = self._load_from_cache(cache_path)
                if cached_data is not None:
                    return cached_data
        
        market = self.get_market_for_symbol(symbol)
        data_sources = self.data_source_priority[market]["company_info"]
        
        for source in data_sources:
            try:
                logger.info(f"Trying {source} for company info: {symbol}")

                if source == "china_enhanced" and market == "cn_market" and CHINA_STOCK_SOURCES_AVAILABLE:
                    # 使用新的A股数据源获取公司信息
                    info = get_china_company_info(symbol)
                    if info is not None:
                        if use_cache:
                            self._save_to_cache(cache_path, info)
                        return info

                elif source == "akshare" and market == "cn_market":
                    df = akshare_utils.get_stock_zh_a_info(symbol)
                    if df is not None and not df.empty:
                        info = df.iloc[0].to_dict()
                        if use_cache:
                            self._save_to_cache(cache_path, info)
                        return info

                elif source == "finnhub":
                    # 这里可以添加finnhub的公司信息获取
                    pass

            except Exception as e:
                logger.warning(f"Failed to get company info from {source}: {e}")
                continue
        
        return None
    
    def get_news_enhanced(self, symbol: str, limit: int = 10, 
                         use_cache: bool = True, max_cache_age: int = 2) -> Optional[str]:
        """
        增强的新闻获取，融合多个数据源
        """
        if use_cache:
            cache_key = self._get_cache_key("news", symbol=symbol, limit=limit)
            cache_path = self._get_cache_path(cache_key)
            
            if self._is_cache_valid(cache_path, max_cache_age):
                cached_data = self._load_from_cache(cache_path)
                if cached_data is not None:
                    return cached_data
        
        market = self.get_market_for_symbol(symbol)
        data_sources = self.data_source_priority[market]["news"]
        
        all_news = []
        
        for source in data_sources:
            try:
                logger.info(f"Trying {source} for news: {symbol}")
                
                if source == "akshare" and market == "cn_market":
                    news = akshare_utils.get_stock_zh_a_news(symbol, limit=limit//2)
                    if news:
                        all_news.append(f"=== AKShare新闻 ===\n{news}")
                
                elif source == "googlenews":
                    # 获取Google新闻
                    company_name = self._get_company_name(symbol)
                    if company_name:
                        news = googlenews_utils.get_google_news(company_name, limit=limit//2)
                        if news:
                            all_news.append(f"=== Google新闻 ===\n{news}")
                
                elif source == "finnhub":
                    # 这里可以添加finnhub新闻
                    pass
                    
            except Exception as e:
                logger.warning(f"Failed to get news from {source}: {e}")
                continue
        
        if all_news:
            combined_news = "\n\n".join(all_news)
            if use_cache:
                self._save_to_cache(cache_path, combined_news)
            return combined_news
        
        return None
    
    def _get_company_name(self, symbol: str) -> Optional[str]:
        """获取公司名称用于新闻搜索"""
        try:
            if self.get_market_for_symbol(symbol) == "cn_market":
                df = akshare_utils.get_stock_zh_a_info(symbol)
                if df is not None and not df.empty:
                    return df.iloc[0].get("股票简称") or df.iloc[0].get("名称")
            # 对于美股，可以从symbol中提取或使用其他方法
            return symbol.replace(".SH", "").replace(".SZ", "")
        except:
            return symbol
    
    def get_social_sentiment_enhanced(self, symbol: str, use_cache: bool = True) -> Optional[str]:
        """
        增强的社交媒体情绪分析
        """
        if use_cache:
            cache_key = self._get_cache_key("social_sentiment", symbol=symbol)
            cache_path = self._get_cache_path(cache_key)
            
            if self._is_cache_valid(cache_path, 4):  # 4小时缓存
                cached_data = self._load_from_cache(cache_path)
                if cached_data is not None:
                    return cached_data
        
        market = self.get_market_for_symbol(symbol)
        data_sources = self.data_source_priority[market]["social_sentiment"]
        
        sentiment_data = []
        
        for source in data_sources:
            try:
                if source == "reddit":
                    # Reddit情绪分析
                    reddit_data = reddit_utils.get_reddit_stock_info(symbol)
                    if reddit_data:
                        sentiment_data.append(f"=== Reddit情绪 ===\n{reddit_data}")
                
                # 可以添加更多社交媒体数据源
                
            except Exception as e:
                logger.warning(f"Failed to get sentiment from {source}: {e}")
                continue
        
        if sentiment_data:
            combined_sentiment = "\n\n".join(sentiment_data)
            if use_cache:
                self._save_to_cache(cache_path, combined_sentiment)
            return combined_sentiment
        
        return None
    
    def get_data_quality_report(self, symbol: str) -> Dict[str, Any]:
        """
        获取数据质量报告
        """
        market = self.get_market_for_symbol(symbol)
        report = {
            "symbol": symbol,
            "market": market,
            "timestamp": datetime.now().isoformat(),
            "data_sources": {},
            "overall_quality": "unknown"
        }
        
        # 测试各个数据源的可用性
        for data_type, sources in self.data_source_priority[market].items():
            report["data_sources"][data_type] = {}
            
            for source in sources:
                try:
                    if data_type == "stock_data":
                        # 测试股票数据
                        end_date = datetime.now().strftime("%Y-%m-%d")
                        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
                        
                        if source == "akshare" and market == "cn_market":
                            df = akshare_utils.get_stock_zh_a_daily(symbol, start_date, end_date)
                            status = "available" if df is not None and not df.empty else "no_data"
                        else:
                            status = "not_tested"
                    else:
                        status = "not_tested"
                    
                    report["data_sources"][data_type][source] = status
                    
                except Exception as e:
                    report["data_sources"][data_type][source] = f"error: {str(e)}"
        
        # 计算整体质量
        available_count = 0
        total_count = 0
        
        for data_type, sources in report["data_sources"].items():
            for source, status in sources.items():
                total_count += 1
                if status == "available":
                    available_count += 1
        
        if total_count > 0:
            quality_ratio = available_count / total_count
            if quality_ratio >= 0.8:
                report["overall_quality"] = "excellent"
            elif quality_ratio >= 0.6:
                report["overall_quality"] = "good"
            elif quality_ratio >= 0.4:
                report["overall_quality"] = "fair"
            else:
                report["overall_quality"] = "poor"
        
        return report
