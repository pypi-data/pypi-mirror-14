# __version__="0.1.0"
#
# import sys
# import os
#
#
#
# def awesome_module():
#     print("Executing kickass_flask_template_module version %s." % __version__)
#
#     print "Let's build stuff!"
#
#     project_name = raw_input('What is your project going to be called? ')
#     print project_name + ", it's gonna be awesome!"
#     folder_location_decision = raw_input('So where\'s it going? Press 1 for current folder or hit enter to specify: ')
#
#     if folder_location_decision == "1":
#         os.mkdir(project_name)
#     else:
#         folder_location = raw_input('Ok, where do you want to put '+ project_name + "?")
#         os.mkdir(folder_location + "/" + project_name)
#
#     project_contents = raw_input('Would you like to create static and template folders? Type 1 for yes and just hit enter for no: ')
#     if project_contents == "1" and folder_location_decision != "1":
#         os.mkdir(folder_location + "/" + project_name + "/static")
#         os.mkdir(folder_location + "/" + project_name + "/templates")
#
#     elif project_contents == "1":
#         os.mkdir(project_name + '/static')
#         os.mkdir(project_name + '/templates')
#
#     project_template = raw_input('How about a server.py file with standard libraries? Type 1 for yes and hit enter for no: ')
#     if project_template == "1" and folder_location_decision != "1":
#         server_file = "server.py"
#         new_file = open(folder_location + "/" + project_name + "/" + server_file, 'w')
#         new_file.write('from flask import Flask, render_template, request, redirect, session\napp = Flask(__name__)\napp.secret_key = ""\n@app.route("/")\ndef index():\napp.run(debug=True)')
#
#     elif project_template == "1" and folder_location_decision == "1":
#         server_file = "server.py"
#         new_file = open(project_name + "/" + server_file, 'w')
#         new_file.write('from flask import Flask, render_template, request, redirect, session\napp = Flask(__name__)\napp.secret_key = ""\n@app.route("/")\ndef index():\napp.run(debug=True)')
#
#     index_file = raw_input("would you like an index.html file in your templates folder? Type 1 for yes and hit enter for no: ")
#     if index_file == "1" and folder_location_decision == "1":
#         index = "index.html"
#         new_index = open(project_name + "/" + "templates" + "/" + index, 'w')
#         new_index.write("<!DOCTYPE HTML>\n<html>\n"'    '"<head>\n"'        '"<meta>\n"'        '"<title>"+ project_name + "</title>\n"'    '"</head>\n<body>\n</body>\n</html>")
#
#     elif index_file == "1" and folder_location_decision != "1":
#         index = "index.html"
#         new_index = open(folder_location + "/" + project_name + "/" + "templates" + "/" + index, 'w')
#         new_index.write("<!DOCTYPE HTML>\n<html>\n"'    '"<head>\n"'        '"<meta>\n"'        '"<title>"+ project_name + "</title>\n"'    '"</head>\n<body>\n</body>\n</html>")




__version__="0.1.1"
import sys
import os
# class awesome_module():
def awesome_module():
    print("Executing mkflask_module version %s." % __version__)
  # print("List of argument strings: %s" % sys.argv[1:])
    print "Let's build stuff!"
    project_name = raw_input('What is your project going to be called? ')
    print (project_name + ", it's gonna be awesome!")
    folder_location_decision = raw_input('So where\'s it going? Press 1 for current folder or hit enter to specify: ')
    if folder_location_decision == "1":
        os.mkdir(project_name)
        print project_name + " folder created"
    else:
        folder_location = raw_input('Ok, where do you want to put the new project? ')
        os.mkdir(folder_location + "/" + project_name)
        print project_name + " folder created in " + folder_location
    project_contents = raw_input('Would you like to create static and template folders? Type 1 for yes and just hit enter for no: ')
    if project_contents == "1" and folder_location_decision != "1":
        os.mkdir(folder_location + "/" + project_name + "/static")
        os.mkdir(folder_location + "/" + project_name + "/templates")
        print "Static and templates folders are GO!"
    elif project_contents == "1":
        os.mkdir(project_name + '/static')
        os.mkdir(project_name + '/templates')
        print "Static and templates folders are GO!"
    if project_contents == "1":
        index_file = raw_input("Would you like an index.html file in your templates folder? Type 1 for Yes and hit enter for no: ")
        if index_file == "1" and folder_location_decision == "1":
            index = "index.html"
            new_index = open(project_name + "/" + "templates" + "/" + index, 'w')
            new_index.write("<!DOCTYPE HTML>\n<html>\n\t<head>\n\t\t<meta>\n\t\t<title>"+ project_name + "</title>\n\t</head>\n<body>\n</body>\n</html>")
            print "index.html file created in " + project_name + "/templates"
            more_files = raw_input("Would you like to make more html pages? Type 1 for Yes or hit enter for no and continue: ")
            page_amount ={}
            while more_files == "1":
                page_name = raw_input("What would you like to call the page? ")
                page = page_name+".html"
                page_amount[page_name] = page
                new_index = open(project_name + "/" + "templates" + "/" + page, 'w')
                new_index.write("<!DOCTYPE HTML>\n<html>\n\t<head>\n\t\t<meta>\n\t\t<title>"+ page_name + "</title>\n\t</head>\n<body>\n</body>\n</html>")
                print(page_name, "has been created!")
                more_files = raw_input("Would you like to make more html pages? Type 1 for Yes or hit enter for no and continue: ")
        elif index_file == "1" and folder_location_decision != "1":
            index = "index.html"
            new_index = open(folder_location + "/" + project_name + "/" + "templates" + "/" + index, 'w')
            new_index.write("<!DOCTYPE HTML>\n<html>\n\t<head>\n\t<meta>\n\t\t<title>"+ project_name + "</title>\n\t</head>\n<body>\n</body>\n</html>")
            print "index.html file created in " + project_name + "/templates"
            more_files = raw_input("Would you like to make more html pages? Type 1 for Yes or hit enter for no and continue: ")
            page_amount ={}
            while more_files == "1":
                page_name = raw_input("What would you like to call the page? ")
                page = page_name+".html"
                page_amount[page_name] = page
                new_index = open(folder_location + "/" + project_name + "/" + "templates" + "/" + page, 'w')
                new_index.write("<!DOCTYPE HTML>\n<html>\n\t<head>\n\t\t<meta>\n\t\t<title>"+ page_name + "</title>\n\t</head>\n<body>\n</body>\n</html>")
                print(page_name, "has been created!")
                more_files = raw_input("Would you like to make more html pages? Type 1 for Yes or hit enter for no and continue: ")
    project_template = raw_input('How about a server.py file with standard libraries? Type 1 for yes and hit enter for no: ')
    if project_template == "1" and folder_location_decision != "1":
        server_file = "server.py"
        new_file = open(folder_location + "/" + project_name + "/" + server_file, 'w')
        new_file.write('from flask import Flask, render_template, request, redirect, session\napp = Flask(__name__)\napp.secret_key =" "\n\n@app.route("/")\ndef index():\n\treturn render_template("index.html")\n')
        print "server.py file will be written with your routes! You're all done. Have fun!"
        for keys, data in page_amount.items():
            new_file.write('\n@app.route("/'+keys+'")\ndef '+keys+'():\n\treturn render_template("'+data+'")\n')
        new_file.write('\napp.run(debug=True)')
    elif project_template == "1" and folder_location_decision == "1":
        server_file = "server.py"
        new_file = open(project_name + "/" + server_file, 'w')
        new_file.write('from flask import Flask, render_template, request, redirect, session\napp = Flask(__name__)\napp.secret_key =" "\n\n@app.route("/")\ndef index():\n\treturn render_template("index.html")\n')
        print "server.py file will be written with your routes! You're all done. Have fun!"
        for keys, data in page_amount.items():
            new_file.write('\n@app.route("/'+keys+'")\ndef '+keys+'():\n\treturn render_template("'+data+'")\n')
        new_file.write('\napp.run(debug=True)')
