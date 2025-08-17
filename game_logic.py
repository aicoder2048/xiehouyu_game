#!/usr/bin/env python3
"""
Game Logic Module for Chinese Xiehouyu Competition Game

This module handles all the core game logic including:
- Game state management
- Answer generation with masking
- Scoring and timing
- Round progression
"""

import json
import random
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class GamePhase(Enum):
    """Game phases"""
    SETUP = "setup"
    PLAYING = "playing"
    WAITING = "waiting"
    ROUND_FEEDBACK = "round_feedback"  # 显示本轮反馈的阶段
    FINISHED = "finished"


class PlayerSide(Enum):
    """Player sides"""
    LEFT = "left"
    RIGHT = "right"


@dataclass
class GameConfig:
    """Game configuration"""
    total_rounds: int = 12
    points_per_correct: int = 2  # 回答正确的基础得分
    bonus_for_correct: int = 1  # 回答正确的额外奖励分数


@dataclass
class PlayerStats:
    """Player statistics"""
    score: int = 0
    correct_answers: int = 0
    wrong_answers: int = 0
    current_streak: int = 0
    max_streak: int = 0
    last_round_score: int = 0  # 上一轮获得的分数
    last_round_details: str = ""  # 上一轮得分详情
    
    def add_correct_answer(self, points_earned: int, details: str):
        """Add a correct answer with points and details"""
        self.score += points_earned
        self.correct_answers += 1
        self.current_streak += 1
        self.max_streak = max(self.max_streak, self.current_streak)
        self.last_round_score = points_earned
        self.last_round_details = details
    
    def add_wrong_answer(self):
        """Add a wrong answer"""
        self.wrong_answers += 1
        self.current_streak = 0
        self.last_round_score = 0
        self.last_round_details = "回答错误，本轮得分为0分"


@dataclass
class QuestionData:
    """Question data structure"""
    riddle: str
    correct_answer: str
    choices: List[str]
    masked_choices: List[str]
    correct_index: int
    difficulty_level: int = 1  # 1-3 based on answer length


class AnswerGenerator:
    """Generates multiple choice answers with masking logic"""
    
    def __init__(self, xiehouyu_data: List[Dict]):
        self.data = xiehouyu_data
        self.answer_pool = [item['answer'] for item in xiehouyu_data]
        
    def generate_question(self) -> QuestionData:
        """Generate a complete question with masked multiple choices"""
        # Select random xiehouyu
        selected = random.choice(self.data)
        riddle = selected['riddle']
        correct_answer = selected['answer']
        
        # Handle multiple answers (separated by semicolon)
        if '；' in correct_answer:
            correct_answer = correct_answer.split('；')[0].strip()
        
        # Generate 3 incorrect answers
        incorrect_answers = self._generate_incorrect_answers(correct_answer, 3)
        
        # Combine all answers
        all_answers = [correct_answer] + incorrect_answers
        
        # Apply masking to all answers
        masked_answers = [self._mask_answer(answer) for answer in all_answers]
        
        # Randomize order
        combined = list(zip(all_answers, masked_answers))
        random.shuffle(combined)
        
        # Find correct answer index after shuffle
        correct_index = next(i for i, (orig, _) in enumerate(combined) if orig == correct_answer)
        
        choices, masked_choices = zip(*combined)
        
        return QuestionData(
            riddle=riddle,
            correct_answer=correct_answer,
            choices=list(choices),
            masked_choices=list(masked_choices),
            correct_index=correct_index,
            difficulty_level=self._calculate_difficulty(correct_answer)
        )
    
    def _generate_incorrect_answers(self, correct_answer: str, count: int) -> List[str]:
        """Generate incorrect answers similar in length and style"""
        correct_length = len(correct_answer)
        
        # Filter answers with similar length (±2 characters)
        similar_answers = [
            answer for answer in self.answer_pool 
            if abs(len(answer) - correct_length) <= 2 and answer != correct_answer
        ]
        
        # If not enough similar answers, use all other answers
        if len(similar_answers) < count:
            similar_answers = [answer for answer in self.answer_pool if answer != correct_answer]
        
        # Handle multiple answers in incorrect options too
        filtered_answers = []
        for answer in similar_answers:
            if '；' in answer:
                answer = answer.split('；')[0].strip()
            filtered_answers.append(answer)
        
        return random.sample(filtered_answers, min(count, len(filtered_answers)))
    
    def _mask_answer(self, answer: str) -> str:
        """Return the full answer without masking"""
        # Disabled masking feature - return original answer
        return answer
    
    def _calculate_difficulty(self, answer: str) -> int:
        """Calculate difficulty level based on answer characteristics"""
        length = len(answer)
        if length <= 3:
            return 1  # Easy
        elif length <= 6:
            return 2  # Medium
        else:
            return 3  # Hard


class ScoreManager:
    """Manages scoring system with bonus and detailed feedback"""
    
    def __init__(self, config: GameConfig):
        self.config = config
    
    def calculate_score_and_details(self, is_correct: bool, difficulty_level: int, is_first_to_answer: bool = False) -> tuple[int, str]:
        """Calculate score and detailed explanation for a round"""
        if not is_correct:
            return 0, "回答错误，本轮得分为0分"
        
        base_score = self.config.points_per_correct  # 基础得分2分
        
        if is_first_to_answer:
            # 优先回答者：基础分 + 优先奖励分
            bonus_score = self.config.bonus_for_correct  # 优先奖励1分
            total_score = base_score + bonus_score
            details = f"回答正确！获得{base_score}分基础得分 + {bonus_score}分优先回答奖励，本轮共得{total_score}分"
        else:
            # 非优先回答者：只有基础分
            total_score = base_score
            details = f"回答正确！获得{base_score}分基础得分，本轮共得{total_score}分"
        
        return total_score, details
    
    def calculate_score(self, is_correct: bool, difficulty_level: int) -> int:
        """Calculate score for a round (backwards compatibility)"""
        score, _ = self.calculate_score_and_details(is_correct, difficulty_level)
        return score


class GameState:
    """Main game state manager"""
    
    def __init__(self, xiehouyu_data: List[Dict], config: GameConfig = None):
        self.config = config or GameConfig()
        self.xiehouyu_data = xiehouyu_data
        self.answer_generator = AnswerGenerator(xiehouyu_data)
        self.score_manager = ScoreManager(self.config)
        
        # Game state
        self.phase = GamePhase.SETUP
        self.current_round = 0
        
        # Player stats
        self.player_stats = {
            PlayerSide.LEFT: PlayerStats(),
            PlayerSide.RIGHT: PlayerStats()
        }
        
        # Current questions - each player gets their own
        self.player_questions = {
            PlayerSide.LEFT: None,
            PlayerSide.RIGHT: None
        }
        self.player_answers = {PlayerSide.LEFT: None, PlayerSide.RIGHT: None}
        self.first_to_answer: Optional[PlayerSide] = None  # 追踪第一个回答的玩家
        
        # Game history
        self.round_history: List[Dict] = []
    
    def start_game(self):
        """Start a new game"""
        self.phase = GamePhase.PLAYING
        self.current_round = 0
        self.round_history = []
        
        # Reset player stats
        for player in self.player_stats:
            self.player_stats[player] = PlayerStats()
        
        self.start_new_round()
    
    def start_new_round(self):
        """Start a new round"""
        print(f"DEBUG: Starting new round. Current: {self.current_round}, Total: {self.config.total_rounds}")  # Debug log
        if self.current_round >= self.config.total_rounds:
            print(f"DEBUG: Reached max rounds, ending game")  # Debug log
            self.end_game()
            return
        
        self.current_round += 1
        print(f"DEBUG: Starting round {self.current_round}")  # Debug log
        # Generate separate questions for each player
        self.player_questions[PlayerSide.LEFT] = self.answer_generator.generate_question()
        self.player_questions[PlayerSide.RIGHT] = self.answer_generator.generate_question()
        self.player_answers = {PlayerSide.LEFT: None, PlayerSide.RIGHT: None}
        self.first_to_answer = None  # 重置第一个回答者追踪
        self.phase = GamePhase.WAITING
        print(f"DEBUG: New round started, phase set to WAITING")  # Debug log
    
    def submit_answer(self, player: PlayerSide, answer_index: int) -> bool:
        """Submit an answer for a player"""
        if self.phase != GamePhase.WAITING or self.player_answers[player] is not None:
            return False
        
        # 记录第一个回答的玩家
        is_first_to_answer = self.first_to_answer is None
        if is_first_to_answer:
            self.first_to_answer = player
        
        self.player_answers[player] = answer_index
        
        # Process answer
        player_question = self.player_questions[player]
        is_correct = answer_index == player_question.correct_index
        player_stats = self.player_stats[player]
        
        # Calculate score with details, including first-to-answer bonus
        score, details = self.score_manager.calculate_score_and_details(
            is_correct, 
            player_question.difficulty_level,
            is_first_to_answer
        )
        
        if is_correct:
            player_stats.add_correct_answer(score, details)
        else:
            player_stats.add_wrong_answer()
        
        # Check if both players answered
        if all(answer is not None for answer in self.player_answers.values()):
            print(f"DEBUG: Both players answered, showing feedback")  # Debug log
            self.show_round_feedback()
        
        return True
    
    def show_round_feedback(self):
        """Show round feedback phase"""
        self.phase = GamePhase.ROUND_FEEDBACK
        print(f"DEBUG: Entering round feedback phase")  # Debug log
    
    def continue_to_next_round(self):
        """Continue to next round or end game"""
        self.end_round()
        
        # Check if game should end
        if self.current_round >= self.config.total_rounds:
            print(f"DEBUG: Game should end now! Current: {self.current_round}, Total: {self.config.total_rounds}")  # Debug log
            self.end_game()
        else:
            # Start next round
            print(f"DEBUG: Starting next round")  # Debug log
            self.start_new_round()
    
    def end_round(self):
        """End current round and prepare for next"""
        # Save round history
        round_data = {
            'round': self.current_round,
            'questions': self.player_questions.copy(),
            'answers': self.player_answers.copy(),
            'scores': {player: stats.score for player, stats in self.player_stats.items()}
        }
        self.round_history.append(round_data)
        
        self.phase = GamePhase.PLAYING
    
    def end_game(self):
        """End the game"""
        print(f"DEBUG: Game ending, setting phase to FINISHED")  # Debug log
        self.phase = GamePhase.FINISHED
        print(f"DEBUG: Game phase is now {self.phase}")  # Debug log
    
    def get_winner(self) -> Optional[PlayerSide]:
        """Get the game winner"""
        if self.phase != GamePhase.FINISHED:
            return None
        
        left_score = self.player_stats[PlayerSide.LEFT].score
        right_score = self.player_stats[PlayerSide.RIGHT].score
        
        if left_score > right_score:
            return PlayerSide.LEFT
        elif right_score > left_score:
            return PlayerSide.RIGHT
        else:
            return None  # Tie
    
    def get_game_summary(self) -> Dict:
        """Get comprehensive game summary"""
        return {
            'total_rounds': self.current_round,
            'winner': self.get_winner(),
            'player_stats': {
                'left': self.player_stats[PlayerSide.LEFT],
                'right': self.player_stats[PlayerSide.RIGHT]
            },
            'round_history': self.round_history
        }
    
    def get_player_question(self, player: PlayerSide) -> Optional[QuestionData]:
        """Get question for specific player"""
        return self.player_questions.get(player)