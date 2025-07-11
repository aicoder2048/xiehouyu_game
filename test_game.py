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
    config = GameConfig(total_rounds=3, round_time_limit=30)
    game_state = GameState(data, config)
    
    print(f"Initial game phase: {game_state.phase}")
    
    # Start game
    game_state.start_game()
    print(f"Game started, phase: {game_state.phase}")
    print(f"Current round: {game_state.current_round}")
    
    if game_state.current_question:
        print(f"Current question: {game_state.current_question.riddle}")
    
    # Test answer submission
    print("\n🔍 Testing answer submission...")
    correct_idx = game_state.current_question.correct_index
    
    # Player 1 submits correct answer
    success = game_state.submit_answer(PlayerSide.LEFT, correct_idx)
    print(f"Player 1 submitted correct answer: {success}")
    
    # Player 2 submits wrong answer
    wrong_idx = (correct_idx + 1) % 4
    success = game_state.submit_answer(PlayerSide.RIGHT, wrong_idx)
    print(f"Player 2 submitted wrong answer: {success}")
    
    # Check scores
    left_stats = game_state.player_stats[PlayerSide.LEFT]
    right_stats = game_state.player_stats[PlayerSide.RIGHT]
    
    print(f"\n📊 Scores after round 1:")
    print(f"  Player 1: {left_stats.score} points, {left_stats.correct_answers} correct")
    print(f"  Player 2: {right_stats.score} points, {right_stats.correct_answers} correct")
    
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