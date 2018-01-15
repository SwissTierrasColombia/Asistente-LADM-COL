
all: resources_rc.py i18n/Asistente-LADM_COL_es.qm

clean:
	rm -f resources_rc.py
	rm -f i18n/Asistente-LADM_COL_es.qm
	rm -f *.pyc *~

resources_rc.py: resources.qrc
	pyrcc5 -o resources_rc.py resources.qrc

i18n/Asistente-LADM_COL_es.qm: i18n/Asistente-LADM_COL_es.ts
	lrelease i18n/Asistente-LADM_COL.pro
