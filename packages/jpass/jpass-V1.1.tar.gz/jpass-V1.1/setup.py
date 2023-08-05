from setuptools import *

kwargs = {
	"author" : "Joe Ellis",
	"author_email" : "joechrisellis@gmail.com",
	"description" : "A command line password manager.",
	"entry_points" : {"console_scripts" : ["jpass=jpass.jpass:main"]},
	"license" : "GPL v2",
	"name" : "jpass",
	"packages" : ["jpass"],
	"version" : "V1.1",
        "install_requires" : ["pycrypto"]
}

setup(**kwargs)
