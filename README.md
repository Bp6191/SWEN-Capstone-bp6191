# Empirical Study of Logging Practices and Evolution in Modern C++ Distributed Systems

**Author:** Bharathi Pandurangan  
**Institution:** Rochester Institute of Technology  
**Program:** Graduate Software Engineering  
**Advisor:** Dr. Yiming Tang  

---

## Project Overview

This capstone project conducts an empirical study to characterize logging practices in modern C++ distributed systems and analyze how these practices evolve over time. 

**Research Questions:**
1. **RQ1:** What logging practices are prevalent in modern C++ distributed systems?
2. **RQ2:** How do logging practices evolve over time in C++ distributed systems?
3. **RQ3:** How do logging practices and evolution patterns vary across different types of distributed systems?

**Key Contribution:** This is the first study to empirically characterize logging practices in modern C++ distributed systems and analyze their evolution through historical commit analysis.

---

## Motivation

Previous work by Yuan et al. (2012) studied C++ logging practices, but this research is now over a decade old. Modern C++ distributed systems have evolved significantly:
- Modern C++ standards (C++11/14/17/20)
- Cloud-native architectures
- Advanced observability tools (OpenTelemetry, distributed tracing)
- Data-intensive workloads

This study addresses the research gap by analyzing **modern** C++ distributed systems and tracking logging evolution over their development history.

---

## Selected Systems

We analyze 5 representative C++ distributed systems selected based on GitHub stars, domain diversity, and active development:

| System | Domain | GitHub Stars | C++ % | LOC | Repository |
|--------|--------|--------------|-------|-----|------------|
| **ClickHouse** | Analytical DB | 37K | 71.2% | 1.2M | [Link](https://github.com/ClickHouse/ClickHouse.git) |
| **Apache Kudu** | Distributed DB | 1.9K  | & 79.7% | 300K | [Link](https://github.com/apache/kudu.git) |
| **RocksDB** | Storage engine | 28K | 95% | 250K | [Link](https://github.com/facebook/rocksdb) |
| **Envoy** | Service mesh | 25K | 90% | 400K | [Link](https://github.com/envoyproxy/envoy) |
| **ScyllaDB** | NoSQL DB | 13K | 73.4% | 150K | [Link](https://github.com/scylladb/scylladb.git) |

---

## Quick Start

### Prerequisites

- **Python 3.7+**
- **Git** (for cloning repositories)
- **Libraries:** (install via pip)
```bash
  pip install pandas matplotlib scipy
```

### Installation

1. **Clone this repository:**
```bash
   git clone https://github.com/yourusername/SWEN-Capstone-bp6191.git
   cd SWEN-Capstone-bp6191
```

2. **Clone the target systems:**
```bash
   mkdir repos
   cd repos
   git clone https://github.com/redis/redis.git
   git clone https://github.com/ClickHouse/ClickHouse.git
   git clone https://github.com/facebook/rocksdb.git
   git clone https://github.com/envoyproxy/envoy.git
   git clone https://github.com/tikv/tikv.git
   cd ..
```

### Running the Analysis

#### Option 1: Run Complete Analysis (All Systems)
```bash
# Make script executable (Mac/Linux)
chmod +x scripts/run_analysis.sh

# Run complete analysis
./scripts/run_analysis.sh
```

#### Option 2: Run Analysis on Individual Systems
```bash
# Extract logging commits from RocksDB
python scripts/extract_log_commits.py repos/rocksdb results/rocksdb_commits.csv

# Analyze temporal trends
python scripts/analyze_evolution.py results/rocksdb_commits.csv results/rocksdb_analysis
```

---

## Methodology

### RQ1: Current Logging Practices (Static Analysis)

**Data Collection:**
1. Extract all logging statements from latest codebase
2. Categorize by: log level, framework, location, contextual information

**Metrics:**
- Logging density (logs per 1000 LOC)
- Log level distribution (DEBUG, INFO, WARN, ERROR)
- Framework adoption (spdlog, glog, custom)
- Contextual information completeness

### RQ2: Logging Evolution (Git Mining)

**Data Collection:**
1. Clone full git history for each system
2. Identify logging-related commits via diff analysis and message keywords
3. Extract commit metadata: hash, author, date, message
4. Categorize commits by intent: bug fix, feature, refactoring, logging improvement

**Metrics:**
- Logging commit frequency over time
- Logging churn rate
- Net logging growth
- Category distribution

**Tools:**
- `extract_log_commits.py` - Mines git history for logging commits
- `analyze_evolution.py` - Analyzes temporal trends and categorizes changes

### RQ3: Cross-System Comparison

**Analysis:**
- Statistical comparison (Chi-square, t-tests)
- Domain-specific patterns (databases vs service mesh vs storage)
- Evolution pattern comparison
---

## Tools & Scripts

### `extract_log_commits.py`

Mines git history to identify and extract logging-related commits.

**Usage:**
```bash
python scripts/extract_log_commits.py  
```

**Example:**
```bash
python scripts/extract_log_commits.py repos/redis results/redis_commits.csv
```

**Output:** CSV file with columns:
- `hash`: Commit hash
- `author`: Commit author
- `date`: Commit date
- `message`: Commit message
- `category`: bug_fix | feature | refactor | logging_improvement
- `logs_added`: Number of log statements added
- `logs_removed`: Number of log statements removed
- `logs_modified`: Number of log statements modified

**Detection Method:**
- Searches for patterns: `LOG(`, `spdlog::`, `glog::`, `LOG_INFO`, `LOG_ERROR`, etc.
- Analyzes commit messages for keywords: log, logging, trace, debug
- Categorizes by commit message intent

---

### `analyze_evolution.py`

Analyzes temporal trends from extracted commit data.

**Usage:**
```bash
python scripts/analyze_evolution.py  
```

**Example:**
```bash
python scripts/analyze_evolution.py results/redis_commits.csv results/redis_analysis
```

**Output Files:**
- `temporal_trends.csv` - Monthly statistics (commits, logs added/removed)
- `category_distribution.csv` - Commit category breakdown
- `churn_analysis.txt` - Churn rate and net change metrics

---

## License

This project is for academic purposes as part of a graduate capstone requirement at Rochester Institute of Technology.

---

## Acknowledgments

- **Advisor:** Dr. Yiming Tang, for guidance and feedback throughout the project
- **RIT Software Engineering Department:** For providing resources and support
- **Open Source Communities:** Apache Kudu, ClickHouse, RocksDB, Envoy, and Scylladb for maintaining excellent distributed systems that made this research possible
---

## Known Issues

- **Unicode encoding errors:** Some commits with non-English characters may be skipped during git mining (affects <1% of commits)
- **Large repositories:** ClickHouse analysis may take 6-8 hours due to repository size (80,000+ commits)

**Workarounds:** Scripts include error handling to continue processing despite encoding issues.
