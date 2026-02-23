BASE_URL = https://open-ortho.org/lectures/
DIAGRAMS_BACKGROUND = white
DIAGRAMS_THEME = default

.PHONY: help qrcodes diagrams serve clean

default: help

help:
	@echo "Available targets:"
	@echo "  help      Show this help message"
	@echo "  serve     Run the local dev server"
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

diagrams:
	@set -e; \
	if ! command -v mmdc > /dev/null 2>&1 && ! command -v npx > /dev/null 2>&1; then \
		echo "Error: mmdc or npx is not installed."; \
		echo "Install mermaid-cli (mmdc) or Node.js 20+ with npm."; \
		exit 1; \
	fi; \
	if [ -z "$$PUPPETEER_EXECUTABLE_PATH" ]; then \
		for candidate in \
			"/Applications/Chromium.app/Contents/MacOS/Chromium" \
			"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
			"$$HOME/Applications/Chromium.app/Contents/MacOS/Chromium" \
			"$$HOME/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
			"/opt/homebrew/bin/chromium" \
			"/usr/local/bin/chromium" \
			"/usr/bin/chromium"; do \
			if [ -x "$$candidate" ]; then \
				export PUPPETEER_EXECUTABLE_PATH="$$candidate"; \
				break; \
			fi; \
		done; \
	fi; \
	if [ -z "$$PUPPETEER_EXECUTABLE_PATH" ]; then \
		echo "Error: PUPPETEER_EXECUTABLE_PATH is not set and no Chrome/Chromium was found."; \
		echo "Install Chrome/Chromium or set PUPPETEER_EXECUTABLE_PATH to the browser binary."; \
		exit 1; \
	fi; \
	mkdir -p assets/generated/diagrams; \
	if ! ls assets/diagrams/*.mmd > /dev/null 2>&1; then \
		echo "No Mermaid diagrams found in assets/diagrams."; \
		exit 0; \
	fi; \
	for file in assets/diagrams/*.mmd; do \
		base=$$(basename "$$file" .mmd); \
		out="assets/generated/diagrams/$${base}.svg"; \
		if command -v mmdc > /dev/null 2>&1; then \
			mmdc -i "$$file" -o "$$out" -b "$(DIAGRAMS_BACKGROUND)" -t "$(DIAGRAMS_THEME)"; \
		else \
			npx mmdc -i "$$file" -o "$$out" -b "$(DIAGRAMS_BACKGROUND)" -t "$(DIAGRAMS_THEME)"; \
		fi; \
	done

clean:
	@rm -rf assets/generated/diagrams

serve:
	@python3 serve.py
