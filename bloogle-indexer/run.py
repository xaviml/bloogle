import optparse

parser = optparse.OptionParser()

parser.add_option('-i', '--input',
    action="collect", dest="input",
    help="Input path")

options, args = parser.parse_args()
#options.input -> to access the data folder

# for loop through htmls file, calling the parser and elasticsearch