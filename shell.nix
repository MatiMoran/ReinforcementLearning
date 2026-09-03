{pkgs ? import <nixpkgs> {}}:

pkgs.mkShell {
  buildInputs = [
    (pkgs.python314.withPackages (ps: [
      ps.ebooklib
      ps.markdownify
      ps.beautifulsoup4
    ]))
  ];

  LD_LIBRARY_PATH = with pkgs; lib.makeLibraryPath [
    stdenv.cc.cc.lib
    zlib
  ];
}
