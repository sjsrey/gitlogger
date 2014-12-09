#! /usr/bin/env python

import os
import time
today = time.strftime("%Y-%m-%d")
repos_file = "/Users/serge/.gitlogger"
output_file = "/Users/serge/Dropbox/gitlog.md"
user_names = ["Sergio Rey","Serge Rey"]

repos_file = open(repos_file)
repos = [repo.strip() for repo in repos_file.readlines() ]
repos_file.close()


output = open(output_file,'r')
output_lines = output.readlines()
output.close()
header = output_lines[0]
body = output_lines[1:]


entry_text = ""
entries = {}
lines = []
for repo in repos:
    alias,path = repo.split(":")
    print(alias, path)
    os.chdir(path)
    entries[alias] = []
    for user in user_names:
        gl="git log --author=\"{0}\" --pretty=\"{1}\" --no-merges --since=\"{2}\"".format(user,"%s","yesterday")
        print gl
        p = os.popen(gl,"r").read()
        print p
        if p != '':
            lines.append(alias+": "+p)
            entries[alias].append(p)
        gr="git log --remotes --author=\"{0}\" --no-merges --pretty=\"{1}\" --since=\"{2}\"".format(user,"%s","yesterday")
        p = os.popen(gr,"r").read()
        if p != '':
            lines.append(alias+": "+p)
            if p not in entries[alias]:
                entries[alias].append(p)
        print p

out = [] 
for entry in entries:
    actions =  entries[entry]
    if len(actions) > 0:
        out.append("- *{0}*".format(entry))
        for action in actions:
            out.append("\t- {0}".format(action.strip()))
print out

fo = open(output_file, 'w')
fo.write(header)
fo.write("\n## {0}\n".format(today))
fo.write("\n".join(out))
fo.write("\n")
fo.write("".join(body))
fo.close()




