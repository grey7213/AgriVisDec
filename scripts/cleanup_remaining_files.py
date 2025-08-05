#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清理残留文件脚本
删除用户手动清空但仍存在的文件
"""

import os
from pathlib import Path

def cleanup_remaining_files():
    """清理残留的空文件"""
    print("🧹 清理残留文件...")
    
    # 需要删除的文件列表
    files_to_remove = [
        'config.py',
        'PROJECT_STATUS.md',
        'TASK_COMPLETION_SUMMARY.md', 
        'FIXES_COMPLETION_SUMMARY.md',
        'CHINA_MAP_FIX_SUMMARY.md',
        'NAN_FIX_COMPLETION_SUMMARY.md',
        'MULTI_DATABASE_GUIDE.md',
        'SOLUTION_SUMMARY.md'
    ]
    
    removed_count = 0
    
    for file_name in files_to_remove:
        file_path = Path(file_name)
        
        if file_path.exists():
            try:
                # 检查文件是否为空或只有很少内容
                file_size = file_path.stat().st_size
                
                if file_size < 100:  # 小于100字节认为是空文件
                    file_path.unlink()
                    print(f"  ✅ 删除空文件: {file_name}")
                    removed_count += 1
                else:
                    print(f"  ⚠️ 跳过非空文件: {file_name} ({file_size} bytes)")
                    
            except Exception as e:
                print(f"  ❌ 删除失败: {file_name} - {str(e)}")
        else:
            print(f"  ℹ️ 文件不存在: {file_name}")
    
    print(f"\n📊 清理完成: 删除了 {removed_count} 个文件")
    
    # 清理临时目录
    temp_dir = Path('temp')
    if temp_dir.exists() and temp_dir.is_dir():
        try:
            # 检查temp目录是否为空
            temp_files = list(temp_dir.iterdir())
            if not temp_files:
                temp_dir.rmdir()
                print("  ✅ 删除空的temp目录")
            else:
                print(f"  ℹ️ temp目录不为空，包含 {len(temp_files)} 个文件")
        except Exception as e:
            print(f"  ❌ 清理temp目录失败: {str(e)}")
    
    return removed_count

def main():
    """主函数"""
    print("🚀 开始清理残留文件")
    print("=" * 50)
    
    removed_count = cleanup_remaining_files()
    
    print("\n" + "=" * 50)
    if removed_count > 0:
        print("✅ 清理完成！项目结构更加整洁")
    else:
        print("ℹ️ 没有需要清理的文件")

if __name__ == "__main__":
    main()
