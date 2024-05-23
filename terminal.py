import os
import subprocess
import platform


def commande_use(commande):
    reponse = " "
    commande_split = commande.split(" ")
    while True:
        if commande == "exit":
            reponse = ""
        if commande == "infos":
            reponse = platform.platform() + " " + os.getcwd() + " > "
        elif len(commande_split) == 2 and commande_split[0] == "cd":
            try:
                os.chdir(commande_split[1].strip("'"))
                reponse = " "
            except FileNotFoundError:
                reponse = "ERREUR : ce répertoire n'exite pas"
        else:
            result = subprocess.run(commande, shell=True, capture_output=True,
                                    universal_newlines=True)  # dir sur PC
            reponse = result.stdout + result.stderr
        return reponse
