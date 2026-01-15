# Database Setup Script for Windows
# Make sure MySQL is in your PATH or specify the full path below

$mysqlPath = "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
$sqlFile = "F:\timetablesystem1\database\setup.sql"

# Check if MySQL exists
if (-not (Test-Path $mysqlPath)) {
    Write-Host "MySQL not found at: $mysqlPath"
    Write-Host "Trying to find MySQL in PATH..."
    $mysqlPath = "mysql"
}

Write-Host "Setting up database..."
Write-Host "========================================"

try {
    # Run MySQL with the SQL file
    & $mysqlPath -u root -pnazila < $sqlFile
    
    if ($?) {
        Write-Host "========================================"
        Write-Host "✓ Database setup completed successfully!"
        Write-Host ""
        Write-Host "You can now:"
        Write-Host "1. Refresh your dashboard at http://127.0.0.1:5000/dashboard"
        Write-Host "2. Login with: admin / admin"
        Write-Host "3. The dashboard cards should now load with data"
    } else {
        Write-Host "✗ Error running SQL file"
    }
}
catch {
    Write-Host "✗ Error: $_"
    Write-Host "Make sure MySQL is installed and in your PATH"
}
