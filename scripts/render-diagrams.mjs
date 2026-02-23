import { readdirSync, mkdirSync, existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");

const diagramsDir = path.join(repoRoot, "assets", "diagrams");
const outputDir = path.join(repoRoot, "assets", "generated", "diagrams");
const themeDark = path.join(diagramsDir, "mermaid-theme-dark.json");
const themeLight = path.join(diagramsDir, "mermaid-theme-light.json");

if (!process.env.PUPPETEER_EXECUTABLE_PATH) {
    const macCandidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        path.join(process.env.HOME ?? "", "Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        path.join(process.env.HOME ?? "", "Applications/Chromium.app/Contents/MacOS/Chromium")
    ];

    for (const candidate of macCandidates) {
        if (candidate && existsSync(candidate)) {
            process.env.PUPPETEER_EXECUTABLE_PATH = candidate;
            break;
        }
    }
}

if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
}

if (!process.env.PUPPETEER_EXECUTABLE_PATH) {
    console.error("Error: PUPPETEER_EXECUTABLE_PATH is not set and no Chrome/Chromium was found.");
    console.error("Install Chrome/Chromium or set PUPPETEER_EXECUTABLE_PATH to the browser binary.");
    process.exit(1);
}

const diagramFiles = readdirSync(diagramsDir)
    .filter((file) => file.endsWith(".mmd"))
    .map((file) => path.join(diagramsDir, file));

if (diagramFiles.length === 0) {
    console.log("No Mermaid diagrams found in assets/diagrams.");
    process.exit(0);
}

const runMmdc = (inputFile, outputFile, themeFile) => {
    const result = spawnSync(
        "mmdc",
        [
            "-i",
            inputFile,
            "-o",
            outputFile,
            "-b",
            "transparent",
            "-C",
            themeFile,
            "-t",
            "default"
        ],
        { stdio: "inherit" }
    );

    if (result.status !== 0) {
        process.exit(result.status ?? 1);
    }
};

for (const diagramFile of diagramFiles) {
    const baseName = path.basename(diagramFile, ".mmd");
    const darkOutput = path.join(outputDir, `${baseName}.dark.svg`);
    const lightOutput = path.join(outputDir, `${baseName}.light.svg`);

    runMmdc(diagramFile, darkOutput, themeDark);
    runMmdc(diagramFile, lightOutput, themeLight);
}
