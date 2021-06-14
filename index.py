from os import error
from util.records import get_new_rec_offset, write_into_files, write_game_count, get_game_count


class Games:

    mode = 1
    count = 0

    def __init__(self, name, genre, pf, desc, dev, pub, r_date):
        self.name = name
        self.genre = genre
        self.pf = pf
        self.desc = desc
        self.pub = pub
        self.r_date = r_date

    def __str__(self):
        return "\nName : "+self.name+"\nGenre : "+self.genre+"\nPlatforms supported : "+self.pf+"\nDescription : "\
               + self.desc+"\nDeveloper : " \
            + self.dev + "\nPublisher : " + self.pub+"\nRelease Date : "+self.r_date

    @staticmethod
    def get_offsets(rrn):
        i_file = open("./text files/index.txt", "r")
        lines = i_file.readlines()
        rrns = [int(line.split('|')[0]) for line in lines]
        if rrn in rrns:
            i = rrns.index(rrn)
            offset = [int(line.split('|')[1]) for line in lines][i]
            return offset
        i_file.close()
        return -1

    @staticmethod
    def open_files(mode):
        file = open("./text files/g_name.txt", mode)
        i_file = open("./text files/index.txt", mode)
        sec_file = open("./text files/sec_index.txt", mode)

        return [file, i_file, sec_file]

    @staticmethod
    def close_files(files):
        for file in files:
            file.close()

    @staticmethod
    def get(rrn):
        file, i_file, sec_file = Games.open_files("r")

        if Games.get_offsets(rrn) != -1:
            name_offset = Games.get_offsets(rrn)
            file.seek(name_offset, 0)
            temp = file.readline().split("|")
            g_name = [val.strip() for val in temp]

            if g_name[1][0] != "$":
                g_name[7] = g_name[7][0:g_name[7].index(
                    "%")] if "%" in g_name[7] else g_name[7]
                print(g_name[7])
                game_obj = Games(
                    g_name[1], g_name[2], g_name[3], g_name[4], g_name[5], g_name[6], g_name[7])
                print('Game found')
                return game_obj
        else:
            print("Game not found\n")

        Games.close_files([file, i_file, sec_file])

    @staticmethod
    # returns 1 if the game name is already there else 0
    def check_for_duplicate_by_name(name):
        name_file = open("./text files/g_name.txt", "r")
        records = name_file.readlines()
        # print(records)
        if records != []:
            name_arr = [record.strip().split('|')[1].strip().lower()
                        for record in records]
            return 1 if name.lower().strip() in name_arr else 0
        else:
            return 0

    @staticmethod
    # returns 1 if the game name is already there else 0
    def check_for_duplicate_by_rrn(rrn):
        i_file = open("./text files/index.txt", "r")
        records = i_file.readlines()
        rrns = [int(record.split('|')[0]) for record in records]
        return 1 if rrn in rrns else 0

    def pack(self):

        if Games.mode == 1:  # append
            file,  i_file, sec_file = Games.open_files("a")

        elif Games.mode == 0:  # write
            file,  i_file, sec_file = Games.open_files("w")

        if(not file) or (not i_file) or (not sec_file):
            print("File could not be created!!\n")

        else:

            rrn = str(Games.count+1)
            g_name_rec = "|"+self.name+"|"+self.genre+"|"+self.pf+"|" + \
                self.desc+"|"+self.dev+"|"+self.pub+"|"+self.r_date+"\n"
            sec_index_rec = rrn + "|" + self.name+"\n"
            i_rec = rrn + "|0\n"

            if Games.count != 0:
                i_rec = rrn + "|" + str(get_new_rec_offset())+"\n"

            values_arr = [g_name_rec, i_rec, sec_index_rec]
            files_arr = [file, i_file, sec_file]

            write_into_files(files_arr, values_arr)
            Games.count = Games.count + 1
            write_game_count(Games.count)
            Games.close_files(files_arr)

    @staticmethod
    def delete(name):

        i = -1

        file = open("./text files/g_name.txt", "r")
        i_file = open("./text files/index.txt", "r")
        sec_file = open("./text files/sec_index.txt", "r")

        # get all the records form the secondary index file
        records = sec_file.readlines()
        all_games = [record.strip().split('|')[1].strip().lower()
                     for record in records]
        rrns = [record.strip().split('|')[0].strip().lower()
                for record in records]

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

    def modify(self, rrn):

        name_offset = Games.get_offsets(rrn)
        file, i_file, sec_file = Games.open_files("r")
        sindex_records = sec_file.readlines()

        all_game_records = file.readlines()
        file.seek(name_offset, 0)
        game_record = file.readline()
        file.close()
        g_name_len = len(game_record)
        game_name = game_record.split("|")[1]

        name = input("Enter the name of the game: \n")
        gen = input("Enter the genre of the game : \n")
        pf = input("Enter the platforms supported by the game : \n")
        desc = input("Enter the description for the game : \n")
        dev = input("Enter the developer's name for the game : \n")
        pub = input("Enter the publisher's name for the game : \n")
        r_date = input("Enter the release date for the game : \n")

        g_name_mod = "|"+name+"|"+gen+"|"+pf+"|"+desc+"|"+dev+"|"+pub+"|"+r_date
        g_name_mod_len = len(g_name_mod)

        if g_name_mod_len > g_name_len:

            # Delete the old record and just enter a new record into the file

            Games.delete(self.name)
            game_obj = Games(name, gen, pf, desc, dev, pub, r_date)
            game_obj.pack()

        else:

            # Replace the old record with the new record if it's length is less than the old record's length

            Games.close_files([file, i_file, sec_file])
            file = open("./text files/g_name.txt", "w")
            sec_file = open("./text files/sec_index.txt", "w")

            # Write the modified record in place of the old record

            index = all_game_records.index(game_record)
            all_game_records[index] = g_name_mod+"%" + \
                all_game_records[index][g_name_mod_len+1:]
            file.writelines(all_game_records)

            # Write the modified name in the secondary index file

            rrns = [int(line.split('|')[0]) for line in sindex_records]
            new_index_rec = str(rrn)+"|"+name+"\n"
            sindex_records[rrns.index(rrn)] = new_index_rec
            sec_file.writelines(sindex_records)

        Games.close_files([file, i_file, sec_file])


# fmode = mode in which the file should be opened n - write mode y -append mode
# op = operation to be performed on the file add, display, delete and modify
# data = can be an array of the necessary values for add op, or name for del or rrn for the modify


def main(fmode, op, data):
    y = 'y'
    if fmode == "n":
        write_game_count(0)
        Games.count = 0
        Games.mode = 0  # write mode
    else:
        Games.mode = 1  # append mode
        Games.count = get_game_count()

    if op == "add":

        name, gen, pf, desc, pub, r_date = data
        if name and gen and pf and desc and pub and r_date:
            game_obj = Games(name, gen, pf, desc, pub, r_date)
            game_obj.pack()
        else:
            raise Exception("Game details cannot be empty\n")

    # delete
    elif op == "del":
        if Games.check_for_duplicate_by_name(data):
            Games.delete(data)
            print("Deleted successfully\n")
        else:
            raise Exception("Game not found\n")

    # modification
    elif op == "mod":
        rrn = data[0]
        if Games.check_for_duplicate_by_rrn(rrn):
            game_obj = Games.get(rrn)
            game_obj.modify(rrn)
            print("Record modified successfully \n")
        else:
            raise Exception("Game not found\n")

    else:
        raise Exception("Invalid operation\n")
