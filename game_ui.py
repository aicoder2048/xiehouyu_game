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
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the integrated player panel"""
        panel_style = GameTheme.PLAYER_PANEL_LEFT if self.player_side == PlayerSide.LEFT else GameTheme.PLAYER_PANEL_RIGHT
        
        with ui.card().style(panel_style).classes('w-full rainbow-border') as self.container:
            # Player header
            with ui.row().classes('w-full items-center justify-between mb-3'):
                with ui.column().classes('items-start'):
                    # Editable player name with edit hint
                    with ui.row().classes('items-center gap-2'):
                        self.player_name_label = ui.label(self.player_name).classes('text-2xl font-bold cursor-pointer')
                        self.player_name_label.on('click', self._edit_name)
                        ui.label('✏️').classes('text-sm opacity-60')
                    
                    ui.label('点击编辑名称').classes('text-xs opacity-50')
                    
                    self.player_name_input = ui.input(
                        value=self.player_name,
                        placeholder='输入名称后按回车确认'
                    ).classes('text-2xl font-bold').style('display: none;')
                    self.player_name_input.on('keydown.enter', self._save_name)
                    self.player_name_input.on('blur', self._save_name)
                    
                    self.status_label = ui.label('😊 等待开始...').classes('text-sm opacity-80')
                
                with ui.column().classes('items-center'):
                    self.score_label = ui.label('0').classes('text-3xl font-bold')
                    ui.label('🏆 得分').classes('text-sm opacity-80')
            
            # Streak and round info
            with ui.row().classes('w-full items-center justify-between mb-2'):
                with ui.row().classes('items-center'):
                    ui.label('🔥').classes('text-lg mr-1')
                    self.streak_label = ui.label('连击: 0').classes('text-lg font-semibold')
                
                self.round_label = ui.label('🎯 第 1 轮').classes('text-lg font-semibold')
            
            # Question area
            with ui.card().style(GameTheme.QUESTION_CARD) as question_card:
                ui.label('📝 题目:').classes('text-lg font-bold mb-2 text-gray-700')
                self.question_label = ui.label('等待题目...').classes('text-xl font-bold text-center text-gray-800 p-2')
            
            # Answer area
            ui.label('🎲 选择答案:').classes('text-lg font-bold mb-2 mt-2')
            
            # Answer buttons (will be replaced with MaskedAnswerButton)
            for i in range(4):
                btn = ui.button(
                    f'选项 {i+1}',
                    on_click=lambda idx=i: self._handle_answer_click(idx)
                ).style(GameTheme.ANSWER_BUTTON).classes('w-full answer-btn')
                self.answer_buttons.append(btn)
    
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
        
        # Update answer buttons with full text (no masking)
        for i, choice in enumerate(question.choices):
            if i < len(self.answer_buttons):
                # Use the full answer text without masking
                self.answer_buttons[i].text = choice
    
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
        """Reset answer button styles"""
        for btn in self.answer_buttons:
            btn.style(GameTheme.ANSWER_BUTTON)
    
    def update_status(self, status: str):
        """Update player status"""
        self.status_label.text = status


class GameHeader:
    """Game header with title and controls"""
    
    def __init__(self, on_start_game: Callable[[], None], on_reset_game: Callable[[], None]):
        self.container = None
        self.start_button = None
        self.rounds_select = None
        self.on_start_game = on_start_game
        self.on_reset_game = on_reset_game
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the game header"""
        with ui.column().classes('w-full items-center mb-4') as self.container:
            # Game title
            ui.label('🌈 歇后语大挑战 🎯').classes('text-4xl font-bold text-center mb-3 gradient-text')
            
            # Control row
            with ui.row().classes('items-center gap-4'):
                # Rounds selector
                ui.label('🎲 游戏轮数:').classes('text-lg font-semibold')
                self.rounds_select = ui.select(
                    options={1: '1轮 🚀', 3: '3轮 ⭐', 6: '6轮 ⚡', 12: '12轮 🔥', 18: '18轮 💪'},
                    value=12
                ).classes('text-md')
                
                # Start button
                self.start_button = ui.button(
                    '🚀 开始游戏',
                    on_click=self.on_start_game
                ).style(GameTheme.START_BUTTON).classes('start-btn')
                
                # Reset button
                ui.button(
                    '🔄 重置游戏',
                    on_click=self.on_reset_game
                ).style(GameTheme.START_BUTTON.replace(GameTheme.SUCCESS, GameTheme.WARNING)).classes('reset-btn')
    
    def update_button_state(self, game_phase: GamePhase):
        """Update button states based on game phase"""
        if game_phase == GamePhase.SETUP:
            self.start_button.text = '🚀 开始游戏'
            self.start_button.enable()
            self.rounds_select.enable()
        elif game_phase == GamePhase.PLAYING or game_phase == GamePhase.WAITING:
            self.start_button.text = '🎮 游戏中...'
            self.start_button.disable()
            self.rounds_select.disable()
        elif game_phase == GamePhase.FINISHED:
            self.start_button.text = '🔄 重新开始'
            self.start_button.enable()
            self.rounds_select.enable()


class GameOverDialog:
    """Game over dialog with final results"""
    
    def __init__(self, on_new_game: Callable[[], None]):
        self.dialog = None
        self.on_new_game = on_new_game
    
    def show(self, winner: Optional[PlayerSide], left_stats: PlayerStats, right_stats: PlayerStats, left_name: str = "🐬 玩家一", right_name: str = "🦊 玩家二"):
        """Show game over dialog"""
        print(f"DEBUG: GameOverDialog.show called with winner={winner}")  # Debug log
        with ui.dialog().classes('w-120') as self.dialog:
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
                    ui.label(f'🎉🏆 {left_name} 获胜！🏆🎉').classes('text-5xl font-bold text-center text-teal-500 mb-4 winner-celebration')
                    ui.label('恭喜！你是歇后语大师！').classes('text-2xl text-center text-teal-400 mb-6')
                elif winner == PlayerSide.RIGHT:
                    ui.label(f'🎉🏆 {right_name} 获胜！🏆🎉').classes('text-5xl font-bold text-center text-orange-500 mb-4 winner-celebration')
                    ui.label('恭喜！你是歇后语大师！').classes('text-2xl text-center text-orange-400 mb-6')
                else:
                    ui.label('🤝✨ 平局！✨🤝').classes('text-4xl font-bold text-center text-gray-500 mb-4 winner-celebration')
                    ui.label('双方势均力敌，都是歇后语高手！').classes('text-xl text-center text-gray-400 mb-6')
                
                # Final statistics
                with ui.row().classes('w-full justify-around mb-8'):
                    # Left player stats
                    with ui.card().style(GameTheme.PLAYER_PANEL_LEFT).classes('p-6'):
                        ui.label(left_name).classes('text-2xl font-bold text-center mb-4')
                        ui.label(str(left_stats.score)).classes('text-4xl font-bold text-center')
                        ui.label('总分').classes('text-lg text-center opacity-80')
                        ui.separator()
                        ui.label(f'答对: {left_stats.correct_answers}').classes('text-lg mt-2')
                        ui.label(f'答错: {left_stats.wrong_answers}').classes('text-lg')
                        ui.label(f'最高连击: {left_stats.max_streak}').classes('text-lg')
                    
                    # Right player stats
                    with ui.card().style(GameTheme.PLAYER_PANEL_RIGHT).classes('p-6'):
                        ui.label(right_name).classes('text-2xl font-bold text-center mb-4')
                        ui.label(str(right_stats.score)).classes('text-4xl font-bold text-center')
                        ui.label('总分').classes('text-lg text-center opacity-80')
                        ui.separator()
                        ui.label(f'答对: {right_stats.correct_answers}').classes('text-lg mt-2')
                        ui.label(f'答错: {right_stats.wrong_answers}').classes('text-lg')
                        ui.label(f'最高连击: {right_stats.max_streak}').classes('text-lg')
                
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
    
    def _on_new_game(self):
        """Handle new game from dialog"""
        self._on_reset_game()
    
    def _update_ui(self):
        """Update all UI components"""
        # Update game header
        self.game_header.update_button_state(self.game_state.phase)
        
        # Update player panels
        for player in [PlayerSide.LEFT, PlayerSide.RIGHT]:
            panel = self.player_panels[player]
            stats = self.game_state.player_stats[player]
            
            # Update stats
            panel.update_stats(stats, self.game_state.current_round)
            
            # Update question and answers
            question = self.game_state.get_player_question(player)
            if question and self.game_state.phase == GamePhase.WAITING:
                panel.update_question(question)
                # Only enable answers if player hasn't answered yet
                if self.game_state.player_answers[player] is None:
                    panel.enable_answers()
                    panel.update_status('🤔 请选择答案')
                    panel.reset_answer_styles()
                else:
                    panel.disable_answers()
                    panel.update_status('⏳ 等待对方回答...')
            else:
                panel.disable_answers()
                if self.game_state.phase == GamePhase.SETUP:
                    panel.update_status('😊 等待游戏开始')
                elif self.game_state.phase == GamePhase.PLAYING:
                    panel.update_status('⏳ 准备下一轮...')
                    # Reset answer styles when starting new round
                    panel.reset_answer_styles()
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
                left_name,
                right_name
            )
    
