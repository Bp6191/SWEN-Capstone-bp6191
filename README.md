# Empirical Study of Logging Practices and Evolution in Modern C++ Distributed Systems

A graduate capstone research project at Rochester Institute of Technology (RIT) that empirically studies logging practices and their evolution in open-source C++ distributed systems. The study analyzes over 2.3 million lines of code and mines 39,675 git commits (2020–2025) across five major projects to answer three research questions:

- **RQ1:** What logging practices are prevalent in modern C++ distributed systems?
- **RQ2:** How do logging practices evolve over time?
- **RQ3:** How do practices vary across different types of distributed systems?

**Author:** Bharathi Pandurangan  
**Advisor:** Dr. Yiming Tang, Department of Software Engineering, RIT  
**Program:** MS Software Engineering, Rochester Institute of Technology

---

## Systems Studied

| System | Domain | Stars | C++ % | LOC | Logging Framework |
|--------|--------|-------|-------|-----|-------------------|
| [ClickHouse](https://github.com/ClickHouse/ClickHouse) | Analytical DB (OLAP) | 37K | 71.2% | 1.2M | `LOG_*` macros |
| [RocksDB](https://github.com/facebook/rocksdb) | Storage Engine | 28K | 83.4% | 250K | `ROCKS_LOG_LEVEL()` |
| [Envoy](https://github.com/envoyproxy/envoy) | Service Mesh / Proxy | 25K | 88.1% | 400K | `ENVOY_LOG()` |
| [Apache Kudu](https://github.com/apache/kudu) | Distributed DB | 1.9K | 79.7% | 300K | glog `LOG()` |
| [ScyllaDB](https://github.com/scylladb/scylladb) | NoSQL DB | 13K | 73.4% | 150K | Seastar `logger.level()` |

---
<!-- 
## Repository Structure

```
.
├── scripts/
│   ├── extract_log_commits.py   # Mine logging-related commits from a repo
│   └── analyze_evolution.py     # Analyze temporal trends and churn from mined data
├── results/
│   ├── rq1_log_counts.csv       # Total log statement counts per system
│   ├── rq1_log_levels.csv       # Log level breakdown per system
│   ├── <system>_commits.csv     # Raw mined commit data per system
│   └── <system>_analysis/       # Per-system analysis output
│       ├── temporal_trends.csv
│       ├── category_distribution.csv
│       └── churn_analysis.txt
├── repos/                       # Cloned source repositories (shallow, 2020–2025)
│   ├── clickhouse/
│   ├── rocksdb/
│   ├── envoy/
│   ├── kudu/
│   └── scylladb/
├── count_logs.ps1               # PowerShell: count log statements in a repo
├── count_log_levels.ps1         # PowerShell: count by log level
├── run_all_analysis.ps1         # Run full analysis pipeline for all systems
└── README.md
```

---

## Prerequisites

- Python 3.8+
- Git (accessible on `PATH`)
- PowerShell 5+ (for `.ps1` scripts on Windows)

No external Python packages are required — the scripts use only the standard library.

---

## Running the Analysis

### Step 1 — Mine commits from a repository

```bash
python scripts/extract_log_commits.py repos/<system> results/<system>_commits.csv
```

### Step 2 — Analyze the mined data

```bash
python scripts/analyze_evolution.py results/<system>_commits.csv results/<system>_analysis
```

This produces three output files in the specified directory:

| File | Contents |
|------|----------|
| `temporal_trends.csv` | Monthly statistics (commits, logs added/removed/modified, net change) |
| `category_distribution.csv` | Commit category breakdown (bug fix, feature, refactor, logging improvement) |
| `churn_analysis.txt` | Churn rate and net change metrics |

### Run all systems at once (Windows)

```powershell
./run_all_analysis.ps1
```

--- -->

## Key Results

### RQ1 — Current Logging Practices

**Log Statement Counts and Density:**

| System | Total Logs | Logs/KLOC | ERROR | INFO | WARN | DEBUG | Other |
|--------|-----------|-----------|-------|------|------|-------|-------|
| ClickHouse | 8,863 | 7.39 | 358 | 903 | 606 | 1,172 | 5,824 |
| RocksDB | 1,013 | 4.05 | 120 | 338 | 186 | 40 | 329 |
| Envoy | 3,082 | 7.71 | 584 | 356 | 359 | 2,068 | — |
| Kudu | 3,369 | 11.23 | 214 | 1,320 | 363 | 0 | 1,472 |
| ScyllaDB | 2,625 | 17.50 | 187 | 578 | 389 | 991 | 480 |

**Key findings:**
- Logging density ranges from 4.05 to 17.50 Logs/KLOC — comparable to Yuan et al. (2012) findings from a decade ago
- Each system uses a completely different logging framework — no C++ logging standard exists
- RocksDB employs unique domain-specific levels: `ROCKS_LOG_HEADER` (219) and `ROCKS_LOG_BUFFER` (92)

### RQ2 — Logging Evolution (2020–2025)

| System | Commits | Bug Fix % | Feature % | Refactor % | Log Imp. % | Net Growth |
|--------|---------|-----------|-----------|------------|------------|------------|
| ClickHouse | 26,373 | 30.5% | 14.8% | 4.0% | 3.3% | +4,515 |
| RocksDB | 4,101 | 20.2% | 22.1% | 4.4% | 1.9% | +1,144 |
| Envoy | 4,276 | 14.0% | 33.2% | 5.3% | 3.5% | +3,783 |
| Kudu | 720 | 14.9% | 22.2% | 3.9% | 2.2% | +571 |
| ScyllaDB | 4,299 | 9.3% | 21.9% | 3.0% | 2.4% | −1 |

**Key findings:**
- ClickHouse added +4,515 net log statements while ScyllaDB changed by only −1 — a **4,500× difference**
- Only 1.9–3.5% of commits are dedicated logging improvements; most logging changes are reactive (within bug fixes or features)
- ClickHouse's logging growth has accelerated over time, with 2025 showing the highest annual net additions

### RQ3 — Cross-System Comparison

**Key findings:**
- **The ScyllaDB Paradox:** Highest logging density (17.50 Logs/KLOC) yet zero evolution, suggesting logging maturity before 2020
- **Domain-specific profiles emerge:**
  - Analytical DBs (ClickHouse): high growth + high bug-fix rate
  - Service meshes (Envoy): high growth driven by feature additions
  - Storage engines (RocksDB): low density + specialized log categories
  - Distributed DBs (Kudu): moderate, declining activity
- Comparison with Yuan et al. (2012) confirms logging density is stable over a decade, but evolution patterns diverge dramatically

---

## Comparison with Prior Work

| Dimension | Yuan et al. (2012) | This Study |
|-----------|-------------------|------------|
| Systems | 4 C/C++ (httpd, OpenSSH, PostgreSQL, Squid) | 5 C++ (ClickHouse, RocksDB, Envoy, Kudu, ScyllaDB) |
| Language era | Pre-C++11 | C++11/14/17/20 |
| Total LOC | 1.1M | 2.3M |
| Log density | ~1 log line per 30 LOC | 4.05–17.50 Logs/KLOC |
| Cross-system variation | Not studied | 4,500× evolution gap |

---

## Known Issues

- **Unicode encoding errors:** Some commits with non-English characters may be skipped during git mining (affects <1% of commits).
- **Large repositories:** ClickHouse analysis may take 6–8 hours due to repository size (80,000+ commits).
- **Windows path length limits:** Some ClickHouse test directories have paths >260 chars. Scripts include `-ErrorAction SilentlyContinue` to handle this.

---
<!-- 
## References

1. Yuan, D., Park, S., & Zhou, Y. (2012). Characterizing logging practices in open-source software. *ICSE '12*, pp. 102–112.
2. Chen, B. & Jiang, Z. M. (2017). Characterizing logging practices in Java-based open source software projects. *Empirical Software Engineering*, 22(1), 330–374.
3. Fu, Q. et al. (2014). Where do developers log? An empirical study on logging practices in industry. *ICSE '14 Companion*, pp. 24–33.
4. He, S. et al. (2021). A survey on automated log analysis for reliability engineering. *ACM Computing Surveys*, 54(6), 1–37.
5. Shang, W., Nagappan, M., & Hassan, A. E. (2015). Studying the relationship between logging characteristics and the code quality of platform software. *Empirical Software Engineering*, 20(1), 1–27.

--- -->

## License

This project is for academic purposes as part of a graduate capstone requirement at Rochester Institute of Technology.

---

## Acknowledgments

- **Advisor:** Dr. Yiming Tang for guidance and feedback throughout this project
- **Open Source Communities:** Apache Kudu, ClickHouse, RocksDB, Envoy, and ScyllaDB for maintaining the distributed systems that made this research possible