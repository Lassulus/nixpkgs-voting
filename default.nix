{ pkgs ? import <nixpkgs> { }
}:


pkgs.python3.pkgs.buildPythonApplication {
  pname = "nixpkgs-voting";
  version = "1.0.0";
  src = ./.;
  format = "pyproject";
  buildInputs = [ pkgs.makeWrapper ];
  propagatedBuildInputs = [
    pkgs.python3Packages.fastapi
    pkgs.python3Packages.fastapi-sso
    pkgs.python3Packages.pydantic
    pkgs.python3Packages.email-validator
    pkgs.python3Packages.uvicorn
    pkgs.python3Packages.python-jose
  ];
  nativeBuildInputs = [ pkgs.python311.pkgs.setuptools ];
  nativeCheckInputs = [
    pkgs.python311.pkgs.pytest
    # technically not test inputs, but we need it for development in PATH
    pkgs.nixVersions.stable
    pkgs.nix-prefetch-git
  ];
  # checkPhase = '' # TODO make this work
  #   PYTHONPATH= $out/bin/nixpkgs-voting --help
  # '';
  shellHook = ''
    # workaround because `python setup.py develop` breaks for me
  '';
}
