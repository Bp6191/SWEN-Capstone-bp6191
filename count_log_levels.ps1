# Count log levels for all systems
cd C:\Bharathi\RIT\SWEN-Capstone-bp6191\repos

$results = @()

# RocksDB
Write-Host "`nCounting RocksDB log levels..." -ForegroundColor Green
cd rocksdb
$error = (Get-ChildItem -Recurse -Include *.cc,*.cpp,*.h | Select-String -Pattern "LOG\(ERROR").Count
$info = (Get-ChildItem -Recurse -Include *.cc,*.cpp,*.h | Select-String -Pattern "LOG\(INFO").Count
$warn = (Get-ChildItem -Recurse -Include *.cc,*.cpp,*.h | Select-String -Pattern "LOG\(WARN").Count
$debug = (Get-ChildItem -Recurse -Include *.cc,*.cpp,*.h | Select-String -Pattern "LOG\(DEBUG").Count
$results += [PSCustomObject]@{System="RocksDB"; ERROR=$error; INFO=$info; WARN=$warn; DEBUG=$debug}

# ClickHouse
Write-Host "Counting ClickHouse log levels..." -ForegroundColor Green
cd ..\clickhouse
$error = (Get-ChildItem -Recurse -Include *.cpp,*.h | Select-String -Pattern "LOG_ERROR").Count
$info = (Get-ChildItem -Recurse -Include *.cpp,*.h | Select-String -Pattern "LOG_INFO").Count
$warn = (Get-ChildItem -Recurse -Include *.cpp,*.h | Select-String -Pattern "LOG_WARNING").Count
$debug = (Get-ChildItem -Recurse -Include *.cpp,*.h | Select-String -Pattern "LOG_DEBUG").Count
$results += [PSCustomObject]@{System="ClickHouse"; ERROR=$error; INFO=$info; WARN=$warn; DEBUG=$debug}

# Envoy
Write-Host "Counting Envoy log levels..." -ForegroundColor Green
cd ..\envoy
$error = (Get-ChildItem -Recurse -Include *.cc,*.h | Select-String -Pattern "ENVOY_LOG.*error").Count
$info = (Get-ChildItem -Recurse -Include *.cc,*.h | Select-String -Pattern "ENVOY_LOG.*info").Count
$warn = (Get-ChildItem -Recurse -Include *.cc,*.h | Select-String -Pattern "ENVOY_LOG.*warn").Count
$debug = (Get-ChildItem -Recurse -Include *.cc,*.h | Select-String -Pattern "ENVOY_LOG.*debug").Count
$results += [PSCustomObject]@{System="Envoy"; ERROR=$error; INFO=$info; WARN=$warn; DEBUG=$debug}

# Kudu
Write-Host "Counting Kudu log levels..." -ForegroundColor Green
cd ..\kudu
$error = (Get-ChildItem -Recurse -Include *.cc,*.h | Select-String -Pattern "LOG\(ERROR").Count
$info = (Get-ChildItem -Recurse -Include *.cc,*.h | Select-String -Pattern "LOG\(INFO").Count
$warn = (Get-ChildItem -Recurse -Include *.cc,*.h | Select-String -Pattern "LOG\(WARNING").Count
$debug = (Get-ChildItem -Recurse -Include *.cc,*.h | Select-String -Pattern "LOG\(DEBUG").Count
$results += [PSCustomObject]@{System="Kudu"; ERROR=$error; INFO=$info; WARN=$warn; DEBUG=$debug}

# ScyllaDB
Write-Host "Counting ScyllaDB log levels..." -ForegroundColor Green
cd ..\scylladb
$error = (Get-ChildItem -Recurse -Include *.cc,*.hh | Select-String -Pattern "logger\.error").Count
$info = (Get-ChildItem -Recurse -Include *.cc,*.hh | Select-String -Pattern "logger\.info").Count
$warn = (Get-ChildItem -Recurse -Include *.cc,*.hh | Select-String -Pattern "logger\.warn").Count
$debug = (Get-ChildItem -Recurse -Include *.cc,*.hh | Select-String -Pattern "logger\.debug").Count
$results += [PSCustomObject]@{System="ScyllaDB"; ERROR=$error; INFO=$info; WARN=$warn; DEBUG=$debug}

cd ..\..

# Display and save
Write-Host "`n=== RESULTS ===" -ForegroundColor Yellow
$results | Format-Table
$results | Export-Csv -Path results\rq1_log_levels.csv -NoTypeInformation

Write-Host "`nSaved to results\rq1_log_levels.csv" -ForegroundColor Green