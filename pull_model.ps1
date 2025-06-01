#!/usr/bin/env pwsh

param(
    [Parameter(Mandatory=$true, Position=0, HelpMessage="Model name to pull (e.g., llava:7b)")]
    [string]$ModelName
)

# Check if model argument is provided (additional validation)
if ([string]::IsNullOrWhiteSpace($ModelName)) {
    Write-Host "Error: Model name must be provided" -ForegroundColor Red
    Write-Host "Example usage: .\pull_model.ps1 llava:7b" -ForegroundColor Yellow
    exit 1
}

Write-Host "Pulling model: $ModelName" -ForegroundColor Green

try {
    # Connect to the existing "ollama" container and pull the specified model
    $result = & docker exec ollama ollama pull $ModelName
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Successfully pulled model: $ModelName" -ForegroundColor Green
    } else {
        Write-Host "Failed to pull model: $ModelName" -ForegroundColor Red
        Write-Host "Exit code: $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
} catch {
    Write-Host "Error executing docker command: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Make sure Docker is running and the 'ollama' container exists." -ForegroundColor Yellow
    exit 1
} 