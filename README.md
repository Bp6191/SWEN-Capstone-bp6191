# Capstone Project: Logging Practices in C++ Distributed Systems

## Quick Start

### 1. Send Response Email
- Open `response_email.txt`
- Copy and send to Dr. Tang today

### 2. Compile LaTeX Document
- Upload `methodology_revised.tex` to Overleaf
- Compile to PDF
- Send to advisor by Friday

### 3. Run Git Mining Analysis
```bash
python scripts/analyze_evolution.py results/clickhouse_commits.csv results/clickhouse_analysis
```

**Output Files:**
- `temporal_trends.csv` - Monthly statistics (commits, logs added/removed)
- `category_distribution.csv` - Commit category breakdown
- `churn_analysis.txt` - Churn rate and net change metrics

--
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
