#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Jetson Nano ROS 2 Foxy bootstrap script
# This script installs OS prerequisites, ROS 2 Foxy, and configures the shell
# environment with logging and idempotency checks.
###############################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR=${LOG_DIR:-"$SCRIPT_DIR/logs"}
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/jetson_install_$(date +%Y%m%d_%H%M%S).log"

# Redirect all output to both stdout and the log file.
exec > >(tee -a "$LOG_FILE") 2>&1

log() {
  local level=$1
  shift
  printf '[%s] [%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$level" "$*"
}

on_error() {
  log "ERROR" "Installation failed at line $1. Check $LOG_FILE for details."
}

trap 'on_error $LINENO' ERR

require_root() {
  if [[ $EUID -ne 0 ]]; then
    log "ERROR" "This script must be run as root. Use sudo or log in as root."
    exit 1
  fi
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

is_package_installed() {
  dpkg -s "$1" >/dev/null 2>&1
}

install_packages() {
  local packages_to_install=()
  for pkg in "$@"; do
    if is_package_installed "$pkg"; then
      log "INFO" "Package '$pkg' already installed. Skipping."
    else
      packages_to_install+=("$pkg")
    fi
  done

  if (( ${#packages_to_install[@]} > 0 )); then
    log "INFO" "Installing packages: ${packages_to_install[*]}"
    apt-get install -y "${packages_to_install[@]}"
  else
    log "INFO" "All requested packages are already installed."
  fi
}

confirm_proceed() {
  if [[ ${ASSUME_YES:-false} == "true" ]]; then
    log "INFO" "ASSUME_YES=true detected. Skipping confirmation prompt."
    return
  fi

  echo "This script will install ROS 2 Foxy and modify system configuration."
  read -rp "Continue? [y/N]: " response
  case "${response,,}" in
    y|yes)
      log "INFO" "User confirmed to continue."
      ;;
    *)
      log "INFO" "Installation aborted by user."
      exit 0
      ;;
  esac
}

check_architecture() {
  local arch
  arch=$(uname -m)
  if [[ $arch != "aarch64" ]]; then
    log "WARNING" "This script was designed for Jetson Nano (aarch64). Current architecture: $arch."
  else
    log "INFO" "Detected aarch64 architecture."
  fi
}

ensure_locale() {
  local target_locale=${ROS2_LOCALE:-en_US.UTF-8}
  if locale -a | grep -q "^${target_locale}$"; then
    log "INFO" "Locale ${target_locale} already generated."
  else
    log "INFO" "Generating locale ${target_locale}."
    locale-gen "$target_locale"
  fi

  log "INFO" "Setting default locale to ${target_locale}."
  update-locale LC_ALL="$target_locale" LANG="$target_locale"
}

add_ros2_apt_repository() {
  local keyring="/usr/share/keyrings/ros-archive-keyring.gpg"
  local repo_file="/etc/apt/sources.list.d/ros2.list"

  if [[ ! -f $keyring ]]; then
    log "INFO" "Adding ROS 2 GPG key to $keyring."
    mkdir -p "$(dirname "$keyring")"
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
      | gpg --dearmor > "$keyring"
    chmod 644 "$keyring"
  else
    log "INFO" "ROS 2 GPG key already present at $keyring."
  fi

  local ubuntu_codename
  ubuntu_codename=$(lsb_release -cs)
  if [[ $ubuntu_codename != "focal" ]]; then
    log "WARNING" "ROS 2 Foxy targets Ubuntu 20.04 (focal). Detected: $ubuntu_codename."
  fi

  if [[ ! -f $repo_file ]]; then
    log "INFO" "Adding ROS 2 apt repository to $repo_file."
    echo "deb [arch=amd64,arm64 signed-by=$keyring] http://packages.ros.org/ros2/ubuntu $ubuntu_codename main" \
      > "$repo_file"
  elif ! grep -q "ros2/ubuntu" "$repo_file"; then
    log "INFO" "Updating ROS 2 apt repository definition in $repo_file."
    echo "deb [arch=amd64,arm64 signed-by=$keyring] http://packages.ros.org/ros2/ubuntu $ubuntu_codename main" \
      > "$repo_file"
  else
    log "INFO" "ROS 2 apt repository already configured."
  fi
}

update_package_index() {
  log "INFO" "Updating apt package index."
  apt-get update
}

install_ros2() {
  install_packages ros-foxy-desktop python3-argcomplete python3-colcon-common-extensions python3-rosdep
}

initialize_rosdep() {
  if ! command_exists rosdep; then
    log "WARNING" "rosdep command not found after installation. Skipping initialization."
    return
  fi

  if [[ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]]; then
    log "INFO" "Initializing rosdep."
    if ! rosdep init; then
      log "WARNING" "rosdep init failed. Check network connectivity or rerun later."
      return
    fi
  else
    log "INFO" "rosdep already initialized."
  fi

  local target_user
  target_user=$(determine_target_user)
  log "INFO" "Updating rosdep caches for user $target_user."
  if ! su - "$target_user" -c "rosdep update"; then
    log "WARNING" "rosdep update failed for user $target_user. You can rerun 'rosdep update' manually."
  fi
}

determine_target_user() {
  if [[ -n ${ROS2_TARGET_USER:-} ]]; then
    if id -u "$ROS2_TARGET_USER" >/dev/null 2>&1; then
      echo "$ROS2_TARGET_USER"
      return
    else
      log "WARNING" "ROS2_TARGET_USER '$ROS2_TARGET_USER' not found. Falling back to default user detection."
    fi
  fi

  if [[ -n ${SUDO_USER:-} && $SUDO_USER != "root" ]]; then
    if id -u "$SUDO_USER" >/dev/null 2>&1; then
      echo "$SUDO_USER"
      return
    fi
  fi

  if [[ -n ${USER:-} ]]; then
    if id -u "$USER" >/dev/null 2>&1; then
      echo "$USER"
      return
    fi
  fi

  echo "root"
}

append_source_to_bashrc() {
  local target_user
  target_user=$(determine_target_user)
  local user_home
  user_home=$(eval echo "~$target_user")
  local bashrc="$user_home/.bashrc"
  local source_line="source /opt/ros/foxy/setup.bash"

  if [[ ! -f $bashrc ]]; then
    log "WARNING" "No .bashrc found for user $target_user at $bashrc. Creating one."
    touch "$bashrc"
    chown "$target_user":"$target_user" "$bashrc"
  fi

  if grep -Fxq "$source_line" "$bashrc"; then
    log "INFO" "ROS 2 environment already sourced in $bashrc."
  else
    log "INFO" "Adding ROS 2 environment sourcing to $bashrc for user $target_user."
    echo "$source_line" >> "$bashrc"
    chown "$target_user":"$target_user" "$bashrc"
  fi
}

main() {
  require_root
  confirm_proceed

  if [[ ${ASSUME_YES:-false} == "true" ]]; then
    export DEBIAN_FRONTEND=noninteractive
  fi

  check_architecture
  log "INFO" "Starting Jetson Nano ROS 2 Foxy installation. Logs: $LOG_FILE"

  update_package_index
  install_packages apt-transport-https ca-certificates curl gnupg lsb-release software-properties-common build-essential locales
  ensure_locale
  update_package_index
  add_ros2_apt_repository
  update_package_index
  install_ros2
  initialize_rosdep
  append_source_to_bashrc

  log "INFO" "Jetson Nano ROS 2 Foxy installation completed successfully."
}

main "$@"
