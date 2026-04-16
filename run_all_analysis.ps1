# MASTER SCRIPT - Run all RQ1 and RQ2 analysis
# Run time: 4-6 hours total

cd C:\Bharathi\RIT\SWEN-Capstone-bp6191

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   RUNNING COMPLETE RQ1 + RQ2 ANALYSIS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# ============================================
# PART 1: RQ2 - TEMPORAL EVOLUTION ANALYSIS
# ============================================

Write-Host "`n[1/3] Running RQ2 temporal analysis..." -ForegroundColor Yellow
Write-Host "This will take 30-60 minutes`n" -ForegroundColor Gray

# Create analysis directories
New-Item -ItemType Directory -Force -Path "results\rocksdb_analysis" | Out-Null
New-Item -ItemType Directory -Force -Path "results\clickhouse_analysis" | Out-Null
New-Item -ItemType Directory -Force -Path "results\envoy_analysis" | Out-Null
New-Item -ItemType Directory -Force -Path "results\kudu_analysis" | Out-Null

# Run temporal analysis
Write-Host "Analyzing RocksDB..." -ForegroundColor Green
python scripts\analyze_evolution.py results\rocksdb_commits.csv results\rocksdb_analysis

Write-Host "Analyzing ClickHouse..." -ForegroundColor Green
python scripts\analyze_evolution.py results\clickhouse_commits.csv results\clickhouse_analysis

Write-Host "Analyzing Envoy..." -ForegroundColor Green
python scripts\analyze_evolution.py results\envoy_commits.csv results\envoy_analysis

Write-Host "Analyzing Kudu..." -ForegroundColor Green
python scripts\analyze_evolution.py results\kudu_commits.csv results\kudu_analysis

Write-Host "RQ2 temporal analysis complete!`n" -ForegroundColor Green

# ============================================
# PART 2: RQ1 - COUNT CURRENT LOGS
# ============================================

Write-Host "`n[2/3] Counting current log statements..." -ForegroundColor Yellow
Write-Host "This will take 2-3 hours`n" -ForegroundColor Gray

.\count_logs.ps1

Write-Host "Log counting complete!`n" -ForegroundColor Green

# ============================================
# PART 3: RQ1 - COUNT LOG LEVELS
# ============================================

Write-Host "`n[3/3] Counting log levels..." -ForegroundColor Yellow
Write-Host "This will take 2-3 hours`n" -ForegroundColor Gray

.\count_log_levels.ps1

Write-Host "Log level counting complete!`n" -ForegroundColor Green

# ============================================
# SUMMARY
# ============================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   ANALYSIS COMPLETE!" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Files created:" -ForegroundColor Yellow
Write-Host "  - results\rocksdb_analysis\*.csv" -ForegroundColor Green
Write-Host "  - results\clickhouse_analysis\*.csv" -ForegroundColor Green
Write-Host "  - results\envoy_analysis\*.csv" -ForegroundColor Green
Write-Host "  - results\kudu_analysis\*.csv" -ForegroundColor Green
Write-Host "  - results\rq1_log_counts.csv" -ForegroundColor Green
Write-Host "  - results\rq1_log_levels.csv" -ForegroundColor Green

Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "  1. Open Excel and import the CSV files" -ForegroundColor White
Write-Host "  2. Create visualizations (charts)" -ForegroundColor White
Write-Host "  3. Calculate logging density" -ForegroundColor White
Write-Host "  4. Write results section" -ForegroundColor White

Write-Host "`nDone!`n" -ForegroundColor Green