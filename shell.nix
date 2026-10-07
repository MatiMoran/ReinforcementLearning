{pkgs ? import <nixpkgs> {}}:

pkgs.mkShell {
  buildInputs = [
    (pkgs.python314.withPackages (ps: [
      ps.ebooklib
      ps.markdownify
      ps.beautifulsoup4
    ]))
    pkgs.poetry
  ];

  shellHook = ''
    if [ ! -d .venv ]; then
      echo "Installing Python dependencies with poetry (first run, may take a few minutes)..."
      poetry install
    fi
    poetry run python -m ipykernel install --user --name reinforcement-learning-uba \
      --display-name "Reinforcement Learning (.venv)" >/dev/null 2>&1 || true
    python - "$LD_LIBRARY_PATH" <<'PY'
    import json, os, sys
    p = os.path.expanduser("~/.local/share/jupyter/kernels/reinforcement-learning-uba/kernel.json")
    kj = json.load(open(p))
    kj.setdefault("env", {})["LD_LIBRARY_PATH"] = sys.argv[1]
    json.dump(kj, open(p, "w"), indent=1)
    PY
    echo "LD_LIBRARY_PATH=$LD_LIBRARY_PATH" > .env
    echo "Environment ready. Launch notebooks with: nix-shell --run \"poetry run jupyter lab\""
  '';

  LD_LIBRARY_PATH = with pkgs; lib.makeLibraryPath [
    stdenv.cc.cc.lib
    zlib
    libpng
    freetype
    fontconfig
  ];
}
