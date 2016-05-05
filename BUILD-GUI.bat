@echo off
pyuic5 tnb_gui.ui -o tnb_gui.py && pyrcc5 images.qrc -o images_rc.py