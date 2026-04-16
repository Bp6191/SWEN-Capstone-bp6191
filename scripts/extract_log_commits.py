#!/usr/bin/env python3
"""
Extract logging-related commits from a git repository.
Usage: python extract_log_commits.py <repo_path> <output_csv>
"""

import subprocess
import csv
import sys
import re
from datetime import datetime

def get_all_commits(repo_path):
    """Get all commit hashes from the repository."""
    cmd = ["git", "-C", repo_path, "log", "--all", "--pretty=format:%H"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip().split('\n')

def get_commit_info(repo_path, commit_hash):
    """Get detailed information about a commit."""
    # Get commit metadata
    cmd = ["git", "-C", repo_path, "show", "--pretty=format:%H|%an|%ae|%ad|%s", 
           "--no-patch", commit_hash]
    result = subprocess.run(cmd, capture_output=True, text=True)
    parts = result.stdout.strip().split('|')
    
    if len(parts) < 5:
        return None
    
    commit_info = {
        'hash': parts[0],
        'author': parts[1],
        'email': parts[2],
        'date': parts[3],
        'message': parts[4]
    }
    
    # Get diff to check for logging changes
    cmd = ["git", "-C", repo_path, "show", commit_hash]
    result = subprocess.run(cmd, capture_output=True, text=True)
    diff = result.stdout
    
    return commit_info, diff

def is_logging_commit(diff, commit_message):
    """
    Determine if a commit is logging-related.
    Checks both diff content and commit message.
    """
    # Logging patterns in code
    log_patterns = [
        r'LOG\(',           # General LOG macro
        r'ROCKS_LOG_',      # RocksDB logging
        r'ENVOY_LOG\(',     # Envoy logging
        r'logger\.\w+\(',   # ScyllaDB/Seastar logging 
        r'DLOG\(',          # Debug log
        r'VLOG\(',          # Verbose log
        r'spdlog::',        # spdlog framework
        r'glog::',          # glog framework
        r'LOG_INFO',        # Common log macros
        r'LOG_ERROR',
        r'LOG_WARN',
        r'LOG_DEBUG',
        r'fprintf\(stderr', # C-style logging
        r'printf\(',        # printf logging
        r'std::cout\s*<<',  # cout logging
        r'std::cerr\s*<<',  # cerr logging
    ]
    
    # Check if diff contains logging changes
    for pattern in log_patterns:
        if re.search(pattern, diff, re.IGNORECASE):
            return True
    
    # Check commit message for logging-related keywords
    log_keywords = ['log', 'logging', 'logger', 'trace', 'debug output']
    message_lower = commit_message.lower()
    for keyword in log_keywords:
        if keyword in message_lower:
            return True
    
    return False

def categorize_commit(commit_message):
    """Categorize commit by intent based on message."""
    message_lower = commit_message.lower()
    
    # Bug fix
    if any(word in message_lower for word in ['fix', 'bug', 'issue', 'patch', 'correct']):
        return 'bug_fix'
    
    # Feature addition
    if any(word in message_lower for word in ['add', 'implement', 'feature', 'new', 'support']):
        return 'feature'
    
    # Refactoring
    if any(word in message_lower for word in ['refactor', 'cleanup', 'improve', 'reorganize', 'simplify']):
        return 'refactor'
    
    # Logging improvement
    if any(word in message_lower for word in ['logging', 'log level', 'trace', 'verbose']):
        return 'logging_improvement'
    
    return 'other'

def analyze_diff_changes(diff):
    """Analyze what changed in the diff regarding logging."""
    lines = diff.split('\n')
    
    added_logs = 0
    removed_logs = 0
    modified_logs = 0
    
    # log_pattern = re.compile(r'LOG\(|spdlog::|glog::|LOG_INFO|LOG_ERROR|LOG_WARN|LOG_DEBUG')
    log_pattern = re.compile(r'LOG\(|ROCKS_LOG_|ENVOY_LOG\(|logger\.\w+\(|spdlog::|glog::|LOG_INFO|LOG_ERROR|LOG_WARN|LOG_DEBUG')
    
    for line in lines:
        if line.startswith('+') and log_pattern.search(line):
            added_logs += 1
        elif line.startswith('-') and log_pattern.search(line):
            removed_logs += 1
    
    # If both added and removed, consider it modification
    if added_logs > 0 and removed_logs > 0:
        modified_logs = min(added_logs, removed_logs)
        added_logs -= modified_logs
        removed_logs -= modified_logs
    
    return {
        'added': added_logs,
        'removed': removed_logs,
        'modified': modified_logs
    }

def main(repo_path, output_file):
    """Main function to extract logging commits."""
    print(f"Analyzing repository: {repo_path}")
    
    # Get all commits
    print("Fetching all commits...")
    commits = get_all_commits(repo_path)
    print(f"Total commits: {len(commits)}")
    
    # Analyze each commit
    logging_commits = []
    
    print("Analyzing commits for logging changes...")
    for i, commit_hash in enumerate(commits):
        if i % 100 == 0:
            print(f"Progress: {i}/{len(commits)} commits analyzed")
        
        try:
            result = get_commit_info(repo_path, commit_hash)
            if result is None:
                continue
            
            commit_info, diff = result
            
            # Check if logging-related
            if is_logging_commit(diff, commit_info['message']):
                # Categorize
                category = categorize_commit(commit_info['message'])
                
                # Analyze changes
                changes = analyze_diff_changes(diff)
                
                # Store result
                logging_commits.append({
                    'hash': commit_info['hash'],
                    'author': commit_info['author'],
                    'date': commit_info['date'],
                    'message': commit_info['message'].replace('\n', ' '),
                    'category': category,
                    'logs_added': changes['added'],
                    'logs_removed': changes['removed'],
                    'logs_modified': changes['modified']
                })
        
        except Exception as e:
            print(f"Error processing commit {commit_hash}: {e}")
            continue
    
    print(f"\nFound {len(logging_commits)} logging-related commits")
    
    # Write to CSV
    print(f"Writing results to {output_file}")
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['hash', 'author', 'date', 'message', 'category', 
                     'logs_added', 'logs_removed', 'logs_modified']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for commit in logging_commits:
            writer.writerow(commit)
    
    print("Done!")
    
    # Print summary statistics
    print("\n=== SUMMARY ===")
    print(f"Total commits analyzed: {len(commits)}")
    print(f"Logging-related commits: {len(logging_commits)}")
    print(f"Percentage: {len(logging_commits)/len(commits)*100:.2f}%")
    
    # Category breakdown
    categories = {}
    for commit in logging_commits:
        cat = commit['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nCommit categories:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count} ({count/len(logging_commits)*100:.1f}%)")
    
    # Change statistics
    total_added = sum(c['logs_added'] for c in logging_commits)
    total_removed = sum(c['logs_removed'] for c in logging_commits)
    total_modified = sum(c['logs_modified'] for c in logging_commits)
    
    print(f"\nLogging changes:")
    print(f"  Logs added: {total_added}")
    print(f"  Logs removed: {total_removed}")
    print(f"  Logs modified: {total_modified}")
    print(f"  Net change: {total_added - total_removed}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_log_commits.py <repo_path> <output_csv>")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    output_file = sys.argv[2]
    
    main(repo_path, output_file)