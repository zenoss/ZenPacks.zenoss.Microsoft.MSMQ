###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2014-2017 Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

default: egg

egg:
	python setup.py bdist_egg

clean:
	rm -rf build dist *.egg-info

test:
	runtests ZenPacks.zenoss.Microsoft.MSMQ
	./check_pep8.sh

reinstall:
	zenpack --remove ZenPacks.zenoss.Microsoft.MSMQ
	zenpack --link --install .

pretty_xml:
	python -c "from butils.pprint import format_xml; format_xml('ns/objects/objects.xml')"
