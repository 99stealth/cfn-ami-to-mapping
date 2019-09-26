
install: build
	@echo "Installing cfn-ami-to-mapping"
	@pip install dist/cfn-ami-to-mapping-* && echo "✅ Package successfully installed" || echo "❌ Something went wrong during the package installation"

remove:
	@echo "Uninstalling cfn-ami-to-mapping"
	@pip uninstall cfn-ami-to-mapping -y && echo "✅ Package successfully uninstalled" || echo "❌ Something went wrong during the package removal"

update: remove install

build:
	@echo "Building the package" && echo "✅ Package successfully built" || echo "❌ Something went wrong during the build"
	@python3 setup.py sdist

clean:
	@echo "Removing build"
	@rm -Rf dist/ *.egg-info/ && echo "✅ Build successfully removed" || echo "❌ Something went wrong during the build removal"

rebuild: clean build