#!/bin/bash
#
# test_wrapper.sh - Test CLI Wrapper Functionality
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }

# Test functions
test_script_executable() {
    if [[ -x "$SCRIPT_DIR/mksynth" ]]; then
        print_success "mksynth is executable"
        return 0
    else
        print_error "mksynth is not executable"
        return 1
    fi
}

test_help_output() {
    # Check if running the wrapper with no arguments produces usage
    if "$SCRIPT_DIR/mksynth" 2>&1 | head -3 | grep -q -E "(Usage|INPUT FORMATS|mksynth)"; then
        print_success "Help output works"
        return 0
    else
        print_error "Help output failed"
        return 1
    fi
}

test_virtual_env() {
    if [[ -d "$SCRIPT_DIR/media_knowledge_env" ]]; then
        print_success "Virtual environment exists"
        return 0
    else
        print_error "Virtual environment not found"
        print_error "Run: python -m venv media_knowledge_env"
        return 1
    fi
}

test_installation_script() {
    if [[ -x "$SCRIPT_DIR/install.sh" ]]; then
        print_success "Install script is executable"
        return 0
    else
        print_error "Install script is not executable"
        return 1
    fi
}

test_uninstallation_script() {
    if [[ -x "$SCRIPT_DIR/uninstall.sh" ]]; then
        print_success "Uninstall script is executable"
        return 0
    else
        print_error "Uninstall script is not executable"
        return 1
    fi
}

# Run tests
echo "Testing CLI Wrapper Components..."
echo "=================================="

failed_tests=0

test_script_executable || ((failed_tests++))
test_help_output || ((failed_tests++))
test_virtual_env || ((failed_tests++))
test_installation_script || ((failed_tests++))
test_uninstallation_script || ((failed_tests++))

echo "=================================="
if [[ $failed_tests -eq 0 ]]; then
    print_success "All tests passed! CLI wrapper is ready."
    echo
    echo "Next steps:"
    echo "1. Run ./install.sh to install aliases"
    echo "2. Source your shell config: source ~/.zshrc (or ~/.bashrc)"
    echo "3. Test: mksynth --help"
else
    print_error "$failed_tests test(s) failed"
    exit 1
fi