from src.pdf_script.environment import AppEnvironment

with open(AppEnvironment.TEXT_PATH + '/1/1.txt') as f:
    for i in f:
        if "fig." in i.lower():
            print(i)

print("ALSDMAJSDNAJSDNAJSDNjASd")
