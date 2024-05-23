import os
import subprocess
import platform


def commande_use(commande):
    reponse = " "
    while True:
        if commande == "exit":
            break
        if commande == "infos":
            reponse = platform.platform() + " " + os.getcwd() + " > "
        else:
            commande_split = commande.split(" ")
            if len(commande_split) == 2 and commande_split[0] == "cd":
                try:
                    os.chdir(commande_split[1])
                except FileNotFoundError:
                    print("ERREUR : ce répertoire n'exite pas")
            else:
                result = subprocess.run(commande, shell=True, capture_output=True,
                                        universal_newlines=True)  # dir sur PC
                reponse = result.stdout + result.stderr
        return reponse
