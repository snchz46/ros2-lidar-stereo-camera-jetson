# Contributing Guide

Thanks for helping improve the ADMIT14 ROS 2 lab! This document explains how students can collaborate effectively and keep the documentation and codebase healthy.

## How to Propose Changes
1. **Discuss first** – Start a thread in the course chat or open a GitHub issue describing the problem or enhancement. Include screenshots/logs where relevant.
2. **Fork and branch** – Create your own fork and work from a descriptive feature branch (e.g., `feature/jetson-usb-camera`).
3. **Keep changes scoped** – Group related documentation and code updates together. Separate unrelated fixes into individual pull requests (PRs).
4. **Write a clear PR description** – Summarize what changed, why it matters for the lab workflow, and how reviewers can verify it. Reference any related issues.

## Development Environment
- Use the ROS 2 distribution recommended in the README quick-start matrix for your host platform.
- Follow the platform-specific setup instructions in `03_ros2_install.md` and `04_ros2_setup.md` before making code changes.
- When working on Jetson hardware, document any additional OS packages or firmware tweaks that differ from the baseline image.

## Linting and Tests
- **Python / ROS packages**: Run `colcon test` from the workspace root. Resolve all failing tests before opening a PR.
- **ROS formatting**: Apply `ament_uncrustify` / `ament_clang_format` if you modify C++ packages, and `ament_flake8` for Python nodes (`colcon test --packages-select <pkg>` is sufficient for lint jobs).
- **Markdown docs**: Run `markdownlint` (e.g., `npx markdownlint-cli "**/*.md"`) to catch style or heading issues. Fix all reported warnings.
- Attach the relevant command output in your PR when tests fail for reasons outside your control.

## Documenting Hardware Setups
- Every hardware-dependent change must include an update to the appropriate section in `README.md` or the platform-specific guides.
- Provide the exact hardware revision, peripheral connections, and any calibration data needed to reproduce your results.
- Add troubleshooting notes for new failure modes you encounter so future cohorts benefit from the findings.

## Pull Request Checklist
- [ ] Tests and linters pass locally (or failures are explained in the PR).
- [ ] Documentation updates accompany code changes that alter workflows or requirements.
- [ ] Screenshots/logs are attached for visual or runtime changes.
- [ ] Reviewers can reproduce the setup using the linked instructions and hardware notes.

Happy hacking, and thanks for making the ADMIT14 project better for the next cohort!
