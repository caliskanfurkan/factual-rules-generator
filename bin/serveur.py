import os
import sys
import time
import flask
s = ""
for i in os.path.dirname(sys.argv[0]).split("/")[:-1]:
    s += i + "/"
sys.path.append(s + "etc")
import allVariables


def WriteFileP(s, current):
    f = open(os.path.dirname(sys.argv[0]) + "/tmp", "w")
    f.write(s + ":" + current)
    f.close()


app = flask.Flask(__name__)
#app.config["DEBUG"] = True

f = open(allVariables.applist, "r")
listapp = f.readlines()

lapp = dict()
list_app = list()
flagun = False
cp = -1

for l in listapp:
    l = l.split(":")
    lapp[l[0]] = l[1].rstrip(("\n"))

list_app = list(lapp.keys())

@app.route('/', methods=['GET'])
def home():
    return "<h1>AutoGene Yara</h1>"

@app.route('/installer', methods=['GET'])
def installer():
    global cp, flagun

    if flagun:
        return flask.redirect("/uninstaller")
    else:
        cp += 1

        try:
            loc = list_app[cp]
        except:
            exit(0)

        flagun = True
        WriteFileP("install", lapp[list_app[cp]])
        return '<div>{"%s":"%s"}</div>' % (list_app[cp], lapp[list_app[cp]])


@app.route('/uninstaller', methods=['GET'])
def uninstaller():
    global cp, flagun

    try:
        loc = list_app[cp]
    except:
        exit(0)

    flagun = False
    WriteFileP("uninstall", lapp[list_app[cp]])
    return '<div>{"%s":"%s"}</div>' % (list_app[cp], lapp[list_app[cp]])


if __name__ == '__main__':
    app.run(host=allVariables.host, port=int(allVariables.port))
