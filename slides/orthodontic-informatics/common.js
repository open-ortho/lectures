// common.js

// List of scripts to be dynamically loaded
const scripts = [
    '/lectures/dist/reveal.js',
    '/lectures/plugin/notes/notes.js',
    '/lectures/plugin/markdown/markdown.js',
    '/lectures/plugin/highlight/highlight.js',
    '/lectures/plugin/external/external.js',
];

// Function to load a script and return a promise that resolves when the script loads
function loadScript(src) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

// Load all scripts sequentially
scripts.reduce((promise, script) => {
    return promise.then(() => loadScript(script));
}, Promise.resolve())
    .then(() => {
        // All scripts are loaded, now initialize Reveal.js
        Reveal.initialize({
            hash: true,
            slideNumber: 'c/t',
            transition: 'fade',
            plugins: [RevealMarkdown, RevealHighlight, RevealNotes, RevealExternal],
        });

        // Additional Reveal configuration
        Reveal.configure({
            pdfSeparateFragments: false,
        });
    })
    .catch(error => {
        console.error('Error loading scripts:', error);
    });
