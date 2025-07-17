"""
中国A股数据源补充模块
整合聚宽JQData、Tushare、Alltick等数据源
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
import time
import requests
from functools import wraps

logger = logging.getLogger(__name__)

def retry_on_failure(max_retries=3, delay=1):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"{func.__name__} failed after {max_retries} attempts: {e}")
                        raise
                    logger.warning(f"{func.__name__} attempt {attempt + 1} failed: {e}, retrying...")
                    time.sleep(delay * (attempt + 1))
            return None
        return wrapper
    return decorator

class JQDataSource:
    """聚宽JQData数据源"""
    
    def __init__(self):
        self.username = os.getenv('JQDATA_USERNAME')
        self.password = os.getenv('JQDATA_PASSWORD')
        self.initialized = False
        
    def _initialize(self):
        """初始化JQData连接"""
        if self.initialized:
            return True
            
        try:
            import jqdatasdk as jq
            if self.username and self.password:
                jq.auth(self.username, self.password)
                self.jq = jq
                self.initialized = True
                logger.info("JQData initialized successfully")
                return True
            else:
                logger.warning("JQData credentials not found in environment variables")
                return False
        except ImportError:
            logger.warning("jqdatasdk not installed. Install with: pip install jqdatasdk")
            return False
        except Exception as e:
            logger.error(f"Failed to initialize JQData: {e}")
            return False
    
    @retry_on_failure(max_retries=3)
    def get_stock_data(self, symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """获取股票价格数据"""
        if not self._initialize():
            return None
            
        try:
            # 转换股票代码格式
            jq_symbol = self._convert_symbol(symbol)
            
            # 获取价格数据
            df = self.jq.get_price(
                jq_symbol,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['open', 'close', 'high', 'low', 'volume', 'money']
            )
            
            if df is not None and not df.empty:
                df = df.reset_index()
                df['symbol'] = symbol
                df['source'] = 'jqdata'
                logger.info(f"JQData: Retrieved {len(df)} records for {symbol}")
                return df
            
        except Exception as e:
            logger.error(f"JQData get_stock_data error for {symbol}: {e}")
            
        return None
    
    @retry_on_failure(max_retries=3)
    def get_fundamentals(self, symbol: str) -> Optional[Dict]:
        """获取基本面数据"""
        if not self._initialize():
            return None
            
        try:
            jq_symbol = self._convert_symbol(symbol)
            
            # 获取基本面数据
            q = self.jq.query(
                self.jq.valuation.code,
                self.jq.valuation.pe_ratio,
                self.jq.valuation.pb_ratio,
                self.jq.valuation.ps_ratio,
                self.jq.valuation.pcf_ratio,
                self.jq.valuation.market_cap,
                self.jq.valuation.circulating_market_cap
            ).filter(
                self.jq.valuation.code == jq_symbol
            )
            
            df = self.jq.get_fundamentals(q, date=datetime.now().strftime('%Y-%m-%d'))
            
            if df is not None and not df.empty:
                data = df.iloc[0].to_dict()
                data['source'] = 'jqdata'
                data['symbol'] = symbol
                logger.info(f"JQData: Retrieved fundamentals for {symbol}")
                return data
                
        except Exception as e:
            logger.error(f"JQData get_fundamentals error for {symbol}: {e}")
            
        return None
    
    def _convert_symbol(self, symbol: str) -> str:
        """转换股票代码格式为JQData格式"""
        if '.' in symbol:
            code, exchange = symbol.split('.')
            if exchange.upper() == 'SH':
                return f"{code}.XSHG"
            elif exchange.upper() == 'SZ':
                return f"{code}.XSHE"
        return symbol

class TushareDataSource:
    """Tushare数据源"""
    
    def __init__(self):
        self.token = os.getenv('TUSHARE_TOKEN')
        self.initialized = False
        
    def _initialize(self):
        """初始化Tushare连接"""
        if self.initialized:
            return True
            
        try:
            import tushare as ts
            if self.token:
                ts.set_token(self.token)
                self.ts = ts
                self.pro = ts.pro_api()
                self.initialized = True
                logger.info("Tushare initialized successfully")
                return True
            else:
                logger.warning("Tushare token not found in environment variables")
                return False
        except ImportError:
            logger.warning("tushare not installed. Install with: pip install tushare")
            return False
        except Exception as e:
            logger.error(f"Failed to initialize Tushare: {e}")
            return False
    
    @retry_on_failure(max_retries=3)
    def get_stock_data(self, symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """获取股票价格数据"""
        if not self._initialize():
            return None
            
        try:
            # 转换股票代码格式
            ts_symbol = self._convert_symbol(symbol)
            
            # 获取价格数据
            df = self.pro.daily(
                ts_code=ts_symbol,
                start_date=start_date.replace('-', ''),
                end_date=end_date.replace('-', '')
            )
            
            if df is not None and not df.empty:
                # 重命名列以保持一致性
                df = df.rename(columns={
                    'trade_date': 'date',
                    'vol': 'volume',
                    'amount': 'money'
                })
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date').reset_index(drop=True)
                df['symbol'] = symbol
                df['source'] = 'tushare'
                logger.info(f"Tushare: Retrieved {len(df)} records for {symbol}")
                return df
                
        except Exception as e:
            logger.error(f"Tushare get_stock_data error for {symbol}: {e}")
            
        return None
    
    @retry_on_failure(max_retries=3)
    def get_company_info(self, symbol: str) -> Optional[Dict]:
        """获取公司基本信息"""
        if not self._initialize():
            return None
            
        try:
            ts_symbol = self._convert_symbol(symbol)
            
            # 获取股票基本信息
            df = self.pro.stock_basic(ts_code=ts_symbol)
            
            if df is not None and not df.empty:
                data = df.iloc[0].to_dict()
                data['source'] = 'tushare'
                data['symbol'] = symbol
                logger.info(f"Tushare: Retrieved company info for {symbol}")
                return data
                
        except Exception as e:
            logger.error(f"Tushare get_company_info error for {symbol}: {e}")
            
        return None
    
    def _convert_symbol(self, symbol: str) -> str:
        """转换股票代码格式为Tushare格式"""
        if '.' in symbol:
            code, exchange = symbol.split('.')
            return f"{code}.{exchange.upper()}"
        return symbol

class AlltickDataSource:
    """Alltick数据源"""
    
    def __init__(self):
        self.token = os.getenv('ALLTICK_TOKEN')
        self.base_url = "https://quote.tradeswitcher.com/quote-stock-b-api"
        
    @retry_on_failure(max_retries=3)
    def get_stock_data(self, symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """获取股票价格数据"""
        if not self.token:
            logger.warning("Alltick token not found in environment variables")
            return None
            
        try:
            # 转换股票代码格式
            alltick_symbol = self._convert_symbol(symbol)
            
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            params = {
                'symbol': alltick_symbol,
                'start_time': start_date,
                'end_time': end_date,
                'period': '1d'
            }
            
            response = requests.get(
                f"{self.base_url}/kline",
                headers=headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and data.get('data'):
                    df = pd.DataFrame(data['data'])
                    if not df.empty:
                        # 重命名列以保持一致性
                        df = df.rename(columns={
                            'time': 'date',
                            'vol': 'volume'
                        })
                        df['date'] = pd.to_datetime(df['date'], unit='s')
                        df['symbol'] = symbol
                        df['source'] = 'alltick'
                        logger.info(f"Alltick: Retrieved {len(df)} records for {symbol}")
                        return df
                        
        except Exception as e:
            logger.error(f"Alltick get_stock_data error for {symbol}: {e}")
            
        return None
    
    def _convert_symbol(self, symbol: str) -> str:
        """转换股票代码格式为Alltick格式"""
        if '.' in symbol:
            code, exchange = symbol.split('.')
            if exchange.upper() == 'SH':
                return f"SH.{code}"
            elif exchange.upper() == 'SZ':
                return f"SZ.{code}"
        return symbol

class ChinaStockDataManager:
    """中国A股数据管理器"""
    
    def __init__(self):
        self.sources = {
            'jqdata': JQDataSource(),
            'tushare': TushareDataSource(),
            'alltick': AlltickDataSource()
        }
        
    def get_stock_data_enhanced(self, symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """
        获取增强的股票数据，尝试多个数据源
        
        Args:
            symbol: 股票代码，如 '603127.SH'
            start_date: 开始日期，如 '2024-01-01'
            end_date: 结束日期，如 '2024-01-31'
            
        Returns:
            合并的股票数据DataFrame
        """
        all_data = []
        
        # 按优先级尝试各个数据源
        source_priority = ['jqdata', 'tushare', 'alltick']
        
        for source_name in source_priority:
            source = self.sources[source_name]
            try:
                data = source.get_stock_data(symbol, start_date, end_date)
                if data is not None and not data.empty:
                    all_data.append(data)
                    logger.info(f"Successfully retrieved data from {source_name} for {symbol}")
                    break  # 获取到数据就停止尝试其他源
            except Exception as e:
                logger.warning(f"Failed to get data from {source_name} for {symbol}: {e}")
                continue
        
        if all_data:
            # 返回第一个成功的数据源的数据
            return all_data[0]
        else:
            logger.error(f"Failed to retrieve data from all sources for {symbol}")
            return None
    
    def get_company_info_enhanced(self, symbol: str) -> Optional[Dict]:
        """
        获取增强的公司信息
        
        Args:
            symbol: 股票代码，如 '603127.SH'
            
        Returns:
            公司信息字典
        """
        # 尝试从Tushare获取公司信息
        tushare_source = self.sources['tushare']
        try:
            info = tushare_source.get_company_info(symbol)
            if info:
                return info
        except Exception as e:
            logger.warning(f"Failed to get company info from Tushare for {symbol}: {e}")
        
        # 尝试从JQData获取基本面数据
        jqdata_source = self.sources['jqdata']
        try:
            fundamentals = jqdata_source.get_fundamentals(symbol)
            if fundamentals:
                return fundamentals
        except Exception as e:
            logger.warning(f"Failed to get fundamentals from JQData for {symbol}: {e}")
        
        return None
    
    def get_data_source_status(self, symbol: str) -> Dict[str, str]:
        """
        检查各数据源的可用性状态
        
        Args:
            symbol: 股票代码
            
        Returns:
            各数据源状态字典
        """
        status = {}
        
        for source_name, source in self.sources.items():
            try:
                if source_name == 'jqdata':
                    available = source._initialize()
                elif source_name == 'tushare':
                    available = source._initialize()
                elif source_name == 'alltick':
                    available = bool(source.token)
                else:
                    available = False
                
                status[source_name] = "available" if available else "unavailable"
                
            except Exception as e:
                status[source_name] = f"error: {str(e)}"
        
        return status

# 全局实例
china_stock_manager = ChinaStockDataManager()

def get_china_stock_data(symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """
    获取中国A股数据的主要接口
    
    Args:
        symbol: 股票代码，如 '603127.SH'
        start_date: 开始日期，如 '2024-01-01'
        end_date: 结束日期，如 '2024-01-31'
        
    Returns:
        股票数据DataFrame
    """
    return china_stock_manager.get_stock_data_enhanced(symbol, start_date, end_date)

def get_china_company_info(symbol: str) -> Optional[Dict]:
    """
    获取中国A股公司信息的主要接口
    
    Args:
        symbol: 股票代码，如 '603127.SH'
        
    Returns:
        公司信息字典
    """
    return china_stock_manager.get_company_info_enhanced(symbol)
