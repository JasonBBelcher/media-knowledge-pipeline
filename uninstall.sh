#!/bin/bash
#
# uninstall.sh - CLI Wrapper Uninstallation Script
# Removes mksynth aliases from shell configuration
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}INFO${NC}: $1"; }
print_success() { echo -e "${GREEN}SUCCESS${NC}: $1"; }
print_warning() { echo -e "${YELLOW}WARNING${NC}: $1"; }
print_error() { echo -e "${RED}ERROR${NC}: $1"; }

# Detect shell type
detect_shell() {
    local shell_name=""
    
    if [[ -n "${ZSH_VERSION:-}" ]]; then
        shell_name="zsh"
    elif [[ -n "${BASH_VERSION:-}" ]]; then
        shell_name="bash"
    else
        # Try to detect from parent process
        local parent_shell="$(ps -p $$ -o comm=)"
        if [[ "$parent_shell" == *"zsh"* ]]; then
            shell_name="zsh"
        elif [[ "$parent_shell" == *"bash"* ]]; then
            shell_name="bash"
        else
            # Fallback to shell name
            shell_name="${SHELL##*/}"
        fi
    fi
    
    echo "$shell_name"
}

# Get shell config file path
get_shell_config() {
    local shell_type="$1"
    local config_file=""
    
    case "$shell_type" in
        zsh)
            config_file="$HOME/.zshrc"
            ;;
        bash)
            config_file="$HOME/.bashrc"
            ;;
        *)
            print_error "Unsupported shell: $shell_type"
            exit 1
            ;;
    esac
    
    echo "$config_file"
}

# Check if aliases exist
aliases_exist() {
    local config_file="$1"
    
    if [[ ! -f "$config_file" ]]; then
        return 1
    fi
    
    grep -q "alias mksynth=" "$config_file"
}

# Remove aliases from config file
remove_aliases() {
    local config_file="$1"
    
    if [[ ! -f "$config_file" ]]; then
        print_warning "Config file $config_file does not exist"
        return 0
    fi
    
    if aliases_exist "$config_file"; then
        # Create backup before removal
        local backup_file="${config_file}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$config_file" "$backup_file"
        print_info "Backed up $config_file to $backup_file"
        
        # Remove alias section using sed
        sed -i.bak '/^# Media Knowledge Synthesizer CLI Aliases/,/^alias mksynth-bug=/d' "$config_file"
        
        # Remove backup created by sed
        rm -f "${config_file}.bak"
        
        # Remove short aliases separately
        sed -i '/^alias mk=/d' "$config_file"
        sed -i '/^alias mkm=/d' "$config_file"
        sed -i '/^alias mkl=/d' "$config_file"
        
        print_success "Removed aliases from $config_file"
        
        # Clean up empty lines
        sed -i '/^$/N;/^\n$/d' "$config_file"
    else
        print_warning "No mksynth aliases found in $config_file"
    fi
}

# Show usage
show_usage() {
    cat << EOF
Uninstall Media Knowledge Synthesizer CLI Aliases

Usage: ./uninstall.sh [OPTIONS]

OPTIONS:
  -h, --help      Show this help message
  -s, --shell     Specify shell type (bash|zsh)
  --all           Remove from all supported shells

EXAMPLES:
  # Interactive uninstall
  ./uninstall.sh
  
  # Specify shell type
  ./uninstall.sh --shell zsh
  
  # Remove from all shells
  ./uninstall.sh --all

This script will:
1. Detect your shell type (bash/zsh)
2. Remove mksynth aliases from config file
3. Clean up empty lines
EOF
}

# Main uninstallation function
main() {
    local specified_shell=""
    local remove_all=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -s|--shell)
                specified_shell="$2"
                shift 2
                ;;
            --all)
                remove_all=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    print_info "Starting Media Knowledge Synthesizer CLI uninstallation"
    
    if [[ "$remove_all" == true ]]; then
        # Remove from all supported shells
        print_info "Removing aliases from all supported shells"
        
        for shell_type in "zsh" "bash"; do
            config_file=$(get_shell_config "$shell_type")
            if [[ -f "$config_file" ]]; then
                print_info "Processing $config_file"
                remove_aliases "$config_file"
            else
                print_warning "Config file $config_file does not exist"
            fi
        done
    else
        # Remove from specified shell
        local shell_type="$specified_shell"
        if [[ -z "$shell_type" ]]; then
            shell_type=$(detect_shell)
        fi
        
        print_info "Detected shell: $shell_type"
        
        local config_file
        config_file=$(get_shell_config "$shell_type")
        
        print_info "Config file: $config_file"
        
        remove_aliases "$config_file"
    fi
    
    print_success "Uninstallation completed!"
    echo
    echo "What's next:"
    echo "1. Source your shell config to apply changes"
    echo "2. Aliases will be removed from new shell sessions"
    echo "3. Existing shell sessions will need to be restarted"
    echo
    echo "To reinstall, run: ./install.sh"
}

# Run main function
main "$@"