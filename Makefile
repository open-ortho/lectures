BASE_URL = https://open-ortho.org/lectures/
DIAGRAMS_BACKGROUND = transparent
DIAGRAMS_OPTS = -b "$(DIAGRAMS_BACKGROUND)"

.PHONY: help qrcodes diagrams serve clean

default: help

help:
	@echo "Available targets:"
	@echo "  help      Show this help message"
	@echo "  serve     Run the local dev server"
	@echo "  detect-browser  Locate Chrome/Chromium for Mermaid CLI"
	@echo "  diagrams  Render Mermaid diagrams"
	@echo "  qrcodes   Generate QR codes for slides"
	@echo "  clean     Remove generated artifacts"

qrcodes:
	@if ! command -v qrencode > /dev/null 2>&1; then \
		echo "Error: qrencode is not installed."; \
		echo "Install it with:"; \
		echo "  - macOS: brew install qrencode"; \
		echo "  - Ubuntu/Debian: sudo apt install qrencode"; \
		echo "  - CentOS/RHEL: sudo yum install qrencode"; \
		echo "  - Fedora: sudo dnf install qrencode"; \
		exit 1; \
	fi
	find slides/ -name index.html -exec dirname {} \; | while read dir; do \
		rel_path=$${dir#slides/}; \
		url="${BASE_URL}slides/$${rel_path}"; \
		echo "Generating QR code for URL: $${url}"; \
		qrencode -t SVG -o "$${dir}/url_qrcode.svg" "$${url}"; \
	done

detect-browser:
	@set -e; \
	if [ -n "$$PUPPETEER_EXECUTABLE_PATH" ]; then \
		echo "$$PUPPETEER_EXECUTABLE_PATH"; \
		exit 0; \
	fi; \
	for candidate in \
		"/Applications/Chromium.app/Contents/MacOS/Chromium" \
		"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
		"$$HOME/Applications/Chromium.app/Contents/MacOS/Chromium" \
		"$$HOME/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
		"/opt/homebrew/bin/chromium" \
		"/usr/local/bin/chromium" \
		"/usr/bin/chromium"; do \
		if [ -x "$$candidate" ]; then \
			echo "$$candidate"; \
			exit 0; \
		fi; \
	done; \
	echo "Error: PUPPETEER_EXECUTABLE_PATH is not set and no Chrome/Chromium was found." 1>&2; \
	echo "Install Chrome/Chromium or set PUPPETEER_EXECUTABLE_PATH to the browser binary." 1>&2; \
	exit 1

diagrams:
	@set -e; \
	if ! command -v mmdc > /dev/null 2>&1 && ! command -v npx > /dev/null 2>&1; then \
		echo "Error: mmdc or npx is not installed."; \
		echo "Install mermaid-cli (mmdc) or Node.js 20+ with npm."; \
		exit 1; \
	fi; \
	browser=$$($(MAKE) -s --no-print-directory detect-browser 2>/dev/null || true); \
	if [ -z "$$browser" ]; then \
		echo "Error: PUPPETEER_EXECUTABLE_PATH is not set and no Chrome/Chromium was found."; \
		echo "Install Chrome/Chromium or set PUPPETEER_EXECUTABLE_PATH to the browser binary."; \
		exit 1; \
	fi; \
	export PUPPETEER_EXECUTABLE_PATH="$$browser"; \
	mkdir -p assets/generated/diagrams; \
	if ! ls assets/diagrams/*.mmd > /dev/null 2>&1; then \
		echo "No Mermaid diagrams found in assets/diagrams."; \
		exit 0; \
	fi; \
	for file in assets/diagrams/*.mmd; do \
		base=$$(basename "$$file" .mmd); \
		out="assets/generated/diagrams/$${base}.svg"; \
		if command -v mmdc > /dev/null 2>&1; then \
			mmdc -i "$$file" -o "$$out" $(DIAGRAMS_OPTS); \
		else \
			npx mmdc -i "$$file" -o "$$out" $(DIAGRAMS_OPTS); \
		fi; \
	done

clean:
	@rm -rf assets/generated/diagrams

serve:
	@python3 serve.py
