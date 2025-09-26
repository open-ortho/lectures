BASE_URL = https://open-ortho.org/lectures/

.PHONY: qrcodes

qrcodes:
	find slides/ -name index.html -exec dirname {} \; | while read dir; do \
		rel_path=$${dir#slides/}; \
		url="${BASE_URL}slides/$${rel_path}"; \
		echo "Generating QR code for URL: $${url}"; \
		qrencode -t SVG -o "$${dir}/url_qrcode.svg" "$${url}"; \
	done