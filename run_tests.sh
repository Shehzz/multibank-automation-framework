#!/bin/bash
# Pytest wrapper that uses PARALLEL_WORKERS and MAX_RETRIES from .env

# Load .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Use PARALLEL_WORKERS if set, otherwise default to 1
WORKERS=${PARALLEL_WORKERS:-1}
RETRIES=${MAX_RETRIES:-0}

# Build pytest command
PYTEST_CMD="pytest"

# Add parallel workers if > 1
if [ "$WORKERS" -gt 1 ]; then
    echo "🚀 Running tests with $WORKERS parallel workers..."
    PYTEST_CMD="$PYTEST_CMD -n $WORKERS --dist loadscope"
else
    echo "🔄 Running tests sequentially..."
fi

# Add retry mechanism if > 0
if [ "$RETRIES" -gt 0 ]; then
    echo "🔁 Retry mechanism enabled: max $RETRIES retries on failure"
    PYTEST_CMD="$PYTEST_CMD --reruns $RETRIES --reruns-delay 1"
fi

# Run pytest with all arguments passed to script
echo "📝 Command: $PYTEST_CMD $@"
echo ""
$PYTEST_CMD "$@"
EXIT_CODE=$?

# Print summary
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed (exit code: $EXIT_CODE)"
fi

exit $EXIT_CODE