BASE_URL = https://open-ortho.org/lectures/

.PHONY: qrcodes

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