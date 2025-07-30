#!/bin/bash

# Script to automatically run all .sh files in the Linear_reg_script folder

# Set the base directory (relative to the current script location)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LINEAR_REG_SCRIPT_DIR="$SCRIPT_DIR/../baseline_performance/Linear_reg_script"

# Check if the Linear_reg_script directory exists
if [ ! -d "$LINEAR_REG_SCRIPT_DIR" ]; then
    echo "Error: Linear_reg_script directory not found at $LINEAR_REG_SCRIPT_DIR"
    exit 1
fi

echo "Starting automatic execution of linear regression scripts..."
echo "Script directory: $LINEAR_REG_SCRIPT_DIR"
echo "=================================================="

# Change to the Linear_reg_script directory
cd "$LINEAR_REG_SCRIPT_DIR" || exit 1

# Counter for tracking progress
count=0
total_scripts=$(find . -name "*.sh" -type f | wc -l)

echo "Found $total_scripts shell scripts to execute"
echo ""

# Find and execute all .sh files in the directory
for script in *.sh; do
    if [ -f "$script" ]; then
        count=$((count + 1))
        echo "[$count/$total_scripts] Executing: $script"
        echo "----------------------------------------"
        
        # Make sure the script is executable
        chmod +x "$script"
        
        # Execute the script and capture its exit status
        if bash "$script"; then
            echo "✅ $script completed successfully"
        else
            echo "❌ $script failed with exit code $?"
            echo "Continuing with next script..."
        fi
        
        echo ""
        echo "=================================================="
        echo ""
    fi
done

echo "Execution completed!"
echo "Total scripts processed: $count"