import sys
import subprocess
import zdbc

def main():
    if (len(sys.argv) == 1) or (not sys.argv[1]):
        sys.exit(2)

    cmd = sys.argv[1]

    if   cmd == "ls":
        '\n'.join(zdbc.ls('.'))

    elif cmd == "search":
        if len(sys.argv) < 5:
            sys.exit(2)

        sargs = list()
        linktype = prop = matchtype = value = ""
        sargs.append( ( "AND", sys.argv[2], sys.argv[3], sys.argv[4] ) )
        as2 = 1
        for i in sys.argv[5:]:
            if as2 == 1:
                linktype = i
            elif as2 == 2:
                prop = i
            elif as2 == 3:
                matchtype = i
            elif as2 == 4:
                value = i
                as2 = 0
                sargs.append( ( linktype, prop, matchtype, value ) )

            as2 += 1

        '\n'.join(zdbc.search(*sargs))

    elif cmd == "entry":
        if len(sys.argv) < 4:
            sys.exit(2)

        enti = zdbc.entry(sys.argv[2])
        scmd = sys.argv[3]
        prop = 'D'

        if not (len(sys.argv) == 4):
            prop = sys.argv[4]

        if scmd == "get":
            val = enti.getraw(prop)
            if val:
                print(": DS " + enti.name + " :")
                print(val)
            else:
                sys.exit(1)
        elif scmd == "getraw":
            val = enti.getraw(prop)
            if not val:
                sys.exit(1)
            print(val)
        elif scmd == "set":
            if len(sys.argv) < 6:
                sys.exit(2)
            if (len(sys.argv) == 7) and (sys.argv[6] == "true"):
                enti.set(prop, sys.argv[5], True)
            else:
                enti.set(prop, sys.argv[5])
        elif scmd == "rm":
            enti.rm(prop)
        else:
            sys.exit(2)

    elif (cmd == "help") or (cmd == "--help"):
        mymp = 'zdbc'
        if (len(sys.argv) > 2) and sys.argv[2]:
            mymp += '-' + sys.argv[2]

        sys.exit(subprocess.call(["man", mymp]))

    elif cmd == "--version":
        print("zdbc 0.2.3")

    else:
        sys.exit(2)
