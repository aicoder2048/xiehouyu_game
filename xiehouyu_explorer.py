#!/usr/bin/env python3
"""
Chinese Xiehouyu Dataset Explorer

A utility script to explore and analyze the Chinese xiehouyu dataset.
Each xiehouyu consists of a riddle and its corresponding answer.
"""

import json
import random
import re
from collections import Counter
from typing import List, Dict, Optional, Tuple


class XiehouyuExplorer:
    def __init__(self, json_file: str = "xiehouyu.json"):
        """Initialize the explorer with the xiehouyu dataset."""
        self.json_file = json_file
        self.data = self._load_data()
        self.riddle_to_answer = {item['riddle']: item['answer'] for item in self.data}
        self.answer_to_riddles = self._build_answer_index()
    
    def _load_data(self) -> List[Dict]:
        """Load the xiehouyu data from JSON file."""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File '{self.json_file}' not found.")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file '{self.json_file}'.")
            return []
    
    def _build_answer_index(self) -> Dict[str, List[str]]:
        """Build reverse index from answers to riddles."""
        answer_index = {}
        for item in self.data:
            riddle = item['riddle']
            answer = item['answer']
            # Handle multiple answers separated by semicolon
            answers = [ans.strip() for ans in answer.split('；')]
            for ans in answers:
                if ans not in answer_index:
                    answer_index[ans] = []
                answer_index[ans].append(riddle)
        return answer_index
    
    def stats(self) -> Dict:
        """Get basic statistics about the dataset."""
        total_count = len(self.data)
        unique_riddles = len(set(item['riddle'] for item in self.data))
        unique_answers = len(set(item['answer'] for item in self.data))
        
        # Count riddles with multiple answers
        multi_answer_count = sum(1 for item in self.data if '；' in item['answer'])
        
        # Average length of riddles and answers
        avg_riddle_length = sum(len(item['riddle']) for item in self.data) / total_count
        avg_answer_length = sum(len(item['answer']) for item in self.data) / total_count
        
        return {
            'total_xiehouyu': total_count,
            'unique_riddles': unique_riddles,
            'unique_answers': unique_answers,
            'multi_answer_riddles': multi_answer_count,
            'avg_riddle_length': round(avg_riddle_length, 2),
            'avg_answer_length': round(avg_answer_length, 2)
        }
    
    def lookup_by_riddle(self, riddle: str) -> Optional[str]:
        """Find answer for a given riddle."""
        return self.riddle_to_answer.get(riddle)
    
    def lookup_by_answer(self, answer: str) -> List[str]:
        """Find riddles for a given answer."""
        return self.answer_to_riddles.get(answer, [])
    
    def search_riddles(self, keyword: str, limit: int = 10) -> List[Dict]:
        """Search for riddles containing a keyword."""
        results = []
        for item in self.data:
            if keyword in item['riddle']:
                results.append(item)
                if len(results) >= limit:
                    break
        return results
    
    def search_answers(self, keyword: str, limit: int = 10) -> List[Dict]:
        """Search for answers containing a keyword."""
        results = []
        for item in self.data:
            if keyword in item['answer']:
                results.append(item)
                if len(results) >= limit:
                    break
        return results
    
    def random_xiehouyu(self, count: int = 1) -> List[Dict]:
        """Get random xiehouyu entries."""
        return random.sample(self.data, min(count, len(self.data)))
    
    def most_common_words(self, field: str = 'riddle', top_n: int = 10) -> List[Tuple[str, int]]:
        """Find most common words in riddles or answers."""
        text = ' '.join(item[field] for item in self.data)
        # Simple word extraction for Chinese text
        words = re.findall(r'[\u4e00-\u9fff]+', text)
        return Counter(words).most_common(top_n)
    
    def riddles_by_length(self, min_length: int = 0, max_length: int = 100) -> List[Dict]:
        """Get riddles within specified length range."""
        return [item for item in self.data 
                if min_length <= len(item['riddle']) <= max_length]
    
    def duplicate_riddles(self) -> List[str]:
        """Find duplicate riddles in the dataset."""
        riddle_counts = Counter(item['riddle'] for item in self.data)
        return [riddle for riddle, count in riddle_counts.items() if count > 1]
    
    def print_stats(self):
        """Print formatted statistics."""
        stats = self.stats()
        print("=== Chinese Xiehouyu Dataset Statistics ===")
        print(f"Total xiehouyu: {stats['total_xiehouyu']:,}")
        print(f"Unique riddles: {stats['unique_riddles']:,}")
        print(f"Unique answers: {stats['unique_answers']:,}")
        print(f"Multi-answer riddles: {stats['multi_answer_riddles']:,}")
        print(f"Average riddle length: {stats['avg_riddle_length']} characters")
        print(f"Average answer length: {stats['avg_answer_length']} characters")
        print()
    
    def print_random_samples(self, count: int = 5):
        """Print random xiehouyu samples."""
        samples = self.random_xiehouyu(count)
        print(f"=== Random Xiehouyu Samples ({count}) ===")
        for i, item in enumerate(samples, 1):
            print(f"{i}. {item['riddle']} —— {item['answer']}")
        print()
    
    def interactive_lookup(self):
        """Interactive lookup mode."""
        print("=== Interactive Lookup Mode ===")
        print("Type 'riddle: <text>' to find answer")
        print("Type 'answer: <text>' to find riddles")
        print("Type 'search: <keyword>' to search riddles")
        print("Type 'random' for random xiehouyu")
        print("Type 'quit' to exit")
        print()
        
        while True:
            try:
                query = input("Enter query: ").strip()
                if query.lower() == 'quit':
                    break
                elif query.lower() == 'random':
                    sample = self.random_xiehouyu(1)[0]
                    print(f"Random: {sample['riddle']} —— {sample['answer']}")
                elif query.startswith('riddle:'):
                    riddle = query[7:].strip()
                    answer = self.lookup_by_riddle(riddle)
                    if answer:
                        print(f"Answer: {answer}")
                    else:
                        print("Riddle not found")
                elif query.startswith('answer:'):
                    answer = query[7:].strip()
                    riddles = self.lookup_by_answer(answer)
                    if riddles:
                        print(f"Found {len(riddles)} riddle(s):")
                        for riddle in riddles:
                            print(f"  - {riddle}")
                    else:
                        print("Answer not found")
                elif query.startswith('search:'):
                    keyword = query[7:].strip()
                    results = self.search_riddles(keyword, 5)
                    if results:
                        print(f"Found {len(results)} riddle(s) with '{keyword}':")
                        for item in results:
                            print(f"  - {item['riddle']} —— {item['answer']}")
                    else:
                        print(f"No riddles found with '{keyword}'")
                else:
                    print("Invalid format. Use 'riddle:', 'answer:', 'search:', or 'random'")
                print()
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break


def main():
    """Main function to demonstrate the explorer."""
    explorer = XiehouyuExplorer()
    
    if not explorer.data:
        print("Failed to load data. Please check the JSON file.")
        return
    
    # Print basic statistics
    explorer.print_stats()
    
    # Show random samples
    explorer.print_random_samples(3)
    
    # Show most common words
    print("=== Most Common Words in Riddles ===")
    common_words = explorer.most_common_words('riddle', 10)
    for word, count in common_words:
        print(f"{word}: {count}")
    print()
    
    # Show some example lookups
    print("=== Example Lookups ===")
    sample = explorer.random_xiehouyu(1)[0]
    print(f"Looking up riddle: {sample['riddle']}")
    print(f"Answer: {explorer.lookup_by_riddle(sample['riddle'])}")
    print()
    
    # Find duplicates
    duplicates = explorer.duplicate_riddles()
    if duplicates:
        print(f"Found {len(duplicates)} duplicate riddles")
        print("First few duplicates:")
        for dup in duplicates[:3]:
            print(f"  - {dup}")
    else:
        print("No duplicate riddles found")
    print()
    
    # Interactive mode
    try:
        choice = input("Enter interactive mode? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            explorer.interactive_lookup()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")


if __name__ == "__main__":
    main()