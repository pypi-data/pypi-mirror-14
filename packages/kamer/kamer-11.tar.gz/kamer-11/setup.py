#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run kamer with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='kamer',
    version='11',
    url='https://pikacode.com/bart/kamer',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" KAMER - mishandeling gepleegd door toediening van voor het leven of de gezondheid schadelijk stoffen """,
    license='MIT',
    zip_safe=False,
    scripts=["bin/kamer",],
    install_requires=["meds"],
    packages=['kamer',
             ],
    long_description = """ 

binnenkort stemt de Tweede Kamer over de Wet verplichte GGZ en ik wil u en de Tweede Kamer hierover informeren.

Mishandeling van medicijnen is strafbaar in het Wetboek van Strafrecht:

* Artikel 300.4 Met mishandeling wordt gelijkgesteld opzettelijke benadeling van de gezondheid.

* Artikel 304.3 indien het misdrijf wordt gepleegd door toediening van voor het leven of de gezondheid schadelijke stoffen.

Behandeling met antipsychotica is opzettelijke benadeling van de gezondheid gepleegd door toediening van voor het leven of de gezondheid schadelijke stoffen, om met die benadeling van de gezondheid te proberen de psychotische symptomen te verminderen.

kortom:

Antipsychotica brengen schade toe aan de hersenen in de hoop met toebrenging van die schade de psychotische symptomen te verminderen. De schade die men toebrengt is opzettelijk en daarmee is het mishandeling.

Op basis van een wettelijk voorschrift  is deze mishandeling niet strafbaar:

* Artikel 42 Niet strafbaar is hij die een feit begaat ter uitvoering van een wettelijk voorschrift

Een wet die tot behandeling verplicht en op die manier de mishandeling niet strafbaar maakt, maakt niet dat men geen misdrijf pleegt. Er word nog steeds een misdrijf gepleegd, waar men schuldig aan is en wat direct gestopt dient te worden. Het is de plicht van het Openbaar Ministerie om op te treden als er strafbare feiten worden gepleegd, ook als vervolging tot niet strafbaar leid, met als argument dat als het plegen van mishandeling niet gestopt word er geen einde komt aan de mishandeling.

Met het aannemen van de Wet verplichte Geestelijke Gezondheidzorg maakt de Tweede Kamer de behandeling met antipsychotica verplicht en daarmee mishandeling gepleegd door het toedienen van voor het leven en de gezondheid schadelijke stoffen niet strafbaar. De Tweede Kamer maakt zich hiermee schuldig aan het op grote schaal mogelijk maken van mishandeling.

De Wet verplichte GGZ dient u daarom niet aan te nemen en om huidige mishandelingen te stoppen dient u terstond het Openbaar Ministerie ontvankelijk te maken voor elke patient die zijn mishandeling door de strafrechter gestopt wil zien worden.


                       """, 
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
