#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
歇后语探索器共享功能模块
提供可在游戏和独立探索器中复用的核心功能
"""

import json
import random
import re
from collections import Counter
from typing import List, Dict, Optional
from pathlib import Path

from nicegui import ui
from xiehouyu_explorer import XiehouyuExplorer


class ExplorerShared:
    """探索器共享功能类"""
    
    def __init__(self):
        self.explorer = XiehouyuExplorer()
        self.stats = self.explorer.stats()
        
        # 主题色彩配置（与游戏风格统一）
        self.primary_color = '#3B82F6'  # 蓝色
        self.secondary_color = '#10B981'  # 绿色
        self.accent_color = '#F59E0B'  # 橙色
        self.danger_color = '#EF4444'  # 红色
        
    def create_stats_card(self, title: str, value: str, icon: str, color: str = 'blue'):
        """创建统计卡片"""
        with ui.card().classes(f'min-w-48 bg-gradient-to-br from-{color}-400 to-{color}-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105'):
            with ui.card_section().classes('text-center'):
                ui.icon(icon, size='3em').classes('mb-2')
                ui.label(title).classes('text-lg font-medium opacity-90')
                ui.label(value).classes('text-3xl font-bold mt-2')
    
    def create_xiehouyu_card(self, item: Dict, show_answer: bool = True):
        """创建歇后语卡片"""
        with ui.card().classes('w-full shadow-lg hover:shadow-xl transition-all duration-300 border-l-4 border-blue-500 bg-gradient-to-r from-blue-50 to-indigo-50'):
            with ui.card_section():
                with ui.row().classes('items-center'):
                    ui.icon('format_quote', size='1.5em').classes('text-blue-500 mr-2')
                    ui.label(item['riddle']).classes('text-lg font-semibold text-gray-800')
                
                if show_answer:
                    with ui.row().classes('items-center mt-3'):
                        ui.icon('lightbulb', size='1.2em').classes('text-amber-500 mr-2')
                        ui.label(item['answer']).classes('text-base text-gray-700 bg-amber-50 px-3 py-2 rounded-lg border border-amber-200')
    
    def show_loading(self, message: str = '加载中...'):
        """显示加载动画"""
        with ui.row().classes('w-full justify-center items-center py-8'):
            ui.spinner('dots', size='lg', color='primary')
            ui.label(message).classes('ml-4 text-lg text-gray-600')
            
    def show_empty_state(self, message: str, icon: str = 'search_off'):
        """显示空状态"""
        with ui.column().classes('w-full items-center py-12'):
            ui.icon(icon, size='4em').classes('text-gray-400 mb-4')
            ui.label(message).classes('text-xl text-gray-500 text-center')

    def create_home_content(self):
        """创建探索器首页内容"""
        with ui.column().classes('flex-1 p-6 items-center justify-center w-full content-wrapper'):
            # 欢迎区域
            with ui.row().classes('w-full justify-center items-center mb-8'):
                with ui.card().classes('w-full max-w-7xl bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-xl'):
                    with ui.card_section().classes('text-center py-8'):
                        ui.icon('auto_awesome', size='4em').classes('mb-4')
                        ui.label('歇后语探索学习').classes('text-4xl font-bold mb-4')
                        ui.label('发现中华文化中的智慧瑰宝').classes('text-xl opacity-90')
            
            # 搜索功能
            with ui.row().classes('w-full justify-center items-center mb-8'):
                with ui.card().classes('w-full max-w-7xl p-6 bg-white shadow-lg'):
                    ui.label('🔍 搜索歇后语').classes('text-2xl font-bold text-center mb-4 text-blue-600')
                    with ui.row().classes('w-full gap-4 items-center'):
                        search_input = ui.input('请输入关键词搜索歇后语...').classes('flex-1')
                        search_button = ui.button('搜索', icon='search').classes('px-6')
                        
                    search_results = ui.column().classes('w-full mt-4')
                    
                    def perform_search():
                        query = search_input.value.strip()
                        search_results.clear()
                        
                        if not query:
                            with search_results:
                                ui.label('请输入搜索关键词').classes('text-gray-500 text-center')
                            return
                        
                        # 搜索逻辑
                        matches = []
                        for item in self.explorer.data:
                            if query in item['riddle'] or query in item['answer']:
                                matches.append(item)
                        
                        with search_results:
                            if matches:
                                ui.label(f'找到 {len(matches)} 条匹配的歇后语：').classes('text-lg font-semibold mb-4 text-center')
                                with ui.column().classes('w-full max-w-6xl mx-auto'):
                                    for match in matches[:10]:  # 显示前10条
                                        self.create_xiehouyu_card(match)
                                if len(matches) > 10:
                                    ui.label(f'还有 {len(matches) - 10} 条结果...').classes('text-gray-500 text-center mt-2')
                            else:
                                ui.label('未找到匹配的歇后语，请尝试其他关键词').classes('text-gray-500 text-center')
                    
                    search_button.on_click(perform_search)
                    search_input.on('keydown.enter', perform_search)
            
            # 精选推荐
            with ui.row().classes('w-full justify-center items-center mb-8'):
                with ui.card().classes('w-full max-w-7xl p-6 bg-white shadow-lg'):
                    ui.label('🎲 精选歇后语推荐').classes('text-3xl font-bold text-center mb-6 text-gray-800')
                    
                    random_container = ui.column().classes('w-full')
                    
                    def show_random_xiehys():
                        random_container.clear()
                        selected = self.explorer.random_xiehouyu(8)
                        
                        with random_container:
                            with ui.grid(columns=2).classes('w-full max-w-7xl mx-auto gap-4'):
                                for i, item in enumerate(selected, 1):
                                    with ui.card().classes('p-4 bg-gradient-to-r from-amber-50 to-orange-50 border-l-4 border-orange-400 hover:shadow-md transition-all hover:scale-105'):
                                        with ui.card_section():
                                            ui.label(f'第 {i} 条').classes('text-sm text-orange-600 mb-2')
                                            ui.label(item['riddle']).classes('text-lg font-semibold text-gray-800 mb-3')
                                            ui.separator().classes('my-2')
                                            ui.label(f"💡 {item['answer']}").classes('text-base text-blue-600')
                            
                            with ui.row().classes('w-full justify-center mt-6'):
                                ui.button('🔄 换一批', on_click=show_random_xiehys).classes('bg-orange-500 text-white px-6 py-2')
                    
                    show_random_xiehys()
            
            # 快速功能入口
            with ui.row().classes('w-full justify-center items-center mb-8'):
                with ui.row().classes('gap-8 justify-center max-w-7xl'):
                    with ui.card().classes('w-52 p-6 cursor-pointer hover:shadow-xl transition-all text-center hover:scale-105') as random_card:
                        ui.icon('casino').classes('text-5xl text-green-500 mb-3')
                        ui.label('🎲 随机探索').classes('text-xl font-semibold')
                        ui.label('发现意想不到的精彩').classes('text-sm text-gray-600 mt-2')
                        random_card.on('click', lambda: ui.navigate.to('/explorer/random'))
                    
                    with ui.card().classes('w-52 p-6 cursor-pointer hover:shadow-xl transition-all text-center hover:scale-105') as stats_card:
                        ui.icon('analytics').classes('text-5xl text-purple-500 mb-3')
                        ui.label('📊 数据统计').classes('text-xl font-semibold')
                        ui.label('了解有趣的数据').classes('text-sm text-gray-600 mt-2')
                        stats_card.on('click', lambda: ui.navigate.to('/explorer/stats'))
                        
                    with ui.card().classes('w-52 p-6 cursor-pointer hover:shadow-xl transition-all text-center hover:scale-105') as game_card:
                        ui.icon('videogame_asset').classes('text-5xl text-red-500 mb-3')
                        ui.label('🎮 返回游戏').classes('text-xl font-semibold')
                        ui.label('开始答题挑战').classes('text-sm text-gray-600 mt-2')
                        game_card.on('click', lambda: ui.navigate.to('/'))
            
            # 统计信息
            with ui.row().classes('w-full justify-center mt-8'):
                with ui.row().classes('gap-8 justify-center max-w-7xl'):
                    ui.label(f'📚 收录 {self.stats["total_xiehouyu"]:,} 条歇后语').classes('text-lg text-gray-600 bg-gray-100 px-4 py-2 rounded-full')
                    ui.label(f'📏 平均长度 {self.stats["avg_riddle_length"]} 字符').classes('text-lg text-gray-600 bg-gray-100 px-4 py-2 rounded-full')

    def create_random_content(self):
        """创建随机探索页面内容"""
        with ui.column().classes('flex-1 p-6 items-center justify-center w-full content-wrapper'):
            ui.label('🎲 随机探索').classes('text-3xl font-bold text-center mb-8 text-gray-800')
            
            # 控制面板
            with ui.row().classes('w-full justify-center items-center mb-8'):
                with ui.card().classes('w-full max-w-6xl bg-gradient-to-r from-green-50 to-blue-50'):
                    with ui.card_section():
                        ui.label('🎯 探索设置').classes('text-xl font-semibold mb-4')
                    
                        with ui.row().classes('w-full items-center space-x-6'):
                            with ui.column().classes('flex-1'):
                                ui.label('数量选择').classes('text-base font-medium mb-2')
                                count_slider = ui.slider(min=1, max=20, value=5, step=1).classes('w-full')
                                count_label = ui.label('5个').classes('text-center text-lg font-semibold text-blue-600')
                                count_slider.on('update:model-value', lambda e: count_label.set_text(f'{int(e.args)}个'))
                            
                            ui.separator().props('vertical')
                            
                            with ui.column():
                                ui.label('快速选择').classes('text-base font-medium mb-2')
                                with ui.row().classes('gap-2'):
                                    ui.button('1个', on_click=lambda: count_slider.set_value(1)).classes('bg-blue-100 text-blue-700')
                                    ui.button('5个', on_click=lambda: count_slider.set_value(5)).classes('bg-green-100 text-green-700')
                                    ui.button('10个', on_click=lambda: count_slider.set_value(10)).classes('bg-purple-100 text-purple-700')
                                    ui.button('20个', on_click=lambda: count_slider.set_value(20)).classes('bg-orange-100 text-orange-700')
            
            # 操作按钮
            with ui.row().classes('w-full justify-center items-center mb-8'):
                with ui.row().classes('gap-4 justify-center'):
                    ui.button('🎲 试试手气！', 
                             on_click=lambda: discover_random(int(count_slider.value))
                             ).classes('bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 text-xl font-bold shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300')
                    
                    ui.button('🔄 再来一次', 
                             on_click=lambda: discover_random(int(count_slider.value))
                             ).classes('bg-gradient-to-r from-green-500 to-blue-500 text-white px-6 py-3 text-lg font-semibold')
                             
                    ui.button('🏠 返回首页', 
                             on_click=lambda: ui.navigate.to('/explorer')
                             ).classes('bg-gradient-to-r from-gray-500 to-gray-600 text-white px-6 py-3 text-lg font-semibold')
            
            # 分类探索
            ui.label('🏷️ 按主题探索').classes('text-2xl font-bold text-center mb-4 text-gray-800')
            with ui.row().classes('w-full justify-center items-center mb-8'):
                with ui.row().classes('max-w-6xl justify-center gap-3 flex-wrap'):
                    categories = [
                        ('🐱 动物', '猫|狗|鸟|鱼|虎|龙|蛇|马|羊|猴|鸡|猪|牛|鼠'),
                        ('🌸 植物', '花|树|草|叶|果|瓜|豆|米|麦|菜'),
                        ('🌈 颜色', '红|黄|蓝|绿|白|黑|紫|粉'),
                        ('🔢 数字', '一|二|三|四|五|六|七|八|九|十'),
                        ('🏠 生活', '家|房|门|窗|床|桌|椅|锅|碗'),
                        ('🎭 文化', '书|笔|戏|歌|画|琴|棋|诗')
                    ]
                    
                    for category_name, pattern in categories:
                        ui.button(category_name, 
                                 on_click=lambda p=pattern: discover_by_category(p, int(count_slider.value))
                                 ).classes('bg-white border-2 border-gray-300 text-gray-700 hover:border-blue-500 hover:text-blue-600 px-4 py-2 font-medium')
            
            # 结果展示区域
            with ui.row().classes('w-full justify-center'):
                result_container = ui.column().classes('w-full max-w-7xl')
            
            def discover_random(count: int):
                result_container.clear()
                
                with result_container:
                    self.show_loading(f'正在为你挑选 {count} 个精彩歇后语...')
                
                ui.timer(0.8, lambda: display_random_results(count), once=True)
            
            def discover_by_category(pattern: str, count: int):
                result_container.clear()
                
                with result_container:
                    self.show_loading('正在按主题搜索...')
                
                ui.timer(0.5, lambda: display_category_results(pattern, count), once=True)
            
            def display_random_results(count: int):
                result_container.clear()
                
                results = self.explorer.random_xiehouyu(count)
                
                with result_container:
                    with ui.row().classes('w-full justify-center items-center mb-6'):
                        ui.icon('stars', size='2em').classes('text-yellow-500 mr-3')
                        ui.label(f'为你精选了 {len(results)} 个歇后语').classes('text-2xl font-bold text-yellow-600')
                    
                    with ui.column().classes('w-full max-w-6xl mx-auto'):
                        for i, item in enumerate(results, 1):
                            with ui.card().classes('w-full mb-4 shadow-lg bg-gradient-to-r from-yellow-50 to-orange-50 border-l-4 border-yellow-400'):
                                with ui.card_section():
                                    ui.label(f'第 {i} 个').classes('text-sm text-yellow-600 font-medium mb-2')
                                    with ui.row().classes('items-center'):
                                        ui.icon('format_quote', size='1.5em').classes('text-yellow-500 mr-2')
                                        ui.label(item['riddle']).classes('text-lg font-semibold text-gray-800')
                                    
                                    with ui.row().classes('items-center mt-3'):
                                        ui.icon('lightbulb', size='1.2em').classes('text-orange-500 mr-2')
                                        ui.label(item['answer']).classes('text-base text-gray-700 bg-orange-100 px-3 py-2 rounded-lg border border-orange-200')
            
            def display_category_results(pattern: str, count: int):
                result_container.clear()
                
                # 搜索匹配的歇后语
                all_matches = []
                for item in self.explorer.data:
                    if re.search(pattern, item['riddle']) or re.search(pattern, item['answer']):
                        all_matches.append(item)
                
                # 随机选择指定数量
                if all_matches:
                    results = random.sample(all_matches, min(count, len(all_matches)))
                else:
                    results = []
                
                with result_container:
                    if results:
                        ui.label(f'🎯 在该主题下找到 {len(results)} 个歇后语').classes('text-2xl font-bold text-center mb-6 text-green-600')
                        
                        with ui.column().classes('w-full max-w-6xl mx-auto'):
                            for item in results:
                                self.create_xiehouyu_card(item)
                                ui.separator().classes('my-3')
                    else:
                        self.show_empty_state('该主题暂时没有找到相关歇后语', 'category')
            
            # 初始显示一些示例
            discover_random(3)

    def create_stats_content(self):
        """创建统计页面内容"""
        with ui.column().classes('flex-1 p-6 items-center justify-center w-full content-wrapper'):
            ui.label('📊 数据统计分析').classes('text-3xl font-bold text-center mb-8 text-gray-800')
            
            # 基础统计卡片
            ui.label('📈 基础统计').classes('text-2xl font-semibold mb-6 text-gray-700')
            
            with ui.row().classes('w-full justify-center mb-8'):
                with ui.row().classes('gap-6 justify-center flex-wrap max-w-7xl'):
                    stats = self.stats
                    self.create_stats_card('总歇后语', f"{stats['total_xiehouyu']:,}", 'inventory', 'blue')
                    self.create_stats_card('独特谜面', f"{stats['unique_riddles']:,}", 'psychology', 'green')
                    self.create_stats_card('独特答案', f"{stats['unique_answers']:,}", 'lightbulb', 'yellow')
                    self.create_stats_card('多答案谜面', f"{stats['multi_answer_riddles']:,}", 'dynamic_feed', 'purple')
            
            # 长度分析
            ui.label('📏 长度分析').classes('text-2xl font-semibold mb-6 text-gray-700')
            
            with ui.row().classes('w-full justify-center mb-8'):
                with ui.row().classes('gap-6 justify-center max-w-7xl'):
                    self.create_stats_card('谜面平均长度', f"{stats['avg_riddle_length']} 字", 'straighten', 'indigo')
                    self.create_stats_card('答案平均长度', f"{stats['avg_answer_length']} 字", 'height', 'pink')
            
            # 高频词汇分析
            ui.label('🔤 高频词汇').classes('text-2xl font-semibold mb-6 text-gray-700')
            
            with ui.row().classes('w-full justify-center mb-8'):
                with ui.row().classes('gap-8 justify-center max-w-7xl'):
                    # 谜面高频词
                    with ui.card().classes('flex-1 max-w-lg'):
                        with ui.card_section():
                            ui.label('谜面高频词').classes('text-xl font-bold text-center mb-4 text-blue-600')
                            
                            riddle_words = self.explorer.most_common_words('riddle', 8)
                            for word, count in riddle_words:
                                with ui.row().classes('w-full justify-between items-center py-1'):
                                    ui.label(word).classes('text-base font-medium')
                                    ui.badge(str(count)).classes('bg-blue-100 text-blue-800')
                    
                    # 答案高频词
                    with ui.card().classes('flex-1 max-w-lg'):
                        with ui.card_section():
                            ui.label('答案高频词').classes('text-xl font-bold text-center mb-4 text-green-600')
                            
                            answer_words = self.explorer.most_common_words('answer', 8)
                            for word, count in answer_words:
                                with ui.row().classes('w-full justify-between items-center py-1'):
                                    ui.label(word).classes('text-base font-medium')
                                    ui.badge(str(count)).classes('bg-green-100 text-green-800')
            
            # 返回按钮
            with ui.row().classes('w-full justify-center mt-8'):
                with ui.row().classes('gap-4 justify-center'):
                    ui.button('🏠 返回首页', on_click=lambda: ui.navigate.to('/explorer')).classes('bg-blue-500 text-white px-6 py-2')
                    ui.button('🎮 返回游戏', on_click=lambda: ui.navigate.to('/')).classes('bg-green-500 text-white px-6 py-2')


# 创建全局共享实例
explorer_shared = ExplorerShared()