{
  description = "Open-Ortho lectures dev environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      supportedSystems = [
        "x86_64-darwin"
        "aarch64-darwin"
        "x86_64-linux"
        "aarch64-linux"
      ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      devShells = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        {
          default = pkgs.mkShell {
            packages = [
              pkgs.nodejs_20
              pkgs.nodePackages."@mermaid-js/mermaid-cli"
            ]
            ++ pkgs.lib.optionals pkgs.stdenv.isLinux [ pkgs.chromium ];
            shellHook =
              if pkgs.stdenv.isLinux then
                ''
                  export PUPPETEER_EXECUTABLE_PATH="${pkgs.chromium}/bin/chromium"
                ''
              else
                ''
                  if [ -z "$PUPPETEER_EXECUTABLE_PATH" ]; then
                    for CANDIDATE in \
                      "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
                      "/Applications/Chromium.app/Contents/MacOS/Chromium" \
                      "$HOME/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
                      "$HOME/Applications/Chromium.app/Contents/MacOS/Chromium"; do
                      if [ -x "$CANDIDATE" ]; then
                        export PUPPETEER_EXECUTABLE_PATH="$CANDIDATE"
                        break
                      fi
                    done
                  fi

                  if [ -z "$PUPPETEER_EXECUTABLE_PATH" ]; then
                    echo "Mermaid CLI needs a Chromium/Chrome executable."
                    echo "Install Chrome and export PUPPETEER_EXECUTABLE_PATH to its binary."
                  fi
                '';
          };
        }
      );
    };
}
