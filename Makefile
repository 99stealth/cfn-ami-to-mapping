
install: install-dependencies
	@echo "Installing cfn-ami-to-mapping"
	@cp main.py /usr/local/bin/cfn-ami-to-mapping && chmod +x /usr/local/bin/cfn-ami-to-mapping && echo "✅ Utility has been successfully installed" || echo "❌ Something went wrong and we could not fix that automatically"

install-dependencies:
	@echo "Installing required dependencies"
	@pip install -r requirements.txt > /dev/null && echo "✅ Dependencies packages successfully installed" || echo "❌ Something went wrong and we could not fix that automatically"

update: clean install

clean:
	@echo "Uninstalling an utility"
	rm -f /usr/local/bin/cfn-ami-to-mapping
