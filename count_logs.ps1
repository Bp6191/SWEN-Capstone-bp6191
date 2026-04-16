# Count current logging statements in all systems
cd C:\Bharathi\RIT\SWEN-Capstone-bp6191\repos

$results = @()

# RocksDB
Write-Host "`nCounting RocksDB logs..." -ForegroundColor Green
cd rocksdb
$total = (Get-ChildItem -Recurse -Include *.cc,*.cpp,*.h | Select-String -Pattern "LOG\(").Count
$results += [PSCustomObject]@{System="RocksDB"; TotalLogs=$total}

# ClickHouse
Write-Host "Counting ClickHouse logs..." -ForegroundColor Green
cd ..\clickhouse
$total = (Get-ChildItem -Recurse -Include *.cpp,*.h | Select-String -Pattern "LOG_").Count
$results += [PSCustomObject]@{System="ClickHouse"; TotalLogs=$total}

# Envoy
Write-Host "Counting Envoy logs..." -ForegroundColor Green
cd ..\envoy
$total = (Get-ChildItem -Recurse -Include *.cc,*.h | Select-String -Pattern "ENVOY_LOG\(").Count
$results += [PSCustomObject]@{System="Envoy"; TotalLogs=$total}

# Kudu
Write-Host "Counting Kudu logs..." -ForegroundColor Green
cd ..\kudu
$total = (Get-ChildItem -Recurse -Include *.cc,*.h | Select-String -Pattern "LOG\(").Count
$results += [PSCustomObject]@{System="Kudu"; TotalLogs=$total}

# ScyllaDB
Write-Host "Counting ScyllaDB logs..." -ForegroundColor Green
cd ..\scylladb
$total = (Get-ChildItem -Recurse -Include *.cc,*.hh | Select-String -Pattern "logger\.").Count
$results += [PSCustomObject]@{System="ScyllaDB"; TotalLogs=$total}

cd ..\..

# Display and save results
Write-Host "`n=== RESULTS ===" -ForegroundColor Yellow
$results | Format-Table
$results | Export-Csv -Path results\rq1_log_counts.csv -NoTypeInformation

Write-Host "`nSaved to results\rq1_log_counts.csv" -ForegroundColor Green