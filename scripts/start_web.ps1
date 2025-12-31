# Start Web Interface
# Run this to start the SQL Analyst web interface

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "                    SQL ANALYST AGENT - WEB INTERFACE" -ForegroundColor Yellow
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting server..." -ForegroundColor Green
Write-Host ""
Write-Host "Once started, open your browser and visit:" -ForegroundColor Cyan
Write-Host "  http://localhost:8000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Magenta
Write-Host ""

# Run the server
python app.py
