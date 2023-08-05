
help:
	@echo "Targets:"
	@echo "   clean           Delete build/test artifacts"
	@echo "   demo1           Test expandFile API and include_template."
	@echo "   demo2           Test expandString."
	@echo "   demo3           Test command line expansion of two files."
	@echo "   demo4           Test some other expanString cases."
	@echo
	@echo "   sdist           Build a pypi distribution. NOTE: Update version in setup.py!"
	@echo "   register_sdist  Register (1st time) and upload (all times) with pypi"
	@echo "        In addition to 'sdict' and 'register_sdict' to release to pypi,"
	@echo "        remember to commit to git:"
	@echo "            git status"
	@echo "            git add './*'"
	@echo "            git commit -a -m \"latest changes\""
	@echo "            git push"
	@echo
	@echo "   local_install   Copy ./pytem.py to ../../lib/python3.5/site-packages/pytem.py"



clean:
	@rm -f *.out
	@rm -f *.tm.py
	@rm -f README.html README.txt
	@rm -rf __pycache__

demo1: clean
	@python pytem_demo1.py

demo2: clean
	@python pytem_demo2.py

demo3: clean
	@python pytem.py -d 0x0100 -o pytem_demo3.out -p pytem_demo3.tm pytem_demo3a.tm

demo4: clean
	@python pytem_demo4.py

sdist: clean
	@pandoc -s README.md -o README.txt
	@python setup.py check
	@python setup.py sdist --formats=zip

#Initial registration with pypi:
register_sdist:
	python setup.py register sdist upload


# Local install the pytem.py module
local_install:
	cp ./pytem.py  ../../lib/python3.5/site-packages/pytem.py
