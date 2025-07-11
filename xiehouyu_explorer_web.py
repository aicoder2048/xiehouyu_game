#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
歇后语探索器 Web 应用
面向12岁中国青少年的现代化歇后语学习平台
"""

import json
import random
import re
from collections import Counter
from typing import List, Dict, Optional
from pathlib import Path

from nicegui import ui, app
from xiehouyu_explorer import XiehouyuExplorer


class XiehouyuWebApp:
    def __init__(self):
        self.explorer = XiehouyuExplorer()
        self.stats = self.explorer.stats()
        
        # 主题色彩配置（适合青少年）
        self.primary_color = '#3B82F6'  # 蓝色
        self.secondary_color = '#10B981'  # 绿色
        self.accent_color = '#F59E0B'  # 橙色
        self.danger_color = '#EF4444'  # 红色
        self.bg_gradient = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        
        # 初始化应用
        self.setup_app()
        
    def setup_app(self):
        """设置应用配置"""
        app.add_static_files('/static', (Path(__file__).parent / 'static').as_posix())
        
    def display_search_results(self, results, query):
        """显示搜索结果"""
        # 清空页面并显示搜索结果
        ui.clear()
        self.create_header()
        
        with ui.column().classes('flex-1 p-6 items-center'):
            ui.label(f'🔍 搜索结果 - "{ query }"').classes('text-3xl font-bold mb-6 text-center text-blue-600')
            
            if not results:
                with ui.card().classes('w-full max-w-6xl mx-auto p-8 text-center'):
                    ui.icon('search_off').classes('text-6xl text-gray-400 mb-4')
                    ui.label('没有找到相关的歇后语').classes('text-xl text-gray-600 mb-2')
                    ui.label('请尝试其他关键词').classes('text-gray-500')
                    ui.button('返回首页', on_click=lambda: ui.navigate.to('/')).classes('mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg')
            else:
                ui.label(f'找到 {len(results)} 条相关歇后语').classes('text-lg text-gray-600 mb-6')
                
                with ui.column().classes('w-full max-w-6xl gap-4 mx-auto'):
                    for i, item in enumerate(results, 1):
                        with ui.card().classes('w-full p-4 hover:shadow-lg transition-all'):
                            with ui.row().classes('w-full items-start gap-4'):
                                ui.label(f'{i}.').classes('text-lg font-bold text-blue-600 w-8')
                                with ui.column().classes('flex-1'):
                                    ui.label(item['riddle']).classes('text-lg font-semibold text-gray-800 mb-2')
                                    ui.label(f"答案：{item['answer']}").classes('text-base text-blue-600')
                
                with ui.row().classes('w-full justify-center mt-6 gap-4'):
                    ui.button('返回首页', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-600 text-white px-6 py-2 rounded-lg')
                    ui.button('重新搜索', on_click=lambda: ui.navigate.to('/')).classes('bg-gray-600 text-white px-6 py-2 rounded-lg')
        
        self.create_footer()

    def create_header(self):
        """创建页面头部导航"""
        with ui.header(elevated=True).style('background: linear-gradient(90deg, #3B82F6, #10B981)'):
            with ui.row().classes('w-full justify-between items-center'):
                with ui.row().classes('items-center'):
                    ui.icon('school', size='2em').classes('text-white mr-2')
                    ui.label('歇后语探索器').classes('text-white text-2xl font-bold')
                    
                with ui.row().classes('items-center space-x-4'):
                    ui.button('🏠 首页', on_click=lambda: ui.navigate.to('/')).classes('text-white bg-transparent hover:bg-white/20')
                    ui.button('🎲 探索', on_click=lambda: ui.navigate.to('/random')).classes('text-white bg-transparent hover:bg-white/20')
                    ui.button('📊 统计', on_click=lambda: ui.navigate.to('/stats')).classes('text-white bg-transparent hover:bg-white/20')
    
    def create_footer(self):
        """创建页面底部"""
        with ui.footer().classes('bg-gray-100 py-4 mt-8'):
            with ui.row().classes('w-full justify-center'):
                ui.label('🌟 传承中华文化，学习传统智慧 🌟').classes('text-gray-600 text-center')
                
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
    
    def create_search_box(self, callback, placeholder: str = '输入关键词搜索...'):
        """创建搜索框"""
        with ui.row().classes('w-full max-w-2xl mx-auto items-center space-x-3'):
            search_input = ui.input(placeholder=placeholder).classes('flex-1 text-lg').props('outlined dense')
            search_input.on('keydown.enter', lambda: callback(search_input.value))
            ui.button('搜索', on_click=lambda: callback(search_input.value)).classes('bg-blue-500 text-white px-6 py-3 text-lg hover:bg-blue-600')
        return search_input
        
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
            

app_instance = XiehouyuWebApp()


@ui.page('/')
def home_page():
    """首页"""
    app_instance.create_header()
    
    with ui.column().classes('flex-1 p-6 items-center justify-center w-full content-wrapper'):
        # 欢迎区域 - 居中设计
        with ui.row().classes('w-full justify-center items-center mb-8'):
            with ui.card().classes('w-full max-w-7xl bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-xl'):
                with ui.card_section().classes('text-center py-8'):
                    ui.icon('auto_awesome', size='4em').classes('mb-4')
                    ui.label('欢迎来到歇后语探索器！').classes('text-4xl font-bold mb-4')
                    ui.label('发现中华文化中的智慧瑰宝').classes('text-xl opacity-90')
        
        # 集成搜索功能 - 主要内容
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
                    for item in app_instance.explorer.data:
                        if query in item['riddle'] or query in item['answer']:
                            matches.append(item)
                    
                    with search_results:
                        if matches:
                            ui.label(f'找到 {len(matches)} 条匹配的歇后语：').classes('text-lg font-semibold mb-4 text-center')
                            with ui.column().classes('w-full max-w-6xl mx-auto'):
                                for match in matches[:10]:  # 显示前10条
                                    app_instance.create_xiehouyu_card(match)
                            if len(matches) > 10:
                                ui.label(f'还有 {len(matches) - 10} 条结果...').classes('text-gray-500 text-center mt-2')
                        else:
                            ui.label('未找到匹配的歇后语，请尝试其他关键词').classes('text-gray-500 text-center')
                
                search_button.on_click(perform_search)
                search_input.on('keydown.enter', perform_search)
        
        # 今日推荐歇后语 - 核心内容区
        with ui.row().classes('w-full justify-center items-center mb-8'):
            with ui.card().classes('w-full max-w-7xl p-6 bg-white shadow-lg'):
                ui.label('🎲 精选歇后语推荐').classes('text-3xl font-bold text-center mb-6 text-gray-800')
                
                random_container = ui.column().classes('w-full')
                
                def show_random_xiehys():
                    random_container.clear()
                    selected = app_instance.explorer.random_xiehouyu(8)
                    
                    with random_container:
                        # 使用网格布局展示更多歇后语
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
        
        # 快速功能入口 - 增强样式
        with ui.row().classes('w-full justify-center items-center mb-8'):
            with ui.row().classes('gap-8 justify-center max-w-7xl'):
                with ui.card().classes('w-52 p-6 cursor-pointer hover:shadow-xl transition-all text-center hover:scale-105') as random_card:
                    ui.icon('casino').classes('text-5xl text-green-500 mb-3')
                    ui.label('🎲 随机探索').classes('text-xl font-semibold')
                    ui.label('发现意想不到的精彩').classes('text-sm text-gray-600 mt-2')
                    random_card.on('click', lambda: ui.navigate.to('/random'))
                
                with ui.card().classes('w-52 p-6 cursor-pointer hover:shadow-xl transition-all text-center hover:scale-105') as stats_card:
                    ui.icon('analytics').classes('text-5xl text-purple-500 mb-3')
                    ui.label('📊 数据统计').classes('text-xl font-semibold')
                    ui.label('了解有趣的数据').classes('text-sm text-gray-600 mt-2')
                    stats_card.on('click', lambda: ui.navigate.to('/stats'))
                
        
        # 简化的统计信息
        with ui.row().classes('w-full justify-center mt-8'):
            with ui.row().classes('gap-8 justify-center max-w-7xl'):
                ui.label(f'📚 收录 {app_instance.stats["total_xiehouyu"]:,} 条歇后语').classes('text-lg text-gray-600 bg-gray-100 px-4 py-2 rounded-full')
                ui.label(f'📏 平均长度 {app_instance.stats["avg_riddle_length"]} 字符').classes('text-lg text-gray-600 bg-gray-100 px-4 py-2 rounded-full')
    
    app_instance.create_footer()





@ui.page('/random')
def random_page():
    """随机探索页面"""
    app_instance.create_header()
    
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
                app_instance.show_loading(f'正在为你挑选 {count} 个精彩歇后语...')
            
            ui.timer(0.8, lambda: display_random_results(count), once=True)
        
        def discover_by_category(pattern: str, count: int):
            result_container.clear()
            
            with result_container:
                app_instance.show_loading('正在按主题搜索...')
            
            ui.timer(0.5, lambda: display_category_results(pattern, count), once=True)
        
        def display_random_results(count: int):
            result_container.clear()
            
            results = app_instance.explorer.random_xiehouyu(count)
            
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
            for item in app_instance.explorer.data:
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
                            app_instance.create_xiehouyu_card(item)
                            ui.separator().classes('my-3')
                else:
                    app_instance.show_empty_state('该主题暂时没有找到相关歇后语', 'category')
        
        # 初始显示一些示例
        discover_random(3)
    
    app_instance.create_footer()


@ui.page('/stats')
def stats_page():
    """统计页面"""
    app_instance.create_header()
    
    with ui.column().classes('flex-1 p-6 items-center justify-center w-full content-wrapper'):
        ui.label('📊 数据统计分析').classes('text-3xl font-bold text-center mb-8 text-gray-800')
        
        # 基础统计卡片
        ui.label('📈 基础统计').classes('text-2xl font-semibold mb-6 text-gray-700')
        
        with ui.row().classes('w-full justify-center mb-8'):
            with ui.row().classes('gap-6 justify-center flex-wrap max-w-7xl'):
                stats = app_instance.stats
                app_instance.create_stats_card('总歇后语', f"{stats['total_xiehouyu']:,}", 'inventory', 'blue')
                app_instance.create_stats_card('独特谜面', f"{stats['unique_riddles']:,}", 'psychology', 'green')
                app_instance.create_stats_card('独特答案', f"{stats['unique_answers']:,}", 'lightbulb', 'yellow')
                app_instance.create_stats_card('多答案谜面', f"{stats['multi_answer_riddles']:,}", 'dynamic_feed', 'purple')
        
        # 长度分析
        ui.label('📏 长度分析').classes('text-2xl font-semibold mb-6 text-gray-700')
        
        with ui.row().classes('w-full justify-center mb-8'):
            with ui.row().classes('gap-6 justify-center max-w-7xl'):
                app_instance.create_stats_card('谜面平均长度', f"{stats['avg_riddle_length']} 字", 'straighten', 'indigo')
                app_instance.create_stats_card('答案平均长度', f"{stats['avg_answer_length']} 字", 'height', 'pink')
        
        # 高频词汇分析
        ui.label('🔤 高频词汇').classes('text-2xl font-semibold mb-6 text-gray-700')
        
        with ui.row().classes('w-full justify-center mb-8'):
            with ui.row().classes('gap-8 justify-center max-w-7xl'):
                # 谜面高频词
                with ui.card().classes('flex-1 max-w-lg'):
                    with ui.card_section():
                        ui.label('谜面高频词').classes('text-xl font-bold text-center mb-4 text-blue-600')
                        
                        riddle_words = app_instance.explorer.most_common_words('riddle', 8)
                        for word, count in riddle_words:
                            with ui.row().classes('w-full justify-between items-center py-1'):
                                ui.label(word).classes('text-base font-medium')
                                ui.badge(str(count)).classes('bg-blue-100 text-blue-800')
                
                # 答案高频词
                with ui.card().classes('flex-1 max-w-lg'):
                    with ui.card_section():
                        ui.label('答案高频词').classes('text-xl font-bold text-center mb-4 text-green-600')
                        
                        answer_words = app_instance.explorer.most_common_words('answer', 8)
                        for word, count in answer_words:
                            with ui.row().classes('w-full justify-between items-center py-1'):
                                ui.label(word).classes('text-base font-medium')
                                ui.badge(str(count)).classes('bg-green-100 text-green-800')
        
        # 长度分布分析
        ui.label('📊 长度分布').classes('text-2xl font-semibold mb-6 mt-8 text-gray-700')
        
        # 计算长度分布
        riddle_lengths = [len(item['riddle']) for item in app_instance.explorer.data]
        length_distribution = Counter(riddle_lengths)
        
        with ui.row().classes('w-full justify-center'):
            with ui.card().classes('w-full max-w-7xl'):
                with ui.card_section():
                    ui.label('谜面长度分布图').classes('text-lg font-semibold text-center mb-4')
                    
                    # 简单的长度分布展示
                    for length in sorted(length_distribution.keys())[:10]:  # 显示前10种长度
                        count = length_distribution[length]
                        percentage = (count / len(app_instance.explorer.data)) * 100
                        
                        with ui.row().classes('w-full items-center mb-2'):
                            ui.label(f'{length}字').classes('w-12 text-center font-medium')
                            
                            # 进度条
                            with ui.element('div').classes('flex-1 bg-gray-200 rounded-full h-6 mx-4'):
                                ui.element('div').classes(f'bg-blue-500 h-6 rounded-full').style(f'width: {min(percentage, 100)}%')
                            
                            ui.label(f'{count:,} ({percentage:.1f}%)').classes('w-24 text-right text-sm text-gray-600')
    
    app_instance.create_footer()



def create_requirements():
    """创建requirements.txt文件"""
    requirements_content = '''nicegui>=1.4.0
'''
    
    try:
        with open('requirements.txt', 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        print('✅ requirements.txt 已创建')
    except Exception as e:
        print(f'❌ 创建 requirements.txt 失败: {e}')


if __name__ in {"__main__", "__mp_main__"}:
    # 创建应用实例
    app_instance = XiehouyuWebApp()
    
    # 添加自定义CSS样式
    ui.add_head_html('''
    <style>
        body {
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .q-page {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            min-height: 100vh;
        }
        .content-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }
        .hover\\:scale-105:hover {
            transform: scale(1.05);
        }
        .transition-all {
            transition: all 0.3s ease;
        }
        .bg-gradient-to-r {
            background: linear-gradient(to right, var(--tw-gradient-stops));
        }
        .from-blue-500 {
            --tw-gradient-from: #3b82f6;
            --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgba(59, 130, 246, 0));
        }
        .to-purple-600 {
            --tw-gradient-to: #7c3aed;
        }
        .shadow-lg {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        .border-l-4 {
            border-left-width: 4px;
        }
        .animate-pulse {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: .5;
            }
        }
    </style>
    ''')
    
    # 设置页面配置
    ui.run(
        title='歇后语探索器 - 发现中华文化的智慧',
        favicon='🎭',
        port=8888,
        reload=False,
        show=True
    )