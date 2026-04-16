# Capstone Project: Logging Practices in C++ Distributed Systems

### 2. Compile LaTeX Document
- Upload `methodology_revised.tex` to Overleaf
- Compile to PDF
- Send to advisor by Friday

### 3. Run Git Mining Analysis
```bash
# Install Python 3
# Clone repositories and run analysis
chmod +x run_analysis.sh
./run_analysis.sh
```

This will:
- Clone all 5 systems
- Extract logging commits
- Analyze evolution trends
- Generate CSV files and statistics

### 4. Review Results

Results will be in `./results/` directory:
- `{system}_commits.csv` - All logging commits
- `{system}_analysis/temporal_trends.csv` - Monthly statistics
- `{system}_analysis/category_distribution.csv` - Commit categories
- `{system}_analysis/churn_analysis.txt` - Churn metrics

## Timeline

- **Week 1 (NOW)**: Send email, finalize systems
- **Week 2**: Run git mining, collect data
- **Week 3-4**: Static analysis (RQ1)
- **Week 5-6**: Evolution analysis (RQ2)
- **Week 7-8**: Cross-system comparison (RQ3)
- **Week 9-10**: Writing
- **Week 11-12**: Revision, presentation

## Questions for Advisor

1. Analyze entire git history or last 5 years?
2. Incorporate smells into evolution study?
3. Minimum star count for system selection?