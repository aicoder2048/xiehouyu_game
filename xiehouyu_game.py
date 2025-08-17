#!/usr/bin/env python3
"""
Chinese Xiehouyu Competition Game

A simplified two-player competitive game using Chinese riddles (xiehouyu) with
child-friendly Bento Grid UI design built with NiceGUI.

Redesigned for separate riddles per player, no timer pressure, and improved UI.
"""

import asyncio
import json
from pathlib import Path
from typing import Optional

from nicegui import ui, app
from game_logic import GameState, GameConfig, GamePhase, PlayerSide, PlayerStats
from game_ui import GameUI, GameTheme
from xiehouyu_explorer import XiehouyuExplorer


class XiehouyuGame:
    """Main game application"""
    
    def __init__(self):
        self.xiehouyu_data = []
        self.game_state: Optional[GameState] = None
        self.game_ui: Optional[GameUI] = None
        self.load_data()
    
    def load_data(self):
        """Load xiehouyu data from JSON file"""
        try:
            data_file = Path('xiehouyu.json')
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    self.xiehouyu_data = json.load(f)
                ui.notify(f'已加载 {len(self.xiehouyu_data)} 条歇后语数据', type='positive')
            else:
                ui.notify('找不到 xiehouyu.json 数据文件', type='negative')
                self.xiehouyu_data = []
        except Exception as e:
            ui.notify(f'加载数据文件失败: {str(e)}', type='negative')
            self.xiehouyu_data = []
    
    def initialize_game(self):
        """Initialize game state and UI"""
        if not self.xiehouyu_data:
            ui.notify('无法开始游戏：没有数据', type='negative')
            return
        
        # Initialize game state
        config = GameConfig(
            total_rounds=12,
            points_per_correct=2,  # 基础得分2分
            bonus_for_correct=1    # 优先回答奖励1分
        )
        self.game_state = GameState(self.xiehouyu_data, config)
        
        # Initialize UI
        self.game_ui = GameUI(self.game_state)
    


# Global game instance
game_instance = XiehouyuGame()


def create_main_page():
    """Create the main game page"""
    # Set page configuration
    ui.page_title('歇后语对战游戏')
    
    # Add custom CSS for enhanced styling and masking
    ui.add_head_html(f'''
        <style>
            /* Global styles */
            body {{
                background: linear-gradient(135deg, {GameTheme.BACKGROUND} 0%, #E2E8F0 50%, #F0F4F8 100%);
                font-family: 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
                min-height: 100vh;
                position: relative;
                overflow-x: hidden;
            }}
            
            /* Animated background stars */
            body::before {{
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: radial-gradient(2px 2px at 20px 30px, #FFD700, transparent),
                           radial-gradient(2px 2px at 40px 70px, #FF69B4, transparent),
                           radial-gradient(1px 1px at 90px 40px, #00CED1, transparent),
                           radial-gradient(1px 1px at 130px 80px, #FFB347, transparent),
                           radial-gradient(2px 2px at 160px 30px, #98FB98, transparent);
                background-repeat: repeat;
                background-size: 200px 100px;
                animation: sparkle 3s linear infinite;
                pointer-events: none;
                z-index: -1;
            }}
            
            @keyframes sparkle {{
                0% {{
                    transform: translateY(0);
                    opacity: 0.5;
                }}
                50% {{
                    opacity: 1;
                }}
                100% {{
                    transform: translateY(-100px);
                    opacity: 0.5;
                }}
            }}
            
            /* Gradient text effect */
            .gradient-text {{
                background: linear-gradient(135deg, {GameTheme.PRIMARY_DARK} 0%, {GameTheme.SECONDARY_DARK} 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            
            /* Card hover effects */
            .card:hover {{
                transform: translateY(-2px);
                transition: transform 0.3s ease;
            }}
            
            /* Rainbow border animation */
            .rainbow-border {{
                position: relative;
                border-radius: 20px;
                overflow: hidden;
            }}
            
            .rainbow-border::before {{
                content: '';
                position: absolute;
                top: -2px;
                left: -2px;
                right: -2px;
                bottom: -2px;
                background: linear-gradient(45deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #8f00ff, #ff0000);
                background-size: 400% 400%;
                animation: rainbow-border 3s ease-in-out infinite;
                z-index: -1;
                border-radius: 20px;
            }}
            
            @keyframes rainbow-border {{
                0% {{
                    background-position: 0% 50%;
                }}
                50% {{
                    background-position: 100% 50%;
                }}
                100% {{
                    background-position: 0% 50%;
                }}
            }}
            
            /* Button animations */
            .start-btn:hover {{
                transform: translateY(-3px);
                box-shadow: 0 12px 40px rgba(72, 187, 120, 0.4);
            }}
            
            .reset-btn:hover {{
                transform: translateY(-3px);
                box-shadow: 0 12px 40px rgba(237, 137, 54, 0.4);
            }}
            
            /* Answer button effects */
            .answer-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                background: rgba(255, 255, 255, 1) !important;
                color: #2D3748 !important;
            }}
            
            /* Masking effect for hidden characters */
            .masked-char {{
                position: relative;
                display: inline-block;
                width: 1.2em;
                height: 1.2em;
                background: {GameTheme.MASK_COLOR};
                border-radius: 4px;
                vertical-align: middle;
                margin: 0 1px;
            }}
            
            .masked-char::before {{
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 0.8em;
                height: 0.8em;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 2px;
            }}
            
            /* Pulse animation for active elements */
            .pulse {{
                animation: pulse 2s infinite;
            }}
            
            @keyframes pulse {{
                0% {{
                    transform: scale(1);
                }}
                50% {{
                    transform: scale(1.02);
                }}
                100% {{
                    transform: scale(1);
                }}
            }}
            
            /* Bounce animation for correct answers */
            .bounce {{
                animation: bounce 0.6s ease-in-out;
            }}
            
            @keyframes bounce {{
                0%, 100% {{
                    transform: translateY(0);
                }}
                50% {{
                    transform: translateY(-8px);
                }}
            }}
            
            /* Shake animation for wrong answers */
            .shake {{
                animation: shake 0.5s ease-in-out;
            }}
            
            @keyframes shake {{
                0%, 100% {{
                    transform: translateX(0);
                }}
                25% {{
                    transform: translateX(-5px);
                }}
                75% {{
                    transform: translateX(5px);
                }}
            }}
            
            /* Ensure side-by-side layout */
            .game-panels {{
                display: flex !important;
                width: 100% !important;
                gap: 1rem !important;
                min-height: 300px;
            }}
            
            .game-panel {{
                flex: 1 !important;
                min-width: 400px !important;
                max-width: 600px !important;
            }}
            
            /* Responsive design - only stack on very small screens */
            @media (max-width: 900px) {{
                .game-panels {{
                    flex-direction: column !important;
                    gap: 1rem !important;
                }}
                
                .game-panel {{
                    min-width: 100% !important;
                    max-width: 100% !important;
                }}
                
                .text-6xl {{
                    font-size: 3rem !important;
                }}
                
                .text-5xl {{
                    font-size: 2.5rem !important;
                }}
                
                .text-4xl {{
                    font-size: 2rem !important;
                }}
                
                .text-3xl {{
                    font-size: 1.5rem !important;
                }}
                
                .text-2xl {{
                    font-size: 1.25rem !important;
                }}
            }}
            
            @media (max-width: 768px) {{
                .items-center {{
                    flex-direction: column;
                    align-items: center;
                }}
                
                .gap-6 {{
                    gap: 1rem !important;
                }}
                
                .mb-8 {{
                    margin-bottom: 2rem !important;
                }}
                
                .p-8 {{
                    padding: 1rem !important;
                }}
            }}
            
            /* Loading animation */
            .loading {{
                animation: loading 1.5s infinite;
            }}
            
            @keyframes loading {{
                0% {{
                    opacity: 1;
                }}
                50% {{
                    opacity: 0.5;
                }}
                100% {{
                    opacity: 1;
                }}
            }}
            
            /* Success/Error feedback */
            .feedback-success {{
                animation: bounce 0.6s ease-in-out;
                background: {GameTheme.SUCCESS} !important;
                color: white !important;
            }}
            
            .feedback-error {{
                animation: shake 0.5s ease-in-out;
                background: {GameTheme.ERROR} !important;
                color: white !important;
            }}
            
            /* Improved spacing */
            .game-container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 2rem;
            }}
            
            /* Enhanced shadows */
            .enhanced-shadow {{
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
            }}
            
            /* Smooth transitions */
            * {{
                transition: all 0.3s ease;
            }}
            
            /* Confetti animation */
            .confetti {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 9999;
            }}
            
            .confetti-piece {{
                position: absolute;
                width: 10px;
                height: 10px;
                background: #f0f;
                animation: confetti-fall 3s linear infinite;
            }}
            
            .confetti-piece:nth-child(1) {{
                left: 10%;
                background: #ff6b6b;
                animation-delay: 0s;
            }}
            
            .confetti-piece:nth-child(2) {{
                left: 20%;
                background: #4ecdc4;
                animation-delay: 0.1s;
            }}
            
            .confetti-piece:nth-child(3) {{
                left: 30%;
                background: #45b7d1;
                animation-delay: 0.2s;
            }}
            
            .confetti-piece:nth-child(4) {{
                left: 40%;
                background: #f9ca24;
                animation-delay: 0.3s;
            }}
            
            .confetti-piece:nth-child(5) {{
                left: 50%;
                background: #6c5ce7;
                animation-delay: 0.4s;
            }}
            
            .confetti-piece:nth-child(6) {{
                left: 60%;
                background: #a29bfe;
                animation-delay: 0.5s;
            }}
            
            .confetti-piece:nth-child(7) {{
                left: 70%;
                background: #fd79a8;
                animation-delay: 0.6s;
            }}
            
            .confetti-piece:nth-child(8) {{
                left: 80%;
                background: #00b894;
                animation-delay: 0.7s;
            }}
            
            .confetti-piece:nth-child(9) {{
                left: 90%;
                background: #e17055;
                animation-delay: 0.8s;
            }}
            
            .confetti-piece:nth-child(10) {{
                left: 15%;
                background: #ff7675;
                animation-delay: 0.9s;
            }}
            
            .confetti-piece:nth-child(11) {{
                left: 25%;
                background: #74b9ff;
                animation-delay: 1s;
            }}
            
            .confetti-piece:nth-child(12) {{
                left: 35%;
                background: #55a3ff;
                animation-delay: 1.1s;
            }}
            
            .confetti-piece:nth-child(13) {{
                left: 45%;
                background: #fd79a8;
                animation-delay: 1.2s;
            }}
            
            .confetti-piece:nth-child(14) {{
                left: 55%;
                background: #fdcb6e;
                animation-delay: 1.3s;
            }}
            
            .confetti-piece:nth-child(15) {{
                left: 65%;
                background: #6c5ce7;
                animation-delay: 1.4s;
            }}
            
            .confetti-piece:nth-child(16) {{
                left: 75%;
                background: #a29bfe;
                animation-delay: 1.5s;
            }}
            
            .confetti-piece:nth-child(17) {{
                left: 85%;
                background: #00cec9;
                animation-delay: 1.6s;
            }}
            
            .confetti-piece:nth-child(18) {{
                left: 95%;
                background: #e84393;
                animation-delay: 1.7s;
            }}
            
            .confetti-piece:nth-child(19) {{
                left: 5%;
                background: #00b894;
                animation-delay: 1.8s;
            }}
            
            .confetti-piece:nth-child(20) {{
                left: 95%;
                background: #e17055;
                animation-delay: 1.9s;
            }}
            
            @keyframes confetti-fall {{
                0% {{
                    transform: translateY(-100vh) rotate(0deg);
                    opacity: 1;
                }}
                100% {{
                    transform: translateY(100vh) rotate(360deg);
                    opacity: 0;
                }}
            }}
            
            /* Winner celebration styles */
            .winner-celebration {{
                animation: winner-bounce 1s ease-in-out;
                text-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
            }}
            
            @keyframes winner-bounce {{
                0%, 20%, 50%, 80%, 100% {{
                    transform: translateY(0) scale(1);
                }}
                40% {{
                    transform: translateY(-30px) scale(1.1);
                }}
                60% {{
                    transform: translateY(-15px) scale(1.05);
                }}
            }}
            
            .fireworks {{
                animation: fireworks 2s ease-out;
            }}
            
            @keyframes fireworks {{
                0% {{
                    transform: scale(0.5);
                    opacity: 0;
                }}
                50% {{
                    transform: scale(1.2);
                    opacity: 1;
                }}
                100% {{
                    transform: scale(1);
                    opacity: 1;
                }}
            }}
            
            /* Page container to ensure proper centering */
            .q-page {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 1rem;
            }}
        </style>
    ''')
    
    # Initialize game
    game_instance.initialize_game()


@ui.page('/')
def main_page():
    """Main game page"""
    create_main_page()


@ui.page('/statistics')
def statistics_page():
    """Statistics page"""
    ui.page_title('歇后语数据统计')
    
    # Create explorer instance
    explorer = XiehouyuExplorer()
    
    if not explorer.data:
        ui.label('无法加载数据').classes('text-2xl text-center')
        return
    
    # Page header
    ui.label('📊 歇后语数据统计').classes('text-4xl font-bold text-center mb-8 gradient-text')
    
    # Statistics cards
    stats = explorer.stats()
    
    with ui.row().classes('w-full gap-6 justify-center'):
        # Total count card
        with ui.card().style(GameTheme.PLAYER_PANEL_LEFT).classes('p-6'):
            ui.label('总数量').classes('text-lg font-semibold')
            ui.label(f'{stats["total_xiehouyu"]:,}').classes('text-4xl font-bold')
            ui.label('条歇后语').classes('text-sm opacity-80')
        
        # Unique riddles card
        with ui.card().style(GameTheme.PLAYER_PANEL_RIGHT).classes('p-6'):
            ui.label('独特谜面').classes('text-lg font-semibold')
            ui.label(f'{stats["unique_riddles"]:,}').classes('text-4xl font-bold')
            ui.label('个不同谜面').classes('text-sm opacity-80')
        
        # Unique answers card
        with ui.card().style(GameTheme.QUESTION_CARD).classes('p-6'):
            ui.label('独特答案').classes('text-lg font-semibold')
            ui.label(f'{stats["unique_answers"]:,}').classes('text-4xl font-bold text-primary')
            ui.label('个不同答案').classes('text-sm opacity-80')
    
    # Random samples
    ui.label('🎯 随机样例').classes('text-2xl font-bold mt-8 mb-4')
    
    samples = explorer.random_xiehouyu(5)
    for i, sample in enumerate(samples, 1):
        with ui.card().style(GameTheme.QUESTION_CARD).classes('mb-4'):
            ui.label(f'{i}. {sample["riddle"]}').classes('text-xl font-semibold')
            ui.label(f'答案: {sample["answer"]}').classes('text-lg text-gray-600 mt-2')
    
    # Back to game button
    ui.button('返回游戏', on_click=lambda: ui.navigate.to('/')).style(GameTheme.START_BUTTON).classes('mt-8')


@ui.page('/help')
def help_page():
    """Help page"""
    ui.page_title('游戏帮助')
    
    ui.label('🎮 游戏帮助').classes('text-4xl font-bold text-center mb-8 gradient-text')
    
    # Game rules
    with ui.card().style(GameTheme.QUESTION_CARD).classes('mb-6 p-6'):
        ui.label('游戏规则').classes('text-2xl font-bold mb-4')
        
        rules = [
            '1. 这是一个双人对战的歇后语游戏',
            '2. 每轮游戏中，两位玩家各自获得不同的歇后语题目',
            '3. 玩家需要从4个选项中选择正确的后半句',
            '4. 每个选项都会随机遮盖一个字，增加游戏难度',
            '5. 没有时间限制，玩家可以仔细思考',
            '6. 答对得分，答错不得分',
            '7. 游戏结束后得分高者获胜',
            '8. 连续答对可以获得连击记录'
        ]
        
        for rule in rules:
            ui.label(rule).classes('text-lg mb-2')
    
    # Scoring system
    with ui.card().style(GameTheme.QUESTION_CARD).classes('mb-6 p-6'):
        ui.label('计分系统').classes('text-2xl font-bold mb-4')
        
        scoring = [
            '• 基础分: 答对一题得1分',
            '• 难度奖励: 难题比简单题得分更高',
            '• 连击记录: 连续答对的题目数量',
            '• 答错: 不得分且连击中断'
        ]
        
        for score in scoring:
            ui.label(score).classes('text-lg mb-2')
    
    # Tips
    with ui.card().style(GameTheme.QUESTION_CARD).classes('mb-6 p-6'):
        ui.label('游戏技巧').classes('text-2xl font-bold mb-4')
        
        tips = [
            '💡 仔细理解歇后语的含义和语境',
            '🎯 根据遮盖的字推测完整答案',
            '🧠 多了解中国传统文化有助于理解歇后语',
            '📚 歇后语通常包含谐音、比喻等修辞手法',
            '🤔 没有时间压力，可以慢慢思考'
        ]
        
        for tip in tips:
            ui.label(tip).classes('text-lg mb-2')
    
    # Back to game button
    ui.button('返回游戏', on_click=lambda: ui.navigate.to('/')).style(GameTheme.START_BUTTON).classes('mt-8')


if __name__ == '__main__':
    # Run the application
    ui.run(
        title='歇后语对战游戏',
        favicon='🎯',
        port=8080,
        host='0.0.0.0',
        reload=False,
        show=True
    )