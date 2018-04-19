import os

def superCopy():
    for file in os.listdir("./output"):
        if file.endswith(".txt"):
            os.popen("cat ./output/" + file + " >> ./superReport$(date).txt")
