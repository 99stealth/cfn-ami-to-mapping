
install: build
	@echo "Installing cfn-ami-to-mapping"
	@pip install dist/cfn-ami-to-mapping-*

remove:
	@echo "Uninstalling cfn-ami-to-mapping"
	@pip uninstall cfn-ami-to-mapping -y

update: remove install

build:
	@echo "Building the package"
	@python3 setup.py sdist

clean:
	@echo "Removing build"
	@rm -Rf dist/ *.egg-info/

rebuild: clean build