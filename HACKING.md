# Setting up Your Pyramid App Cookiecutter Test Development Environment

First you'll need to install:

* [Git](https://git-scm.com/).
  On Ubuntu: `sudo apt install git`, on macOS: `brew install git`.
* [pyenv](https://github.com/pyenv/pyenv).
  See [pyenv's README](https://github.com/pyenv/pyenv#readme) for install instructions.
  First you need to [install the Python build dependencies](https://github.com/pyenv/pyenv/wiki#suggested-build-environment)
  then on macOS use the **Homebrew** installation method,
  on Ubuntu use the **Basic GitHub Checkout** method.
  You _don't_ need to set up pyenv's shell integration ("shims"), you can
  [use pyenv without shims](https://github.com/pyenv/pyenv#using-pyenv-without-shims).
* [GNU Make](https://www.gnu.org/software/make/).
  This is probably already installed or will have been installed while installing pyenv, run `make --version` to check.

Then to set up your development environment:

```terminal
git clone https://github.com/hypothesis/pyramid-app-cookiecutter-test.git
cd pyramid_app_cookiecutter_test
make services
make devdata
make help
```

Changing the Project's Python Version
-------------------------------------

To change what version of Python the project uses:

1. Change the Python version in the
   [cookiecutter.json](.cookiecutter/cookiecutter.json) file. For example:

   ```json
   "python_version": "3.10.4",
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Re-compile the `requirements/*.txt` files.
   This is necessary because the same `requirements/*.in` file can compile to
   different `requirements/*.txt` files in different versions of Python:

   ```terminal
   make requirements
   ```

4. Commit everything to git and send a pull request

Changing the Project's Python Dependencies
------------------------------------------

### To Add a New Dependency

Add the dependency to the appropriate `requirements/*.in` file(s) and then run:

```terminal
make requirements
```

### To Remove a Dependency

Remove the dependency from the appropriate `requirements/*.in` file(s) and then run:

```terminal
make requirements
```

### To Upgrade or Downgrade a Dependency

We mostly rely on [Dependabot](https://github.com/dependabot) to keep all our
dependencies up to date by sending automated pull requests to all our repos.

If you need to upgrade or downgrade a dependency manually you can use
[pip-tools](https://pip-tools.readthedocs.io/en/latest/) to do that locally.
First make sure that pip-tools is installed:

```terminal
PYENV_VERSION=3.10.4 pyenv exec pip install --quiet --disable-pip-version-check --upgrade pip-tools
```

Then to upgrade a dependency to the latest version:

```terminal
PYENV_VERSION=3.10.4 pyenv exec pip-compile --allow-unsafe --quiet --generate-hashes --upgrade-package <FOO> requirements/<ENV>.in
make requirements
```

To upgrade or downgrade a dependency to a specific version

```terminal
PYENV_VERSION=3.10.4 pyenv exec pip-compile --allow-unsafe --quiet --generate-hashes --upgrade-package <FOO>==<X.Y.Z> requirements/<ENV>.in
make requirements
```

To upgrade all dependencies to their latest versions:

```terminal
PYENV_VERSION=3.10.4 pyenv exec pip-compile --allow-unsafe --quiet --generate-hashes --upgrade <FOO> requirements/<ENV>.in
make requirements
```
