#!/usr/bin/env python3
"""
TradingAgents Web应用启动脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """启动Web应用"""
    
    # 获取项目根目录
    project_root = Path(__file__).parent.parent
    web_app_dir = project_root / "web_app"
    
    print("🚀 启动 TradingAgents Web应用")
    print("=" * 50)
    
    # 检查依赖
    print("检查依赖...")
    try:
        import streamlit
        print("✅ Streamlit 已安装")
    except ImportError:
        print("❌ Streamlit 未安装，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "plotly"])
        print("✅ 依赖安装完成")
    
    # 检查配置
    env_file = project_root / ".env"
    if not env_file.exists():
        print("⚠️  警告: .env 文件不存在，请先配置环境变量")
        print("   可以复制 .env.example 并修改配置")
    else:
        print("✅ 配置文件存在")
    
    # 启动应用
    print(f"\n🌐 启动Web应用...")
    print(f"📁 应用目录: {web_app_dir}")
    print(f"🔗 访问地址: http://localhost:8501")
    print("\n按 Ctrl+C 停止应用")
    print("=" * 50)
    
    try:
        # 切换到web_app目录并启动streamlit
        os.chdir(web_app_dir)
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
