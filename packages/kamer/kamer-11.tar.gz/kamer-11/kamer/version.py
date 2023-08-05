# kamer/version.py
#
#

""" version plugin. """

## IMPORTS

from kamer import __version__

## DEFINE

txt = """ mishandeling gepleegd door toediening van voor het leven of de gezondheid schadelijk stoffen """

## CMNDS

def version(event): event.reply("KAMER #%s - %s" % (__version__, txt))

def register(plugs): plugs.register("version", version)
