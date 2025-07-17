"""
TradingAgents 模型提供商推荐配置
根据不同使用场景提供最佳模型配置建议
"""

from typing import Dict, List, Any
import os

class ModelRecommendations:
    """模型推荐配置管理器"""
    
    def __init__(self):
        self.recommendations = self._load_recommendations()
    
    def _load_recommendations(self) -> Dict[str, Dict[str, Any]]:
        """加载推荐配置"""
        return {
            # 🚀 高速免费配置
            "high_speed_free": {
                "name": "🚀 高速免费 (Groq)",
                "provider": "groq",
                "deep_think_llm": "llama3-groq-70b-8192-tool-use-preview",
                "quick_think_llm": "llama3-groq-8b-8192-tool-use-preview",
                "description": "超高速响应，完全免费，支持工具调用",
                "pros": [
                    "响应速度极快 (< 1秒)",
                    "完全免费使用",
                    "支持工具调用",
                    "高并发处理能力"
                ],
                "cons": [
                    "模型选择相对有限",
                    "依赖网络连接"
                ],
                "use_cases": [
                    "快速原型开发",
                    "高频交易分析",
                    "实时市场监控",
                    "教学演示"
                ],
                "setup_difficulty": "简单",
                "cost": "免费",
                "api_key_required": True
            },
            
            # 💎 平衡推荐配置
            "balanced_recommended": {
                "name": "💎 平衡推荐 (OpenRouter)",
                "provider": "openrouter",
                "deep_think_llm": "deepseek/deepseek-r1-distill-qwen-14b:free",
                "quick_think_llm": "qwen/qwen3-14b:free",
                "description": "免费额度大，模型质量高，支持工具调用",
                "pros": [
                    "免费额度充足",
                    "模型质量优秀",
                    "支持多种模型",
                    "工具调用稳定"
                ],
                "cons": [
                    "需要注册账号",
                    "有使用限制"
                ],
                "use_cases": [
                    "日常股票分析",
                    "投资研究",
                    "风险评估",
                    "个人投资决策"
                ],
                "setup_difficulty": "简单",
                "cost": "免费 (有限额)",
                "api_key_required": True
            },
            
            # 🧠 智能优选配置
            "intelligent_premium": {
                "name": "🧠 智能优选 (OpenRouter Pro)",
                "provider": "openrouter",
                "deep_think_llm": "qwen/qwen2.5-72b-instruct",
                "quick_think_llm": "qwen/qwen2.5-14b-instruct",
                "description": "顶级模型性能，适合专业分析",
                "pros": [
                    "顶级模型性能",
                    "复杂推理能力强",
                    "多语言支持优秀",
                    "分析深度高"
                ],
                "cons": [
                    "需要付费",
                    "成本相对较高"
                ],
                "use_cases": [
                    "专业投资分析",
                    "机构级研究",
                    "复杂策略开发",
                    "深度市场分析"
                ],
                "setup_difficulty": "简单",
                "cost": "付费 ($0.5-2/M tokens)",
                "api_key_required": True
            },
            
            # 🏠 本地部署配置
            "local_deployment": {
                "name": "🏠 本地部署 (Ollama)",
                "provider": "ollama",
                "deep_think_llm": "qwen3:14b",
                "quick_think_llm": "qwen3:8b",
                "description": "完全本地运行，数据隐私，无网络依赖",
                "pros": [
                    "完全免费",
                    "数据隐私保护",
                    "无网络依赖",
                    "可自定义模型"
                ],
                "cons": [
                    "需要本地GPU",
                    "安装配置复杂",
                    "模型下载耗时"
                ],
                "use_cases": [
                    "敏感数据分析",
                    "离线环境使用",
                    "自定义模型训练",
                    "企业内部部署"
                ],
                "setup_difficulty": "复杂",
                "cost": "免费 (需硬件)",
                "api_key_required": False,
                "hardware_requirements": {
                    "min_ram": "16GB",
                    "recommended_ram": "32GB",
                    "gpu": "8GB+ VRAM (推荐)",
                    "storage": "50GB+"
                }
            },
            
            # ⚡ 开源高速配置
            "opensource_fast": {
                "name": "⚡ 开源高速 (Together AI)",
                "provider": "together",
                "deep_think_llm": "Qwen/Qwen2-72B-Instruct",
                "quick_think_llm": "Qwen/Qwen2.5-7B-Instruct",
                "description": "开源模型丰富，性价比高",
                "pros": [
                    "开源模型丰富",
                    "性价比高",
                    "社区支持好",
                    "更新频繁"
                ],
                "cons": [
                    "需要付费",
                    "模型质量参差不齐"
                ],
                "use_cases": [
                    "开源项目开发",
                    "研究实验",
                    "成本敏感应用",
                    "模型对比测试"
                ],
                "setup_difficulty": "简单",
                "cost": "付费 ($0.2-1/M tokens)",
                "api_key_required": True
            },
            
            # 🔬 专业版配置
            "professional": {
                "name": "🔬 专业版 (OpenAI)",
                "provider": "openai",
                "deep_think_llm": "gpt-4o",
                "quick_think_llm": "gpt-4o-mini",
                "description": "业界标杆，最稳定可靠",
                "pros": [
                    "业界标杆",
                    "最稳定可靠",
                    "文档完善",
                    "技术支持好"
                ],
                "cons": [
                    "成本最高",
                    "中文能力一般"
                ],
                "use_cases": [
                    "企业级应用",
                    "关键业务分析",
                    "高可靠性要求",
                    "国际市场分析"
                ],
                "setup_difficulty": "简单",
                "cost": "付费 ($2.5-15/M tokens)",
                "api_key_required": True
            }
        }
    
    def get_recommendation_by_use_case(self, use_case: str) -> List[str]:
        """根据使用场景获取推荐配置"""
        recommendations = []
        
        use_case_mapping = {
            "个人投资": ["balanced_recommended", "high_speed_free"],
            "专业分析": ["intelligent_premium", "professional"],
            "企业部署": ["local_deployment", "professional"],
            "开发测试": ["high_speed_free", "opensource_fast"],
            "教学演示": ["high_speed_free", "balanced_recommended"],
            "数据隐私": ["local_deployment"],
            "高频交易": ["high_speed_free", "local_deployment"],
            "成本敏感": ["high_speed_free", "balanced_recommended", "opensource_fast"]
        }
        
        return use_case_mapping.get(use_case, ["balanced_recommended"])
    
    def get_recommendation_by_budget(self, budget: str) -> List[str]:
        """根据预算获取推荐配置"""
        budget_mapping = {
            "免费": ["high_speed_free", "balanced_recommended", "local_deployment"],
            "低预算": ["opensource_fast", "balanced_recommended"],
            "中预算": ["intelligent_premium", "opensource_fast"],
            "高预算": ["professional", "intelligent_premium"]
        }
        
        return budget_mapping.get(budget, ["balanced_recommended"])
    
    def generate_setup_commands(self, config_key: str) -> str:
        """生成配置设置命令"""
        if config_key not in self.recommendations:
            return "配置不存在"
        
        config = self.recommendations[config_key]
        
        commands = f"""# {config['name']} 配置设置
# 1. 环境变量设置
export LLM_PROVIDER={config['provider']}
export DEEP_THINK_LLM={config['deep_think_llm']}
export QUICK_THINK_LLM={config['quick_think_llm']}

# 2. .env 文件配置
echo "LLM_PROVIDER={config['provider']}" >> .env
echo "DEEP_THINK_LLM={config['deep_think_llm']}" >> .env
echo "QUICK_THINK_LLM={config['quick_think_llm']}" >> .env"""

        # 添加API密钥配置
        if config.get('api_key_required', False):
            provider_key_map = {
                "openai": "OPENAI_API_KEY",
                "groq": "GROQ_API_KEY", 
                "openrouter": "OPENROUTER_API_KEY",
                "together": "TOGETHER_API_KEY",
                "google": "GOOGLE_API_KEY"
            }
            
            if config['provider'] in provider_key_map:
                key_name = provider_key_map[config['provider']]
                commands += f"""
echo "{key_name}=your_api_key_here" >> .env"""

        # 添加特殊配置
        if config['provider'] == 'ollama':
            commands += f"""

# 3. Ollama 特殊配置
# 安装 Ollama (如果未安装)
curl -fsSL https://ollama.ai/install.sh | sh

# 下载模型
ollama pull {config['deep_think_llm']}
ollama pull {config['quick_think_llm']}

# 启动 Ollama 服务
ollama serve"""

        commands += f"""

# 4. 验证配置
python scripts/validate_model_config.py

# 5. 测试运行
python scripts/test_all_improvements.py"""

        return commands
    
    def get_all_recommendations(self) -> Dict[str, Dict[str, Any]]:
        """获取所有推荐配置"""
        return self.recommendations
    
    def get_recommendation(self, config_key: str) -> Dict[str, Any]:
        """获取特定推荐配置"""
        return self.recommendations.get(config_key, {})

# 全局实例
model_recommendations = ModelRecommendations()

def get_recommended_configs_by_scenario(scenario: str) -> List[Dict[str, Any]]:
    """根据场景获取推荐配置"""
    config_keys = model_recommendations.get_recommendation_by_use_case(scenario)
    return [model_recommendations.get_recommendation(key) for key in config_keys]

def get_setup_guide(config_key: str) -> str:
    """获取配置设置指南"""
    return model_recommendations.generate_setup_commands(config_key)
