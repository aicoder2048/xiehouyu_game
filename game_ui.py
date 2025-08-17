#!/usr/bin/env python3
"""
UI Components Module for Chinese Xiehouyu Competition Game

Redesigned with two-column layout and integrated player panels.
"""

from nicegui import ui
from typing import Callable, Optional, List
from game_logic import GameState, PlayerSide, GamePhase, PlayerStats, QuestionData
import re


class GameTheme:
    """Theme configuration for child-friendly design"""
    
    # Primary colors - Blue-green gradient  
    PRIMARY_LIGHT = "#4ECDC4"
    PRIMARY_DARK = "#44A08D"
    
    # Secondary colors - Orange-yellow
    SECONDARY_LIGHT = "#FFB347"
    SECONDARY_DARK = "#FF8C42"
    
    # Neutral colors
    BACKGROUND = "#F8F9FA"
    CARD_BG = "#FFFFFF"
    TEXT_PRIMARY = "#2D3748"
    TEXT_SECONDARY = "#718096"
    
    # Status colors
    SUCCESS = "#48BB78"
    ERROR = "#F56565"
    WARNING = "#ED8936"
    
    # Masking box color
    MASK_COLOR = "#6B7280"
    
    # Component styles
    PLAYER_PANEL_LEFT = f"""
        background: linear-gradient(135deg, {PRIMARY_LIGHT} 0%, {PRIMARY_DARK} 100%);
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(78, 205, 196, 0.3);
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        padding: 1rem;
        min-height: 300px;
    """
    
    PLAYER_PANEL_RIGHT = f"""
        background: linear-gradient(135deg, {SECONDARY_LIGHT} 0%, {SECONDARY_DARK} 100%);
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(255, 179, 71, 0.3);
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        padding: 1rem;
        min-height: 300px;
    """
    
    QUESTION_CARD = """
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.8);
    """
    
    ANSWER_BUTTON = """
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 0.3rem;
        margin: 0.25rem 0;
        border: 2px solid rgba(255,255,255,0.6);
        color: #2D3748;
        font-weight: 500;
        font-size: 14px;
        transition: all 0.3s ease;
        cursor: pointer;
        min-height: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
    """
    
    ANSWER_BUTTON_HOVER = """
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        background: rgba(255, 255, 255, 1);
    """
    
    START_BUTTON = f"""
        background: linear-gradient(135deg, {SUCCESS} 0%, #38A169 100%);
        border-radius: 16px;
        padding: 1rem 3rem;
        font-size: 24px;
        font-weight: bold;
        color: white;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(72, 187, 120, 0.3);
    """


class MaskedAnswerButton:
    """Answer button with clickable masked characters"""
    
    def __init__(self, text: str, index: int, on_click: Callable[[int], None]):
        self.text = text
        self.index = index
        self.on_click = on_click
        self.mask_positions = self._get_mask_positions(text)
        self.revealed_positions = set()
        self.container = None
        self.button_element = None
        
        self._create_button()
    
    def _get_mask_positions(self, text: str) -> List[int]:
        """Get random positions to mask (Chinese characters only)"""
        chinese_positions = []
        for i, char in enumerate(text):
            if '\u4e00' <= char <= '\u9fff':  # Chinese character range
                chinese_positions.append(i)
        
        if chinese_positions:
            import random
            return [random.choice(chinese_positions)]
        return []
    
    def _create_button(self):
        """Create the masked answer button"""
        # Create the button with HTML content
        html_content = self._generate_html()
        
        with ui.column().classes('w-full') as self.container:
            self.button_element = ui.button(
                on_click=lambda: self.on_click(self.index)
            ).style(GameTheme.ANSWER_BUTTON).classes('w-full answer-btn')
            
            # Add HTML content to button
            with self.button_element:
                ui.html(html_content)
    
    def _generate_html(self) -> str:
        """Generate HTML with masked characters"""
        html_parts = []
        for i, char in enumerate(self.text):
            if i in self.mask_positions and i not in self.revealed_positions:
                # Create clickable masked box
                html_parts.append(f'''
                    <span class="masked-box" 
                          data-char="{char}" 
                          data-pos="{i}"
                          onclick="revealChar(this, {self.index}, {i})"
                          style="display: inline-block; width: 1.2em; height: 1.2em; 
                                 background: #6B7280; border-radius: 4px; 
                                 cursor: pointer; margin: 0 1px; vertical-align: middle;
                                 transition: all 0.3s ease;"
                          onmouseover="this.style.background='#9CA3AF'"
                          onmouseout="this.style.background='#6B7280'">
                    </span>
                ''')
            else:
                html_parts.append(char)
        
        return ''.join(html_parts)
    
    def reveal_character(self, position: int):
        """Reveal a masked character"""
        if position in self.mask_positions:
            self.revealed_positions.add(position)
            # Update the button HTML
            self.button_element.clear()
            with self.button_element:
                ui.html(self._generate_html())
    
    def set_style(self, style: str):
        """Set button style"""
        self.button_element.style(style)
    
    def disable(self):
        """Disable the button"""
        self.button_element.disable()
    
    def enable(self):
        """Enable the button"""
        self.button_element.enable()


class MaskedText:
    """Utility class for creating masked text with CSS boxes"""
    
    @staticmethod
    def create_masked_html(text: str, mask_positions: List[int]) -> str:
        """Create HTML with CSS masking boxes"""
        if not mask_positions:
            return text
            
        # Create spans with masking for specified positions
        html_parts = []
        for i, char in enumerate(text):
            if i in mask_positions:
                # Create a masked character
                html_parts.append(f'<span class="masked-char" data-char="{char}">&nbsp;</span>')
            else:
                html_parts.append(char)
        
        return ''.join(html_parts)
    
    @staticmethod
    def get_mask_positions(text: str) -> List[int]:
        """Get random positions to mask (Chinese characters only)"""
        chinese_positions = []
        for i, char in enumerate(text):
            if '\u4e00' <= char <= '\u9fff':  # Chinese character range
                chinese_positions.append(i)
        
        if chinese_positions:
            # Mask one random Chinese character
            import random
            return [random.choice(chinese_positions)]
        return []


class PlayerPanel:
    """Integrated player panel with question, answers, and stats"""
    
    def __init__(self, player_side: PlayerSide, on_answer_click: Callable[[int], None]):
        self.player_side = player_side
        self.on_answer_click = on_answer_click
        self.container = None
        self.score_label = None
        self.streak_label = None
        self.question_label = None
        self.answer_buttons = []
        self.status_label = None
        self.round_label = None
        self.player_name_input = None
        self.player_name_label = None
        self.player_name = "🐬 玩家一" if player_side == PlayerSide.LEFT else "🦊 玩家二"
        self.name_editing = False
        self.feedback_card = None
        self.feedback_label = None
        self.correct_answer_label = None
        self.score_details_label = None
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the integrated player panel"""
        panel_style = GameTheme.PLAYER_PANEL_LEFT if self.player_side == PlayerSide.LEFT else GameTheme.PLAYER_PANEL_RIGHT
        
        with ui.card().style(panel_style + '; min-height: auto; padding: 0.75rem;').classes('w-full rainbow-border') as self.container:
            # Player header - 减少间距
            with ui.row().classes('w-full items-center justify-between mb-2'):
                with ui.column().classes('items-start'):
                    # Editable player name with edit hint - 压缩尺寸
                    with ui.row().classes('items-center gap-1'):
                        self.player_name_label = ui.label(self.player_name).classes('text-xl font-bold cursor-pointer')
                        self.player_name_label.on('click', self._edit_name)
                        ui.label('✏️').classes('text-xs opacity-60')
                    
                    ui.label('点击编辑名称').classes('text-xs opacity-50')
                    
                    self.player_name_input = ui.input(
                        value=self.player_name,
                        placeholder='输入名称后按回车确认'
                    ).classes('text-xl font-bold').style('display: none;')
                    self.player_name_input.on('keydown.enter', self._save_name)
                    self.player_name_input.on('blur', self._save_name)
                    
                    self.status_label = ui.label('😊 等待开始...').classes('text-sm opacity-80')
                
                with ui.column().classes('items-center'):
                    self.score_label = ui.label('0').classes('text-2xl font-bold')
                    ui.label('🏆 得分').classes('text-xs opacity-80')
            
            # Streak and round info - 压缩尺寸
            with ui.row().classes('w-full items-center justify-between mb-1'):
                with ui.row().classes('items-center'):
                    ui.label('🔥').classes('text-sm mr-1')
                    self.streak_label = ui.label('连击: 0').classes('text-sm font-semibold')
                
                self.round_label = ui.label('🎯 第 1 轮').classes('text-sm font-semibold')
            
            # Question area - 压缩尺寸
            with ui.card().style(GameTheme.QUESTION_CARD + '; padding: 0.5rem; margin: 0.25rem 0;') as question_card:
                ui.label('📝 题目:').classes('text-md font-bold mb-1 text-gray-700')
                self.question_label = ui.label('等待题目...').classes('text-lg font-bold text-center text-gray-800 py-1')
            
            # Answer area - 2x2 grid layout
            ui.label('🎲 选择答案:').classes('text-lg font-bold mb-1 mt-1')
            
            # Answer buttons in 2x2 grid
            with ui.grid(columns=2).classes('w-full gap-2'):
                for i in range(4):
                    option_letter = ['A', 'B', 'C', 'D'][i]
                    btn = ui.button(
                        f'{option_letter}. 选项{i+1}',
                        on_click=lambda idx=i: self._handle_answer_click(idx)
                    ).style(GameTheme.ANSWER_BUTTON + '; height: 45px;').classes('w-full answer-btn text-sm')
                    self.answer_buttons.append(btn)
            
            # Feedback area for round results - 压缩紧凑显示
            with ui.card().style(GameTheme.QUESTION_CARD + '; display: none; padding: 0.5rem; margin: 0.25rem 0;') as self.feedback_card:
                ui.label('📋 本轮反馈:').classes('text-md font-bold mb-1 text-gray-700')
                self.correct_answer_label = ui.label('').classes('text-md font-semibold text-green-600 mb-1')
                self.score_details_label = ui.label('').classes('text-sm text-gray-700 mb-1')
                
                # Next round countdown info
                ui.label('⏰ 自动进入下一轮或点击右上角"下一轮"按钮').classes('text-xs text-gray-500')
    
    def _edit_name(self):
        """Switch to name editing mode"""
        if not self.name_editing:
            self.name_editing = True
            self.player_name_label.style('display: none;')
            self.player_name_input.style('display: block;')
            self.player_name_input.value = self.player_name
    
    def _save_name(self, e=None):
        """Save the edited name"""
        if self.name_editing:
            new_name = self.player_name_input.value.strip()
            self.player_name = new_name if new_name else self.player_name
            self.name_editing = False
            self.player_name_label.text = self.player_name
            self.player_name_label.style('display: block;')
            self.player_name_input.style('display: none;')
    
    def _handle_answer_click(self, index: int):
        """Handle answer button click"""
        # Disable all buttons to prevent multiple clicks
        for btn in self.answer_buttons:
            btn.disable()
        
        # Call the callback
        self.on_answer_click(index)
    
    def update_stats(self, stats: PlayerStats, round_num: int):
        """Update player statistics and round info"""
        self.score_label.text = str(stats.score)
        self.streak_label.text = f'连击: {stats.current_streak}'
        self.round_label.text = f'🎯 第 {round_num} 轮'
        
        # Update streak color and emoji
        if stats.current_streak >= 3:
            self.streak_label.text = f'🔥 连击: {stats.current_streak} 🔥'
            self.streak_label.classes('text-yellow-200')
        elif stats.current_streak >= 1:
            self.streak_label.text = f'⚡ 连击: {stats.current_streak}'
            self.streak_label.classes('text-orange-200')
        else:
            self.streak_label.text = f'连击: {stats.current_streak}'
            self.streak_label.classes('text-gray-200')
    
    def update_question(self, question: QuestionData):
        """Update question display"""
        self.question_label.text = question.riddle
        
        # IMPORTANT: Reset all answer button styles first
        self.reset_answer_styles()
        
        # Update answer buttons with full text and A/B/C/D labels
        for i, choice in enumerate(question.choices):
            if i < len(self.answer_buttons):
                option_letter = ['A', 'B', 'C', 'D'][i]
                # Use the full answer text with letter prefix
                self.answer_buttons[i].text = f'{option_letter}. {choice}'
                # Ensure each button has clean styling with height
                self.answer_buttons[i].style(GameTheme.ANSWER_BUTTON + '; height: 45px;')
    
    def disable_answers(self):
        """Disable all answer buttons"""
        for btn in self.answer_buttons:
            btn.disable()
    
    def enable_answers(self):
        """Enable all answer buttons"""
        for btn in self.answer_buttons:
            btn.enable()
    
    def highlight_correct_answer(self, correct_index: int, selected_index: int):
        """Highlight the correct answer and user's selection"""
        for i, btn in enumerate(self.answer_buttons):
            if i == correct_index:
                # Highlight correct answer in green
                btn.style(f'{GameTheme.ANSWER_BUTTON}; background: {GameTheme.SUCCESS}; color: white;')
            elif i == selected_index and i != correct_index:
                # Highlight wrong selection in red
                btn.style(f'{GameTheme.ANSWER_BUTTON}; background: {GameTheme.ERROR}; color: white;')
            else:
                # Keep normal style for other options
                btn.style(f'{GameTheme.ANSWER_BUTTON}; opacity: 0.6;')
    
    def reset_answer_styles(self):
        """Reset answer button styles - comprehensive reset"""
        for btn in self.answer_buttons:
            # Force complete style reset with explicit overrides
            btn.style(f'{GameTheme.ANSWER_BUTTON}; opacity: 1 !important; background: rgba(255, 255, 255, 0.9) !important; color: #2D3748 !important;')
            # Also enable the button to ensure it's interactive
            btn.enable()
    
    def update_status(self, status: str):
        """Update player status"""
        self.status_label.text = status
    
    def show_round_feedback(self, correct_answer: str, score_details: str):
        """Show round feedback with correct answer and score details"""
        self.correct_answer_label.text = f'✅ 正确答案: {correct_answer}'
        self.score_details_label.text = score_details
        self.feedback_card.style(GameTheme.QUESTION_CARD + '; display: block;')
    
    def hide_round_feedback(self):
        """Hide round feedback"""
        self.feedback_card.style(GameTheme.QUESTION_CARD + '; display: none;')


class GameHeader:
    """Game header with title and controls"""
    
    def __init__(self, on_start_game: Callable[[], None], on_reset_game: Callable[[], None]):
        self.container = None
        self.start_button = None
        self.rounds_select = None
        self.global_next_round_button = None
        self.on_start_game = on_start_game
        self.on_reset_game = on_reset_game
        self.on_global_next_round = None  # 将由GameUI设置
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the game header"""
        with ui.column().classes('w-full items-center mb-4') as self.container:
            # Game title
            ui.label('🌈 歇后语大挑战 🎯').classes('text-4xl font-bold text-center mb-3 gradient-text')
            
            # Control row - 左对齐游戏控制，右对齐下一轮按钮
            with ui.row().classes('w-full items-center justify-between'):
                # Left side - Game controls
                with ui.row().classes('items-center gap-4'):
                    # Rounds selector
                    ui.label('🎲 游戏轮数:').classes('text-lg font-semibold')
                    self.rounds_select = ui.select(
                        options={1: '1轮 🚀', 3: '3轮 ⭐', 6: '6轮 ⚡', 12: '12轮 🔥', 18: '18轮 💪'},
                        value=12
                    ).classes('text-md')
                    
                    # Start button
                    self.start_button = ui.button(
                        '🚀 开始',
                        on_click=self.on_start_game
                    ).style(GameTheme.START_BUTTON).classes('start-btn')
                    
                    # Reset button
                    ui.button(
                        '🔄 重置',
                        on_click=self.on_reset_game
                    ).style(GameTheme.START_BUTTON.replace(GameTheme.SUCCESS, GameTheme.WARNING)).classes('reset-btn')
                    
                    # Navigation buttons
                    ui.button(
                        '📚 探索',
                        on_click=lambda: ui.navigate.to('/explorer')
                    ).style(GameTheme.START_BUTTON.replace(GameTheme.SUCCESS, '#3B82F6')).classes('nav-btn')
                
                # Right side - Next round button (initially hidden)
                self.global_next_round_button = ui.button(
                    '▶️ 下一轮',
                    on_click=lambda: self.on_global_next_round() if self.on_global_next_round else None
                ).style(GameTheme.START_BUTTON + '; display: none;').classes('next-round-btn')
    
    def update_button_state(self, game_phase: GamePhase):
        """Update button states based on game phase"""
        if game_phase == GamePhase.SETUP:
            self.start_button.text = '🚀 开始'
            self.start_button.enable()
            self.rounds_select.enable()
        elif game_phase in [GamePhase.PLAYING, GamePhase.WAITING, GamePhase.ROUND_FEEDBACK]:
            self.start_button.text = '🎮 游戏中...'
            self.start_button.disable()
            self.rounds_select.disable()
        elif game_phase == GamePhase.FINISHED:
            self.start_button.text = '🔄 重新开始'
            self.start_button.enable()
            self.rounds_select.enable()
            self.hide_global_next_round_button()
    
    def show_global_next_round_button(self, text: str = '▶️ 下一轮'):
        """显示全局下一轮按钮"""
        if self.global_next_round_button:
            self.global_next_round_button.text = text
            self.global_next_round_button.style(GameTheme.START_BUTTON + '; display: inline-block;')
    
    def hide_global_next_round_button(self):
        """隐藏全局下一轮按钮"""
        if self.global_next_round_button:
            self.global_next_round_button.style(GameTheme.START_BUTTON + '; display: none;')
    
    def set_global_next_round_callback(self, callback: Callable[[], None]):
        """设置全局下一轮按钮的回调函数"""
        self.on_global_next_round = callback


class GameOverDialog:
    """Game over dialog with final results"""
    
    def __init__(self, on_new_game: Callable[[], None]):
        self.dialog = None
        self.on_new_game = on_new_game
    
    def show(self, winner: Optional[PlayerSide], left_stats: PlayerStats, right_stats: PlayerStats, config, left_name: str = "🐬 玩家一", right_name: str = "🦊 玩家二"):
        """Show game over dialog"""
        print(f"DEBUG: GameOverDialog.show called with winner={winner}")  # Debug log
        with ui.dialog().classes('max-w-6xl w-full') as self.dialog:
            with ui.card().classes('p-8 fireworks'):
                # Confetti animation
                confetti_html = '''
                <div class="confetti">
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                    <div class="confetti-piece"></div>
                </div>
                '''
                ui.html(confetti_html)
                
                # Winner announcement with celebration
                if winner == PlayerSide.LEFT:
                    ui.label(f'🎉🏆 {left_name} 获胜！🏆🎉').classes('text-4xl font-bold text-center text-teal-500 mb-4 winner-celebration whitespace-nowrap')
                    ui.label('恭喜！你是歇后语大师！').classes('text-2xl text-center text-teal-400 mb-6')
                elif winner == PlayerSide.RIGHT:
                    ui.label(f'🎉🏆 {right_name} 获胜！🏆🎉').classes('text-4xl font-bold text-center text-orange-500 mb-4 winner-celebration whitespace-nowrap')
                    ui.label('恭喜！你是歇后语大师！').classes('text-2xl text-center text-orange-400 mb-6')
                else:
                    ui.label('🤝✨ 平局！✨🤝').classes('text-4xl font-bold text-center text-gray-500 mb-4 winner-celebration whitespace-nowrap')
                    ui.label('双方势均力敌，都是歇后语高手！').classes('text-xl text-center text-gray-400 mb-6')
                
                # Final statistics
                with ui.row().classes('w-full justify-around mb-8'):
                    # Left player stats
                    with ui.card().style(GameTheme.PLAYER_PANEL_LEFT).classes('p-6'):
                        ui.label(left_name).classes('text-2xl font-bold text-center mb-4')
                        ui.label(str(left_stats.score)).classes('text-4xl font-bold text-center')
                        ui.label('总分').classes('text-lg text-center opacity-80')
                        ui.separator()
                        
                        # 详细得分分解
                        left_breakdown = left_stats.get_score_breakdown(config)
                        ui.label('📊 得分详情').classes('text-lg font-bold mt-4 mb-2')
                        ui.label(f'正确答题得分: {left_breakdown["base_count"]} × {left_breakdown["base_points"]} = {left_breakdown["base_score"]}分').classes('text-sm')
                        ui.label(f'优先答题得分: {left_breakdown["priority_count"]} × {left_breakdown["priority_points"]} = {left_breakdown["priority_score"]}分').classes('text-sm')
                        
                        if left_breakdown["streak_bonuses"]:
                            streak_detail = " + ".join(map(str, left_breakdown["streak_bonuses"]))
                            ui.label(f'连击得分: {streak_detail} = {left_breakdown["streak_total"]}分').classes('text-sm')
                        else:
                            ui.label(f'连击得分: 0分').classes('text-sm')
                            
                        ui.separator().classes('my-2')
                        ui.label(f'最高连击: {left_stats.max_streak}').classes('text-sm')
                    
                    # Right player stats
                    with ui.card().style(GameTheme.PLAYER_PANEL_RIGHT).classes('p-6'):
                        ui.label(right_name).classes('text-2xl font-bold text-center mb-4')
                        ui.label(str(right_stats.score)).classes('text-4xl font-bold text-center')
                        ui.label('总分').classes('text-lg text-center opacity-80')
                        ui.separator()
                        
                        # 详细得分分解
                        right_breakdown = right_stats.get_score_breakdown(config)
                        ui.label('📊 得分详情').classes('text-lg font-bold mt-4 mb-2')
                        ui.label(f'正确答题得分: {right_breakdown["base_count"]} × {right_breakdown["base_points"]} = {right_breakdown["base_score"]}分').classes('text-sm')
                        ui.label(f'优先答题得分: {right_breakdown["priority_count"]} × {right_breakdown["priority_points"]} = {right_breakdown["priority_score"]}分').classes('text-sm')
                        
                        if right_breakdown["streak_bonuses"]:
                            streak_detail = " + ".join(map(str, right_breakdown["streak_bonuses"]))
                            ui.label(f'连击得分: {streak_detail} = {right_breakdown["streak_total"]}分').classes('text-sm')
                        else:
                            ui.label(f'连击得分: 0分').classes('text-sm')
                            
                        ui.separator().classes('my-2')
                        ui.label(f'最高连击: {right_stats.max_streak}').classes('text-sm')
                
                # Action buttons
                with ui.row().classes('w-full justify-center gap-6'):
                    ui.button(
                        '再来一局',
                        on_click=self._new_game
                    ).style(GameTheme.START_BUTTON).classes('text-xl px-8 py-4')
                    
                    ui.button(
                        '结束游戏',
                        on_click=self.dialog.close
                    ).style(GameTheme.START_BUTTON.replace(GameTheme.SUCCESS, GameTheme.WARNING)).classes('text-xl px-8 py-4')
        
        print(f"DEBUG: Opening game over dialog")  # Debug log
        self.dialog.open()
        print(f"DEBUG: Game over dialog opened")  # Debug log
    
    def _new_game(self):
        """Start new game"""
        self.dialog.close()
        self.on_new_game()


class GameUI:
    """Main game UI coordinator"""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.game_header = None
        self.player_panels = {}
        self.game_over_dialog = None
        self.countdown_timer = None
        self.countdown_seconds = 0
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the main game UI"""
        # Game header
        self.game_header = GameHeader(
            self._on_start_game,
            self._on_reset_game
        )
        
        # Main game area - two columns side by side
        with ui.row().classes('game-panels mt-4'):
            # Left player panel
            with ui.column().classes('game-panel'):
                self.player_panels[PlayerSide.LEFT] = PlayerPanel(
                    PlayerSide.LEFT,
                    lambda idx: self._on_answer_click(PlayerSide.LEFT, idx)
                )
            
            # Right player panel
            with ui.column().classes('game-panel'):
                self.player_panels[PlayerSide.RIGHT] = PlayerPanel(
                    PlayerSide.RIGHT,
                    lambda idx: self._on_answer_click(PlayerSide.RIGHT, idx)
                )
        
        # Game over dialog
        self.game_over_dialog = GameOverDialog(self._on_new_game)
        
        # Set up global next round button callback
        self.game_header.set_global_next_round_callback(self._on_next_round)
    
    def _on_answer_click(self, player: PlayerSide, answer_index: int):
        """Handle answer click from player"""
        # Check if this will be the final answer and store other player's info before submitting
        other_player = PlayerSide.RIGHT if player == PlayerSide.LEFT else PlayerSide.LEFT
        will_be_both_answered = self.game_state.player_answers[other_player] is not None
        other_player_answer = self.game_state.player_answers[other_player] if will_be_both_answered else None
        other_player_question = self.game_state.get_player_question(other_player) if will_be_both_answered else None
        
        success = self.game_state.submit_answer(player, answer_index)
        if success:
            # Show answer feedback only for the player who answered
            panel = self.player_panels[player]
            question = self.game_state.get_player_question(player)
            if question:
                panel.highlight_correct_answer(question.correct_index, answer_index)
                
                # Update status
                if answer_index == question.correct_index:
                    panel.update_status('✨ 太棒了！答对了！')
                else:
                    panel.update_status('💫 再想想！答错了！')
            
            # 立即更新当前玩家的分数显示
            panel.update_stats(self.game_state.player_stats[player], self.game_state.current_round)
            
            # If both players had answered (checked before state was reset)
            if will_be_both_answered and other_player_answer is not None and other_player_question:
                # Show results for the other player too
                other_panel = self.player_panels[other_player]
                other_panel.highlight_correct_answer(other_player_question.correct_index, other_player_answer)
                
                # Update status for other player
                if other_player_answer == other_player_question.correct_index:
                    other_panel.update_status('✨ 太棒了！答对了！')
                else:
                    other_panel.update_status('💫 再想想！答错了！')
                
                # 立即更新另一个玩家的分数显示
                other_panel.update_stats(self.game_state.player_stats[other_player], self.game_state.current_round)
            
            # Always update UI after any answer submission
            self._update_ui()
    
    def _on_start_game(self):
        """Handle start game button click"""
        print(f"DEBUG: Starting new game with {self.game_header.rounds_select.value} rounds")  # Debug log
        self.game_state.config.total_rounds = self.game_header.rounds_select.value
        self.game_state.start_game()
        self._update_ui()
    
    def _on_reset_game(self):
        """Handle reset game button click"""
        print(f"DEBUG: Resetting game")  # Debug log
        self.game_state.phase = GamePhase.SETUP
        self.game_state.current_round = 0
        
        # Reset player stats
        for player in self.game_state.player_stats:
            self.game_state.player_stats[player] = PlayerStats()
        
        # Reset player names to defaults
        print(f"DEBUG: Resetting player names")  # Debug log
        self.player_panels[PlayerSide.LEFT].player_name = "🐬 玩家一"
        self.player_panels[PlayerSide.LEFT].player_name_label.text = "🐬 玩家一"
        self.player_panels[PlayerSide.LEFT].player_name_input.value = "🐬 玩家一"
        
        self.player_panels[PlayerSide.RIGHT].player_name = "🦊 玩家二"
        self.player_panels[PlayerSide.RIGHT].player_name_label.text = "🦊 玩家二"
        self.player_panels[PlayerSide.RIGHT].player_name_input.value = "🦊 玩家二"
        
        # Reset rounds selector to default
        print(f"DEBUG: Resetting rounds selector to 12")  # Debug log
        self.game_header.rounds_select.value = 12
        
        # Force UI refresh
        self.game_header.rounds_select.update()
        
        self._update_ui()
    
    def _start_new_game(self):
        """Start a new game preserving player names and settings"""
        print(f"DEBUG: Starting new game preserving player names")  # Debug log
        self.game_state.phase = GamePhase.SETUP
        self.game_state.current_round = 0
        
        # Reset only game stats, preserve player names
        for player in self.game_state.player_stats:
            self.game_state.player_stats[player] = PlayerStats()
        
        # Do NOT reset player names or rounds selector
        self._update_ui()
    
    def _on_new_game(self):
        """Handle new game from dialog"""
        self._start_new_game()
    
    def _on_next_round(self):
        """Handle next round button click"""
        if self.countdown_timer:
            self.countdown_timer.cancel()
            self.countdown_timer = None
        self.game_state.continue_to_next_round()
        self._update_ui()
    
    def _start_countdown(self, countdown_seconds: int = None):
        """Start countdown for next round with dynamic timing based on round results"""
        if countdown_seconds is None:
            # 动态计算倒计时时间
            left_stats = self.game_state.player_stats[PlayerSide.LEFT]
            right_stats = self.game_state.player_stats[PlayerSide.RIGHT]
            
            # 检查本轮是否有人答错
            left_answered_wrong = left_stats.last_round_score == 0
            right_answered_wrong = right_stats.last_round_score == 0
            
            if left_answered_wrong or right_answered_wrong:
                # 有人答错，给更多时间反思：9秒
                countdown_seconds = 9
                print(f"DEBUG: 有玩家答错，倒计时设为{countdown_seconds}秒")
            else:
                # 都答对了，快速进入下一轮：3秒
                countdown_seconds = 3
                print(f"DEBUG: 两人都答对，倒计时设为{countdown_seconds}秒")
        
        self.countdown_seconds = countdown_seconds
        
        def update_countdown():
            if self.countdown_seconds > 0:
                # Update global button text with countdown
                countdown_text = f'⏰ {self.countdown_seconds}秒后下一轮'
                self.game_header.show_global_next_round_button(countdown_text)
                self.countdown_seconds -= 1
            elif self.countdown_seconds <= 0:
                # Auto-advance to next round
                if self.game_state.phase == GamePhase.ROUND_FEEDBACK:
                    if self.countdown_timer:
                        self.countdown_timer.cancel()
                        self.countdown_timer = None
                    self.game_state.continue_to_next_round()
                    self._update_ui()
        
        # Use NiceGUI timer instead of asyncio task
        self.countdown_timer = ui.timer(1.0, update_countdown)
    
    def _show_round_feedback(self):
        """Show round feedback for both players"""
        # Show feedback for both players
        for player in [PlayerSide.LEFT, PlayerSide.RIGHT]:
            panel = self.player_panels[player]
            question = self.game_state.get_player_question(player)
            stats = self.game_state.player_stats[player]
            
            if question:
                panel.show_round_feedback(
                    question.correct_answer,
                    stats.last_round_details
                )
                
                # Update status based on answer
                answer_index = self.game_state.player_answers[player]
                if answer_index == question.correct_index:
                    panel.update_status('✨ 太棒了！答对了！')
                else:
                    panel.update_status('💫 再想想！答错了！')
                
                # Highlight correct answer
                panel.highlight_correct_answer(question.correct_index, answer_index)
        
        # Show global next round button and start countdown
        self.game_header.show_global_next_round_button('▶️ 下一轮')
        self._start_countdown()
    
    def _update_ui(self):
        """Update all UI components"""
        # Update game header
        self.game_header.update_button_state(self.game_state.phase)
        
        # Handle round feedback phase
        if self.game_state.phase == GamePhase.ROUND_FEEDBACK:
            self._show_round_feedback()
            return
        else:
            # Hide feedback and next round button when not in feedback phase
            for player in [PlayerSide.LEFT, PlayerSide.RIGHT]:
                self.player_panels[player].hide_round_feedback()
            self.game_header.hide_global_next_round_button()
            if self.countdown_timer:
                self.countdown_timer.cancel()
                self.countdown_timer = None
        
        # CRITICAL: Force reset all answer styles first if in new round
        if self.game_state.phase == GamePhase.WAITING:
            print(f"DEBUG: Force resetting all answer styles for new round")
            for player in [PlayerSide.LEFT, PlayerSide.RIGHT]:
                self.player_panels[player].reset_answer_styles()
        
        # Update player panels
        for player in [PlayerSide.LEFT, PlayerSide.RIGHT]:
            panel = self.player_panels[player]
            stats = self.game_state.player_stats[player]
            
            # Update stats
            panel.update_stats(stats, self.game_state.current_round)
            
            # Update question and answers
            question = self.game_state.get_player_question(player)
            if question and self.game_state.phase == GamePhase.WAITING:
                # CRITICAL: Reset answer styles FIRST before updating question
                panel.reset_answer_styles()
                panel.update_question(question)
                # Force enable all buttons and reset styles again to ensure clean state
                panel.enable_answers()
                panel.reset_answer_styles()
                
                # Only then check if player should be disabled
                if self.game_state.player_answers[player] is not None:
                    panel.disable_answers()
                    # Get the answer text the player chose
                    answer_index = self.game_state.player_answers[player]
                    if question and answer_index is not None and 0 <= answer_index < len(question.choices):
                        chosen_answer = question.choices[answer_index]
                        panel.update_status(f'你已回答（{chosen_answer}），等待对方回答后进入下一轮')
                    else:
                        panel.update_status('你已回答，等待对方回答后进入下一轮')
                else:
                    panel.update_status('🤔 请选择答案')
            else:
                panel.disable_answers()
                if self.game_state.phase == GamePhase.SETUP:
                    panel.update_status('😊 等待游戏开始')
                    # Reset answer styles when in setup
                    panel.reset_answer_styles()
                elif self.game_state.phase == GamePhase.PLAYING:
                    panel.update_status('⏳ 准备下一轮...')
                    # Reset answer styles when starting new round
                    panel.reset_answer_styles()
                elif self.game_state.phase == GamePhase.ROUND_FEEDBACK:
                    panel.update_status('📋 查看本轮结果...')
                elif self.game_state.phase == GamePhase.FINISHED:
                    panel.update_status('🎉 游戏结束')
        
        # Show game over dialog if finished
        if self.game_state.phase == GamePhase.FINISHED:
            print(f"DEBUG: Game finished, showing dialog")  # Debug log
            winner = self.game_state.get_winner()
            left_name = self.player_panels[PlayerSide.LEFT].player_name
            right_name = self.player_panels[PlayerSide.RIGHT].player_name
            print(f"DEBUG: Winner: {winner}, Left: {left_name}, Right: {right_name}")  # Debug log
            self.game_over_dialog.show(
                winner,
                self.game_state.player_stats[PlayerSide.LEFT],
                self.game_state.player_stats[PlayerSide.RIGHT],
                self.game_state.config,
                left_name,
                right_name
            )
    
