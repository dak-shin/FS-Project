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
