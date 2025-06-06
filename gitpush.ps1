param(
    [Parameter(Mandatory=$true)]
    [string]$CommitMessage
)

# Show current status
git status

# Add all changes
git add .

# Commit with message
git commit -m $CommitMessage

# Pull latest changes
git pull origin main

# Push changes
git push origin main

Write-Host "Changes pushed successfully!" -ForegroundColor Green
