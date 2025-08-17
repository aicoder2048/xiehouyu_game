#!/usr/bin/env python3
"""
Test script for the xiehouyu game logic
"""

import json
from game_logic import GameState, GameConfig, PlayerSide, AnswerGenerator


def test_game_logic():
    """Test the core game logic"""
    print("🧪 Testing Xiehouyu Game Logic...")
    
    # Load test data
    try:
        with open('xiehouyu.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Loaded {len(data)} xiehouyu entries")
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return
    
    # Test AnswerGenerator
    print("\n📝 Testing AnswerGenerator...")
    generator = AnswerGenerator(data)
    
    # Generate a few questions
    for i in range(3):
        question = generator.generate_question()
        print(f"\n问题 {i+1}:")
        print(f"  谜面: {question.riddle}")
        print(f"  正确答案: {question.correct_answer}")
        print(f"  难度: {question.difficulty_level}")
        print(f"  选项:")
        for j, (choice, masked) in enumerate(zip(question.choices, question.masked_choices)):
            marker = "✓" if j == question.correct_index else " "
            print(f"    {marker} {j+1}. {masked} (原文: {choice})")
    
    # Test GameState
    print("\n🎮 Testing GameState...")
    config = GameConfig(total_rounds=3, points_per_correct=2, bonus_for_correct=1)
    game_state = GameState(data, config)
    
    print(f"Initial game phase: {game_state.phase}")
    
    # Start game
    game_state.start_game()
    print(f"Game started, phase: {game_state.phase}")
    print(f"Current round: {game_state.current_round}")
    
    # Get questions for both players
    left_question = game_state.get_player_question(PlayerSide.LEFT)
    right_question = game_state.get_player_question(PlayerSide.RIGHT)
    
    if left_question:
        print(f"Left player question: {left_question.riddle}")
        print(f"Left player correct answer: {left_question.correct_answer}")
    
    if right_question:
        print(f"Right player question: {right_question.riddle}")
        print(f"Right player correct answer: {right_question.correct_answer}")
    
    # Test answer submission
    print("\n🔍 Testing answer submission...")
    if left_question and right_question:
        left_correct_idx = left_question.correct_index
        right_correct_idx = right_question.correct_index
        
        # Test 1: Player 1 submits correct answer first (should get priority bonus)
        success = game_state.submit_answer(PlayerSide.LEFT, left_correct_idx)
        print(f"Player 1 submitted correct answer first: {success}")
        print(f"First to answer: {game_state.first_to_answer}")
        
        # Test 2: Player 2 submits correct answer second (should get only base score)
        success = game_state.submit_answer(PlayerSide.RIGHT, right_correct_idx)
        print(f"Player 2 submitted correct answer second: {success}")
        
        # Check scores
        left_stats = game_state.player_stats[PlayerSide.LEFT]
        right_stats = game_state.player_stats[PlayerSide.RIGHT]
        
        print(f"\n📊 Scores after round 1:")
        print(f"  Player 1 (优先回答): {left_stats.score} points, {left_stats.correct_answers} correct")
        print(f"  Player 1 details: {left_stats.last_round_details}")
        print(f"  Player 2 (非优先回答): {right_stats.score} points, {right_stats.correct_answers} correct")
        print(f"  Player 2 details: {right_stats.last_round_details}")
        print(f"  Game phase: {game_state.phase}")
        
        # Verify expected scores
        expected_left_score = 3  # 2基础 + 1优先奖励
        expected_right_score = 2  # 2基础
        if left_stats.score == expected_left_score and right_stats.score == expected_right_score:
            print("✅ 得分逻辑正确！优先回答者获得奖励分")
        else:
            print(f"❌ 得分逻辑错误！期望左侧{expected_left_score}分，右侧{expected_right_score}分")
    
    print("\n✅ Game logic test completed successfully!")


def test_masking_logic():
    """Test the answer masking logic"""
    print("\n🎭 Testing Answer Masking Logic...")
    
    test_answers = [
        "斤斤计较",
        "自讨苦吃",
        "多面手",
        "框框套套",
        "好当家"
    ]
    
    # Load data for generator
    try:
        with open('xiehouyu.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        generator = AnswerGenerator(data)
        
        for answer in test_answers:
            masked = generator._mask_answer(answer)
            print(f"  {answer} → {masked}")
    except Exception as e:
        print(f"❌ Masking test failed: {e}")


if __name__ == "__main__":
    test_game_logic()
    test_masking_logic()