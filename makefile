ext_name=ods2pdf

all:
	zip install

zip:
	rm -f $(ext_name).oxt
	zip -r $(ext_name).oxt ods2pdf/* -x */__pycache__/*

install:
	unopkg add $(ext_name).oxt

update:
	make zip
	unopkg reinstall $(ext_name).oxt

uninstall:
	unopkg remove $(ext_name).oxt