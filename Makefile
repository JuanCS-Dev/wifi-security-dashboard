# Makefile for WiFi Security Education Dashboard
# Provides convenient shortcuts for common tasks
#
# Author: Juan-Dev - Soli Deo Gloria ✝️
# Date: 2025-11-10

.PHONY: help install test test-unit test-manual coverage validate metrics run run-real clean

help:  ## Show this help message
	@echo "WiFi Security Education Dashboard v2.0"
	@echo "======================================="
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install all dependencies
	@echo "Installing dependencies..."
	pip3 install -r requirements-v2.txt
	@echo "✓ Done"

test:  ## Run all tests (unit + manual)
	@echo "Running all tests..."
	python3 -m pytest tests/ -v
	@echo "Running manual tests..."
	python3 tests/manual/test_mock_mode_manual.py
	python3 tests/manual/test_real_mode_manual.py
	python3 tests/manual/test_consistency_performance.py

test-unit:  ## Run unit tests only
	python3 -m pytest tests/unit/ -v

test-manual:  ## Run manual tests only
	python3 tests/manual/test_mock_mode_manual.py
	python3 tests/manual/test_real_mode_manual.py
	python3 tests/manual/test_consistency_performance.py

coverage:  ## Run tests with coverage report
	python3 -m pytest tests/unit/ --cov=src --cov-report=term-missing --cov-report=html
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

validate:  ## Validate Constituição Vértice v3.0 compliance
	@echo "Validating P1-P6 principles..."
	python3 tools/validate_constitution.py

metrics:  ## Calculate LEI, FPC, Coverage, CRS metrics
	@echo "Calculating metrics..."
	python3 tools/calculate_metrics.py

run:  ## Run dashboard in mock mode (default)
	python3 main_v2.py

run-real:  ## Run dashboard in real mode (requires root)
	@echo "⚠️  Running in REAL mode (requires root)"
	sudo python3 main_v2.py --real

check-deps:  ## Check all dependencies
	@bash scripts/check_dependencies.sh

clean:  ## Clean temporary files
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name htmlcov -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	@echo "✓ Cleaned"

setup:  ## Quick setup (install + verify)
	@bash scripts/setup.sh
