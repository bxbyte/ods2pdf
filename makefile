here=$(shell pwd)
# Build folder
build_dir=/tmp/build_ods2pdf
# Folder injected
inject_dir=src
# Source document
src_doc=template_src.ods
# Result document
res_doc=template.ods

all: clear inject

clear:
	find . -regex ".*pycache.*" -delete
	rm -rf $(build_dir)
	rm -rf $(res_doc)

inject:
	python inject.py $(inject_dir) $(src_doc) $(res_doc)