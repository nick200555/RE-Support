#!/bin/bash
# frappe_preflight.sh

APP_NAME=$(basename "$(pwd)")
MODULE_ROOT="./$APP_NAME"
FAILURES=0

echo "🔍 Starting Pre-Flight Checks for Frappe App: $APP_NAME"

# 1. Structural File Checks
echo "-----------------------------------"
if [ ! -f "$MODULE_ROOT/hooks.py" ]; then
    echo "❌ Missing core: $MODULE_ROOT/hooks.py"
    FAILURES=$((FAILURES+1))
else
    echo "✅ Core hooks.py detected"
fi

if [ ! -f "$MODULE_ROOT/modules.txt" ]; then
    echo "❌ Missing dependencies list: $MODULE_ROOT/modules.txt"
    FAILURES=$((FAILURES+1))
else
    echo "✅ modules.txt detected"
fi

# 2. Package Verification
echo "-----------------------------------"
MISSING_INITS=$(find $MODULE_ROOT -type d \
    -not -name "__pycache__" \
    -not -path "*/public*" \
    -not -path "*/www*" \
    -not -path "*/templates*" \
    -exec sh -c '[ ! -f "$1/__init__.py" ] && echo "$1"' _ {} \; || true)

if [ -n "$MISSING_INITS" ]; then
    echo "❌ Missing __init__.py files in:"
    echo "$MISSING_INITS"
    echo "💡 Fixing instantly..."
    find $MODULE_ROOT -type d \
        -not -name "__pycache__" \
        -not -path "*/public*" \
        -not -path "*/www*" \
        -not -path "*/templates*" \
        -exec sh -c '[ ! -f "$1/__init__.py" ] && touch "$1/__init__.py"' _ {} \;
    echo "✅ Fixed automatically!"
else
    echo "✅ Namespace package integrity verified (All __init__.py files valid)"
fi

# 3. Final Analysis
echo "-----------------------------------"
if [ $FAILURES -gt 0 ]; then
    echo "⚠️  App currently has $FAILURES architectural faults. 'bench install-app' will likely fail."
    exit 1
else
    echo "🚀 Pre-flight checks passed! Safe to proceed with 'bench --site <site-name> install-app $APP_NAME'."
    exit 0
fi
