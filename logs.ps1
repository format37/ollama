#!/usr/bin/env pwsh

param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$ContainerName = "ollama",
    
    [Parameter(Mandatory=$false)]
    [switch]$Follow,
    
    [Parameter(Mandatory=$false)]
    [int]$Tail = 50,
    
    [Parameter(Mandatory=$false)]
    [switch]$Timestamps,
    
    [Parameter(Mandatory=$false)]
    [string]$Since
)

Write-Host "Viewing logs for container: $ContainerName" -ForegroundColor Green

try {
    # Build docker logs command with options
    $args = @("docker", "logs")
    
    if ($Follow) {
        $args += "--follow"
        Write-Host "Following logs (Press Ctrl+C to stop)..." -ForegroundColor Yellow
    }
    
    if ($Tail -gt 0) {
        $args += "--tail"
        $args += $Tail.ToString()
    }
    
    if ($Timestamps) {
        $args += "--timestamps"
    }
    
    if (-not [string]::IsNullOrWhiteSpace($Since)) {
        $args += "--since"
        $args += $Since
    }
    
    $args += $ContainerName
    
    # Execute the docker logs command
    & $args[0] $args[1..($args.Length-1)]
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to retrieve logs for container: $ContainerName" -ForegroundColor Red
        Write-Host "Exit code: $LASTEXITCODE" -ForegroundColor Red
        Write-Host "Make sure the container exists and is accessible." -ForegroundColor Yellow
        exit $LASTEXITCODE
    }
} catch {
    Write-Host "Error executing docker logs command: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Make sure Docker is running and the container '$ContainerName' exists." -ForegroundColor Yellow
    exit 1
} 