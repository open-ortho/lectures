/*
 * external.js
 * Adapted for reveal.js 4 plugin API.
 * Based on janschoepke/reveal_external (MIT).
 */
(function() {
    "use strict";

    function createPlugin() {
        let deck;
        let options;

        function getTarget(node) {
            let url = node.getAttribute("data-external") || "";
            let isReplace = false;

            if (url === "") {
                url = node.getAttribute("data-external-replace") || "";
                isReplace = true;
            }

            if (url.length > 0) {
                const r = url.match(/^([^#]+)(?:#(.+))?/);
                return {
                    url: r[1] || "",
                    fragment: r[2] || "",
                    isReplace: isReplace,
                };
            }

            return null;
        }

        function convertUrl(src, path) {
            if (path !== "" && src.indexOf(".") === 0) {
                return path + "/" + src;
            }
            return src;
        }

        function convertAttributes(attributeName, container, path) {
            const nodes = container.querySelectorAll("[" + attributeName + "]");

            if (container.getAttribute(attributeName)) {
                container.setAttribute(
                    attributeName,
                    convertUrl(container.getAttribute(attributeName), path)
                );
            }

            for (let i = 0, c = nodes.length; i < c; i++) {
                nodes[i].setAttribute(
                    attributeName,
                    convertUrl(nodes[i].getAttribute(attributeName), path)
                );
            }
        }

        function convertUrls(container, path) {
            for (let i = 0, c = options.mapAttributes.length; i < c; i++) {
                convertAttributes(options.mapAttributes[i], container, path);
            }
        }

        function updateSection(section, target, parentPath) {
            const url = parentPath !== "" ? (parentPath + "/" + target.url) : target.url;
            const xhr = new XMLHttpRequest();

            xhr.onreadystatechange = function() {
                if (xhr.readyState !== 4) {
                    return;
                }

                if ((xhr.status >= 200 && xhr.status < 300) || (xhr.status === 0 && xhr.responseText !== "")) {
                    const filePath = url.substr(0, url.lastIndexOf("/"));
                    const html = (new DOMParser()).parseFromString(xhr.responseText, "text/html");
                    const nodes = target.fragment !== ""
                        ? html.querySelectorAll(target.fragment)
                        : html.querySelector("body").childNodes;

                    if (!target.isReplace) {
                        section.innerHTML = "";
                    }

                    for (let i = 0, c = nodes.length; i < c; i++) {
                        convertUrls(nodes[i], filePath);
                        const node = document.importNode(nodes[i], true);

                        if (target.isReplace) {
                            section.parentNode.insertBefore(node, section);
                        } else {
                            section.appendChild(node);
                        }

                        if (node instanceof Element) {
                            loadExternal(node, filePath);
                        }
                    }

                    if (target.isReplace) {
                        section.parentNode.removeChild(section);
                    }

                    if (options.async) {
                        deck.sync();
                        deck.setState(deck.getState());
                    }
                } else {
                    console.error(
                        "ERROR: The attempt to fetch " + url +
                        " failed with HTTP status " + xhr.status + "."
                    );
                }
            };

            xhr.open("GET", url, options.async);

            try {
                xhr.send();
            } catch (e) {
                console.error(
                    "Failed to get the file " + url +
                    ". Make sure that the presentation and the file are served by an HTTP server and can be found there.",
                    e
                );
            }
        }

        function loadExternal(container, path) {
            const currentPath = typeof path === "undefined" ? "" : path;

            if (
                container instanceof Element &&
                (container.getAttribute("data-external") || container.getAttribute("data-external-replace"))
            ) {
                const target = getTarget(container);
                if (target) {
                    updateSection(container, target, currentPath);
                }
            } else {
                const sections = container.querySelectorAll("[data-external], [data-external-replace]");
                for (let i = 0; i < sections.length; i++) {
                    const target = getTarget(sections[i]);
                    if (target) {
                        updateSection(sections[i], target, currentPath);
                    }
                }
            }
        }

        return {
            id: "external",
            init: function(reveal) {
                deck = reveal;

                const config = deck.getConfig() || {};
                config.external = config.external || {};

                options = {
                    async: !!config.external.async,
                    mapAttributes: Array.isArray(config.external.mapAttributes)
                        ? config.external.mapAttributes
                        : (config.external.mapAttributes ? ["src"] : []),
                };

                loadExternal(deck.getRevealElement());
            },
        };
    }

    window.RevealExternal = createPlugin();
})();
