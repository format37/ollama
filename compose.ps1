#!/usr/bin/env pwsh

param(
    [Parameter(Mandatory=$true, Position=0)]
    [ValidateSet("up", "down", "restart", "build", "pull", "ps", "stop", "start")]
    [string]$Command,
    
    [Parameter(Mandatory=$false)]
    [switch]$Detached,
    
    [Parameter(Mandatory=$false)]
    [switch]$Build,
    
    [Parameter(Mandatory=$false)]
    [switch]$Force
)

Write-Host "Running docker compose $Command..." -ForegroundColor Green

try {
    switch ($Command) {
        "up" {
            $args = @("docker", "compose", "up")
            if ($Detached) { $args += "-d" }
            if ($Build) { $args += "--build" }
            & $args[0] $args[1..($args.Length-1)]
        }
        "down" {
            $args = @("docker", "compose", "down")
            if ($Force) { $args += "--remove-orphans" }
            & $args[0] $args[1..($args.Length-1)]
        }
        "restart" {
            & docker compose restart
        }
        "build" {
            & docker compose build
        }
        "pull" {
            & docker compose pull
        }
        "ps" {
            & docker compose ps
        }
        "stop" {
            & docker compose stop
        }
        "start" {
            & docker compose start
        }
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Command completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "Command failed with exit code: $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
} catch {
    Write-Host "Error executing command: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} 