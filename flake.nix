{
  description = "Flake for jpdb";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
    flake-utils.url = "github:numtide/flake-utils";
    nixgl = {
      url = "github:nix-community/nixGL";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, nixgl, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        nixGLIntel = nixgl.packages.${system}.nixGLIntel;
        surferWrapped = pkgs.writeShellScriptBin "surfer" ''
          exec ${nixGLIntel}/bin/nixGLIntel ${pkgs.surfer}/bin/surfer "$@"
        '';
      in {
        devShell = pkgs.mkShell {
          nativeBuildInputs = [ pkgs.pkg-config pkgs.perl pkgs.python311 ];
          buildInputs = [
            pkgs.rustc pkgs.cargo pkgs.rust-analyzer
            surferWrapped
          ];
        };
        packages.default = pkgs.rustPlatform.buildRustPackage {
          pname = "jpdb";
          version = "0.1.0";
          src = ./.;
        };
      }
    );
}
