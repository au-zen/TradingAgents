#!/usr/bin/env python3
"""
从远程GitHub仓库删除.env文件的脚本
"""

import requests
import os
import sys
from pathlib import Path

def remove_env_from_github():
    """从GitHub仓库删除.env文件"""
    
    # GitHub API配置
    owner = "au-zen"
    repo = "TradingAgents"
    file_path = ".env"
    
    # 从环境变量获取GitHub token（如果有的话）
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("❌ 未找到GITHUB_TOKEN环境变量")
        print("💡 请设置GitHub Personal Access Token:")
        print("   export GITHUB_TOKEN=your_token_here")
        return False
    
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'TradingAgents-Script'
    }
    
    # 获取文件信息
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    
    print(f"🔍 检查远程仓库中的{file_path}文件...")
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 404:
            print(f"✅ {file_path}文件在远程仓库中不存在")
            return True
        elif response.status_code != 200:
            print(f"❌ 获取文件信息失败: {response.status_code}")
            print(f"响应: {response.text}")
            return False
        
        file_info = response.json()
        sha = file_info['sha']
        
        print(f"📋 找到{file_path}文件，SHA: {sha}")
        
        # 删除文件
        delete_data = {
            "message": "🔒 删除.env文件以保护敏感信息",
            "sha": sha
        }
        
        print(f"🗑️  正在删除远程{file_path}文件...")
        
        delete_response = requests.delete(url, headers=headers, json=delete_data)
        
        if delete_response.status_code == 200:
            print(f"✅ 成功删除远程{file_path}文件")
            return True
        else:
            print(f"❌ 删除文件失败: {delete_response.status_code}")
            print(f"响应: {delete_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 操作失败: {e}")
        return False

def main():
    """主函数"""
    print("🔒 GitHub远程.env文件删除工具")
    print("=" * 40)
    
    success = remove_env_from_github()
    
    if success:
        print("\n🎉 操作完成！")
        print("💡 建议:")
        print("1. 确保本地.gitignore包含.env文件")
        print("2. 创建.env.example作为模板文件")
        print("3. 在README中说明如何配置环境变量")
        return 0
    else:
        print("\n❌ 操作失败")
        print("💡 可能的解决方案:")
        print("1. 检查GitHub Token权限")
        print("2. 确认仓库名称正确")
        print("3. 手动在GitHub网页界面删除文件")
        return 1

if __name__ == "__main__":
    sys.exit(main())
