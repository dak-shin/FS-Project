# returns array with [name offset, desc offset, dev offset]


def get_new_rec_offset():

    file = open("./text files/g_name.txt", "a")
    offset = file.tell()
    file.close()

    return offset

# This function takes an array of file objects and an array of values to be written into those files


def write_into_files(files, values):
    i = 0
    for file in files:
        file.write(values[i])
        i = i+1
        file.close()

# Writes the number of records into num.txt


def write_game_count(count):
    c_file = open("./text files/num.txt", "w")
    temp = str(count)
    c_file.write(temp)
    c_file.close()

# Gets the count from num.txt


def get_game_count():
    c_file = open("./text files/num.txt", "r")
    temp = c_file.read().strip()
    c_file.close()
    return int(temp) if temp else 0

# Delete a particular record from the data file 


def delete(name):

    i = -1

    file = open("./text files/g_name.txt", "r")  
    i_file = open("./text files/index.txt", "r")  
    sec_file = open("./text files/sec_index.txt", "r")


    # get all the records form the secondary index file 
    records = sec_file.readlines()
    all_games = [record.strip().split('|')[1].strip().lower() for record in records]
    rrns = [record.strip().split('|')[0].strip().lower() for record in records]


    # get the rrn of the record to be deleted from the secondary index file 
    if name in all_games:
        drec_index = all_games.index(name)
        drec_rrn = int(rrns[drec_index])


    # get the offsets from the index file using the rrn 
    name_offset = 0
    lines = i_file.readlines()
    rrns = [int(line.split('|')[0]) for line in lines]


    # get offset of the record to be deleted
    if drec_rrn in rrns:
        i = rrns.index(drec_rrn)
        offset = [int(line.split('|')[1]) for line in lines][i]
    else:
        print("Record's RRN is not in the list of RRNs \n")

    name_recs = file.readlines()
    file.seek(offset, 0)
    dname_rec = file.readline()
    file.close()

    dgame_index = name_recs.index(dname_rec)
    name_recs[dgame_index] = "$" + name_recs[dgame_index][1:]
    file = open("./text files/g_name.txt", "w")

    file.writelines(name_recs)

    i_file.close()
    sec_file.close()

    i_file = open("./text files/index.txt", "w")  #
    sec_file = open("./text files/sec_index.txt", "w")

    lines.remove(lines[i])
    i_file.writelines(lines)

    records.remove(records[drec_index])
    sec_file.writelines(records)

    i_file.close()
    sec_file.close()

    #print("Game has been deleted successfully")

    






























