{ pkgs ? import <nixpkgs> {} }:
let
  python-packages = ps: with ps; [
    psutil
    pyserial
    python-lsp-server
  ];
  python-with-packages = pkgs.python3.withPackages python-packages;
in pkgs.mkShell {
  packages = [
    python-with-packages
    pkgs.minicom
  ];
}
