BASE_URL = https://open-ortho.org/lectures/

.PHONY: qrcodes diagrams

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
	@if ! command -v npm > /dev/null 2>&1; then \
		echo "Error: npm is not installed."; \
		echo "Install Node.js 20+ and npm to render diagrams."; \
		exit 1; \
	fi
	@npm run diagrams
