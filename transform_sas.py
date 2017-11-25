import argparse

# All of the strings needed to create the first function
four = ' ' * 4
eight = ' ' * 8
twelve = ' ' * 12


def create_docstring(rec_type, func_name):
    global four
    global eight
    global twelve
    docstring = ('\ndef {}(rec):\n'.format(func_name) +
                 four + '"""\n' +
                 four + 'Process a {} record from '.format(rec_type) +
                 'the raw CPS file.\n\n' +
                 four + 'Parameters\n' + four + '----------\n' +
                 four + 'rec: String containing a ' +
                 'CPS {} record\n\n'.format(rec_type) +
                 four + 'Returns\n' + four + '-------\n' +
                 four + 'DataFrame with the final record\n\n' +
                 four + '"""\n' +
                 four + 'record = OrderedDict()\n\n')
    return docstring


def set_loc(curr_start, length):
    pystart = curr_start
    pyend = pystart + length
    return pystart, pyend


def create_section(sas):
    curr_start = 0
    sec_string = ''
    end_line = False
    x = sas.readline().split()
    while not end_line:
        curr_start = int(x[0][1:]) - 1
        if x[2][-1] != '.':
            deci = int(x[2][-1])
            lgth = int(x[2][0]) - deci
            name = x[1]
            start1, end1 = set_loc(curr_start, lgth)
            curr_start += lgth
            start2, end2 = set_loc(curr_start, deci)
            s1 = four + "record['{}'] = ".format(name)
            s2 = "[float(rec[{}:{}] + '.' + ".format(start1, end1)
            s3 = "rec[{}:{}])]\n".format(start2, end2)
            s = s1 + s2 + s3
        elif x[2][0] == '$':
            lgth = int(x[2][1:-1])
            name = x[1]
            start, end = set_loc(curr_start, lgth)
            s = four + "record['{}'] = [int(rec[{}:{}])]\n".format(name, start,
                                                                   end)
        else:
            name = x[1]
            lgth = int(x[2][:-1])
            start, end = set_loc(curr_start, lgth)
            if lgth == 1:
                s = four + "record['{}'] = [int(rec[{}])]\n".format(name,
                                                                    start)
            else:
                s = four + "record['{}'] = [int(rec[{}:{}])]\n".format(name,
                                                                       start,
                                                                       end)
        str_vars = ['h_idnum2', 'h_idnum1', 'peridnum']
        if name in str_vars:
            s = four + "record['{}'] = [str(rec[{}:{}])]\n".format(name,
                                                                   start,
                                                                   end)
        sec_string += s
        x = sas.readline().split()
        if len(x) == 0 or x[0] == ';':
            end_line = True
    sec_string += "\n    return pd.DataFrame(record)\n\n"
    return sec_string


def find_section(sas):
    input_line = False
    while not input_line:
        line = sas.readline()
        split_line = line.split()
        # Account for new line values
        newline_check = len(split_line) == 0
        if not newline_check:
            if split_line[0] == 'INPUT' and len(split_line) == 1:
                input_line = True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('year', help=('Year of the CPS file'))
    args = parser.parse_args()
    sas = open('sas_cps{}.txt'.format(args.year), 'r')
    lead_docstring = ('"""\n' +
                      'Read in raw CPS data file and structure ' +
                      'to be used in future scripts\n' +
                      'Input file: asec2016_pubuse_v3.dat\n' +
                      'Run time is approximately two hours\n' + '"""\n')
    import_statements = ('from collections import OrderedDict\n' +
                         'import pandas as pd\n' +
                         'from tqdm import tqdm\n\n')

    house_func = create_docstring('household', 'h_recs')
    fam_func = create_docstring('family', 'f_recs')
    person_func = create_docstring('person', 'p_recs')

    create_func = '\ndef create_cps(raw_cps):\n'
    start_ds = (four + '"""\n    Function to start ' +
                'process of creating the CPS file\n\n' + four +
                'Parameters\n' +
                four + '----------\n' +
                four + 'raw_cps: String containing path to ' +
                'CPS file in DAT format as downloaded\n' +
                twelve + ' from the NBER website\n\n' +
                four + 'Returns\n' +
                four + '-------\n' +
                four + 'CPS file as a pandas DF\n' +
                four + '"""\n' +
                four + "# Read in CPS file\n")
    read_file = (four + 'cps = [line.strip().split() for line in\n' +
                 eight + '   open(raw_cps).readlines()]\n\n')
    loop_prep = (four + '# Empty list to hold the completed records\n' +
                 four + 'cps_list = []\n' +
                 four + "print ('Creating Records')\n")
    loop = (four + "for record in tqdm(cps):\n" +
            eight + "# Find the type of record\n" +
            eight + "rectype = record[0][0]\n" +
            eight + "if rectype == '1':\n" +
            twelve + "# If it's a household, hold that record " +
            "to concat to family records\n" +
            twelve + "house_rec = h_recs(record[0])\n" +
            eight + "elif rectype == '2':\n" +
            twelve + "# If it's a family record, concat to household " +
            "record and store\n" +
            twelve + "house_fam = pd.concat([house_rec, f_recs" +
            "(record[0])], axis=1)\n" +
            eight + "else:\n" +
            twelve + "# If it's a person record, concat to " +
            "household and family record\n" +
            twelve + "final_rec = pd.concat([house_fam, " +
            "p_recs(record[0])], axis=1)\n" +
            twelve + "# Append final record to the list of records\n" +
            twelve + "cps_list.append(final_rec)\n\n")
    export = (four + "# Create data set by combining all of the records\n" +
              four + "cps_mar = pd.concat(cps_list)\n" +
              four + "# Export the data\n" +
              four + "print ('Exporting Data')\n" +
              four + "cps_mar.to_csv('cpsmar{}.csv', ".format(args.year) +
              "index=False)\n" +
              four + "return cps_mar")

    find_section(sas)
    house_sec = create_section(sas)
    find_section(sas)
    fam_sec = create_section(sas)
    find_section(sas)
    person_sec = create_section(sas)
    combined = (lead_docstring + import_statements + house_func +
                house_sec + fam_func + fam_sec + person_func +
                person_sec + create_func + start_ds +
                read_file + loop_prep + loop + export + '\n')
    pyfile = open('cpsmar_{}.py'.format(args.year), 'w+')
    pyfile.write(combined)
    sas.close()
    pyfile.close()


if __name__ == '__main__':
    main()
