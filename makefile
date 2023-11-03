ext_name=ods2pdf

all: pkg install

pkg:
	rm -f $(ext_name).oxt
	cd src && zip -r ../$(ext_name).oxt ./* -x */__pycache__/* && cd ..

install: clean_lock
	unopkg add "$(ext_name).oxt"
	
update: pkg uninstall install

uninstall:
	unopkg remove $(ext_name).oxt

clean_lock:
	rm -f $(HOME)/.config/libreoffice/*/.lock