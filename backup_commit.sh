#!/bin/bash

# Create a timestamped backup copy outside your repository
cp -r . ../FQ_backup_$(date +%Y%m%d_%H%M%S)

# Check git status, stage, commit, and push
git status
git add .
git commit -m "Backup workspace before restoring modern CustomTkinter UI"
git push
