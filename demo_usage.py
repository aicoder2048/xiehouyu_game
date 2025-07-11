#!/usr/bin/env python3
"""
Demo usage of the Xiehouyu Explorer
"""

from xiehouyu_explorer import XiehouyuExplorer

def demo():
    explorer = XiehouyuExplorer()
    
    print("=== Xiehouyu Explorer Demo ===\n")
    
    # Basic stats
    stats = explorer.stats()
    print(f"Dataset contains {stats['total_xiehouyu']:,} xiehouyu entries\n")
    
    # Search examples
    print("=== Search Examples ===")
    
    # Search for riddles containing "老虎"
    tiger_riddles = explorer.search_riddles("老虎", 3)
    print("Riddles containing '老虎':")
    for item in tiger_riddles:
        print(f"  {item['riddle']} —— {item['answer']}")
    print()
    
    # Search for answers containing "聪明"
    smart_answers = explorer.search_answers("聪明", 3)
    print("Answers containing '聪明':")
    for item in smart_answers:
        print(f"  {item['riddle']} —— {item['answer']}")
    print()
    
    # Lookup specific riddle
    print("=== Lookup Examples ===")
    test_riddle = "八仙过海"
    answer = explorer.lookup_by_riddle(test_riddle)
    if answer:
        print(f"Riddle: {test_riddle}")
        print(f"Answer: {answer}")
    else:
        print(f"Riddle '{test_riddle}' not found")
    print()
    
    # Reverse lookup
    test_answer = "各显神通"
    riddles = explorer.lookup_by_answer(test_answer)
    if riddles:
        print(f"Answer: {test_answer}")
        print("Found riddles:")
        for riddle in riddles:
            print(f"  {riddle}")
    else:
        print(f"Answer '{test_answer}' not found")
    print()
    
    # Random samples
    print("=== Random Samples ===")
    random_samples = explorer.random_xiehouyu(5)
    for i, item in enumerate(random_samples, 1):
        print(f"{i}. {item['riddle']} —— {item['answer']}")
    print()
    
    # Length analysis
    short_riddles = explorer.riddles_by_length(0, 4)
    long_riddles = explorer.riddles_by_length(10, 20)
    print(f"Short riddles (≤4 chars): {len(short_riddles)}")
    print(f"Long riddles (10-20 chars): {len(long_riddles)}")
    
    if short_riddles:
        print("Example short riddle:")
        print(f"  {short_riddles[0]['riddle']} —— {short_riddles[0]['answer']}")
    
    if long_riddles:
        print("Example long riddle:")
        print(f"  {long_riddles[0]['riddle']} —— {long_riddles[0]['answer']}")

if __name__ == "__main__":
    demo()