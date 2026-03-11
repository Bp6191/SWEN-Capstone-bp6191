#!/usr/bin/env python3
"""
Analyze logging evolution trends from extracted commits.
Usage: python analyze_evolution.py <input_csv> <output_dir>
"""

import csv
import sys
from datetime import datetime
from collections import defaultdict
import os

def parse_date(date_str):
    """Parse git date string to datetime."""
    try:
        # Git date format: "Day Mon DD HH:MM:SS YYYY +ZZZZ"
        return datetime.strptime(date_str.split('+')[0].strip(), "%a %b %d %H:%M:%S %Y")
    except:
        return None

def analyze_temporal_trends(commits):
    """Analyze how logging changes over time."""
    # Group by year-month
    monthly_stats = defaultdict(lambda: {
        'total_commits': 0,
        'logs_added': 0,
        'logs_removed': 0,
        'logs_modified': 0
    })
    
    for commit in commits:
        date = parse_date(commit['date'])
        if date:
            month_key = date.strftime('%Y-%m')
            monthly_stats[month_key]['total_commits'] += 1
            monthly_stats[month_key]['logs_added'] += int(commit['logs_added'])
            monthly_stats[month_key]['logs_removed'] += int(commit['logs_removed'])
            monthly_stats[month_key]['logs_modified'] += int(commit['logs_modified'])
    
    return dict(sorted(monthly_stats.items()))

def analyze_category_distribution(commits):
    """Analyze distribution of commit categories."""
    categories = defaultdict(int)
    
    for commit in commits:
        categories[commit['category']] += 1
    
    return dict(categories)

def analyze_churn(commits):
    """Calculate logging churn rate."""
    total_added = sum(int(c['logs_added']) for c in commits)
    total_removed = sum(int(c['logs_removed']) for c in commits)
    total_modified = sum(int(c['logs_modified']) for c in commits)
    
    total_changes = total_added + total_removed + total_modified
    churn_rate = total_modified / total_changes if total_changes > 0 else 0
    
    return {
        'total_added': total_added,
        'total_removed': total_removed,
        'total_modified': total_modified,
        'total_changes': total_changes,
        'churn_rate': churn_rate,
        'net_change': total_added - total_removed
    }

def main(input_file, output_dir):
    """Main analysis function."""
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Read commits
    print(f"Reading commits from {input_file}...")
    commits = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        commits = list(reader)
    
    print(f"Loaded {len(commits)} logging-related commits")
    
    # Temporal trends
    print("\nAnalyzing temporal trends...")
    monthly_stats = analyze_temporal_trends(commits)
    
    temporal_output = os.path.join(output_dir, 'temporal_trends.csv')
    with open(temporal_output, 'w', newline='') as f:
        fieldnames = ['month', 'total_commits', 'logs_added', 'logs_removed', 
                     'logs_modified', 'net_change']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for month, stats in monthly_stats.items():
            writer.writerow({
                'month': month,
                'total_commits': stats['total_commits'],
                'logs_added': stats['logs_added'],
                'logs_removed': stats['logs_removed'],
                'logs_modified': stats['logs_modified'],
                'net_change': stats['logs_added'] - stats['logs_removed']
            })
    
    print(f"Temporal trends saved to {temporal_output}")
    
    # Category distribution
    print("\nAnalyzing commit categories...")
    categories = analyze_category_distribution(commits)
    
    category_output = os.path.join(output_dir, 'category_distribution.csv')
    with open(category_output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['category', 'count', 'percentage'])
        
        total = len(commits)
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            writer.writerow([cat, count, f"{count/total*100:.1f}%"])
    
    print(f"Category distribution saved to {category_output}")
    
    # Churn analysis
    print("\nAnalyzing logging churn...")
    churn_stats = analyze_churn(commits)
    
    churn_output = os.path.join(output_dir, 'churn_analysis.txt')
    with open(churn_output, 'w') as f:
        f.write("LOGGING CHURN ANALYSIS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total logs added: {churn_stats['total_added']}\n")
        f.write(f"Total logs removed: {churn_stats['total_removed']}\n")
        f.write(f"Total logs modified: {churn_stats['total_modified']}\n")
        f.write(f"Total changes: {churn_stats['total_changes']}\n")
        f.write(f"Net change: {churn_stats['net_change']}\n")
        f.write(f"Churn rate: {churn_stats['churn_rate']:.2%}\n")
    
    print(f"Churn analysis saved to {churn_output}")
    
    print("\n=== ANALYSIS COMPLETE ===")
    print(f"Results saved to {output_dir}/")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python analyze_evolution.py <input_csv> <output_dir>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])