"""Dies ist das Modul 'schachtler.py'. Es stellt eine Funktion namens print_lvl(),
die eine Liste mit beliebig vielen eingebetteten Listen ausgibt."""
def print_lvl(liste, ebene=0):
        for element in liste:
                if isinstance(element, list):
                        print_lvl(element, ebene+1)
                else:
                        for tab_stop in range(ebene):
                                print("\t", end='')
                        print(element)
