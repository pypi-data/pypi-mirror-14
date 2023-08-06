sdist:
	rm dist/SiQt*; make stamp; python setup.py sdist bdist_wheel; 

stamp:
	sed -i '$$ d' siqt/__init__.py ; sed -i '$$ d' siqt/__init__.py ; echo '__version_date__ = "'`git log --pretty=format:'%cd' -n 1`'"' >> siqt/__init__.py; echo '__version_hash__ = "'`git log --pretty=format:'%h' -n 1`'"' >> siqt/__init__.py

release_notes:
	git log --pretty=format:" - [\`%h\`] *%ai*%n%n   - %s%n  %b" >> RELEASE.md

test2: 
	python2 /usr/bin/nosetests -s SiQt --with-coverage --cover-package=SiQt
test3: 
	python3 /usr/bin/nosetests -s SiQt --with-coverage --cover-package=SiQt

# twine upload -s dist/
