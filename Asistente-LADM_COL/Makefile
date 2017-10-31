
all: resources_rc.py

clean:
	rm -f resources_rc.py
	rm -f *.pyc *~

resources_rc.py: resources.qrc
	pyrcc5 -o resources_rc.py resources.qrc
