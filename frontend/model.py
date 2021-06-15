
from frontend.app import app, login_manager
from util.records import get_new_rec_offset, write_into_files, write_game_count, get_game_count
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)


# check for duplicate games

def check_duplicate_games(user_id, game_name):
    with open("./text files/purchases.txt", "r") as file:
        purchases = file.readlines()
        owned_games = []
        for record in purchases:
            if record.split("|")[0] == str(user_id):
                owned_games.append(record.split("|")[1].strip())
        if game_name in owned_games:
            return True
        return False


class Games:

    mode = 1
    count = 0

    def __init__(self, name, genre, pf, desc, pub, r_date, price):
        self.name = name
        self.genre = genre
        self.pf = pf
        self.desc = desc
        self.price = price
        self.pub = pub
        self.r_date = r_date

    def __str__(self):
        return "\nName : "+self.name+"\nGenre : "+self.genre+"\nPlatforms supported : "+self.pf+"\nDescription : "\
               + self.desc + "\nPublisher : " + self.pub + \
            "\nRelease Date : "+self.r_date+"\nPrice : "+self.price

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
                # print(g_name[7])
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

    @staticmethod
    def get_all_games():
        games_obj_arr = []
        with open("./text files/g_name.txt", "r") as games_file:
            all_games = games_file.readlines()
            for game in all_games:
                if game[0] != "$":
                    temp = game.strip().split("|")
                    game_obj = Games(
                        temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7])
                    games_obj_arr.append(game_obj)
                else:
                    continue

        return games_obj_arr

    @staticmethod
    def purchase_game(game_name, user_obj):
        with open("./text files/purchases.txt", "a") as file:
            purchase_rec = str(user_obj.id)+"|"+game_name+"\n"
            file.write(purchase_rec)

    @staticmethod
    def get_owned_games(user_id):

        def get_the_game(rec):
            id = rec.split("|")[0]
            return True if user_id == int(id) else False

        with open("./text files/purchases.txt", "r") as file:
            purchases = file.readlines()
            # print(purchases)
            game_name_arr = filter(get_the_game, purchases)
            # print(list(game_name_arr))

        return game_name_arr

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
                self.desc+"|"+self.pub+"|"+self.r_date+"|"+self.price+"\n"
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

    def modify(self, rrn, info_arr):

        name_offset = Games.get_offsets(rrn)
        file, i_file, sec_file = Games.open_files("r")
        sindex_records = sec_file.readlines()

        all_game_records = file.readlines()
        file.seek(name_offset, 0)
        game_record = file.readline()
        file.close()
        g_name_len = len(game_record)
        game_name = game_record.split("|")[1]

        name, gen, pf, desc, pub, r_date = info_arr

        g_name_mod = "|"+name+"|"+gen+"|"+pf+"|" + \
            desc+"|"+pub+"|"+r_date+"|"+self.price
        g_name_mod_len = len(g_name_mod)

        if g_name_mod_len+2 > g_name_len:

            # Delete the old record and just enter a new record into the file

            Games.delete(self.name)
            game_obj = Games(name, gen, pf, desc, pub, r_date)
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


class Users(UserMixin):

    user_count = 0

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def pack(self):
        user_rec = str(self.id)+"|"+self.username.lower() + \
            "|"+self.password + "\n"
        with open("./text files/users.txt", "a") as user_file:
            user_file.write(user_rec)
            Users.user_count = Users.user_count + 1
            with open("./text files/user_count.txt", "w") as count_file:
                count_file.write(str(Users.user_count))
            return 1

    @staticmethod
    def get_count():
        with open("./text files/user_count.txt", "r") as file:
            temp = file.readline()
            new_id = int(temp) if temp else 1
            Users.user_count = new_id
        return new_id

    @staticmethod
    def check_username(username):
        with open("./text files/users.txt", "r") as user_file:
            records = user_file.readlines()
            usernames = [record.split("|")[1] for record in records]
            if username in usernames:
                return True
            else:
                return False

    @staticmethod
    def check_password(username, password):
        with open("./text files/users.txt", "r") as user_file:
            records = user_file.readlines()
            usernames = [record.split("|")[1] for record in records]
            if username.lower() in usernames:
                index = usernames.index(username.lower())
                pw = [record.split("|")[2] for record in records][index]
                if password == pw:
                    return True
                else:
                    raise Exception(pw, password)
                    return False
            else:
                raise Exception(usernames, username)

    @staticmethod
    def get(user_id):
        user_id = int(user_id)
        with open("./text files/users.txt", "r") as user_file:
            records = user_file.readlines()
            userids = [int(record.split("|")[0]) for record in records]
            if user_id in userids:
                index = userids.index(user_id)
                password = [record.split("|")[0] for record in records][index]
                username = [record.split("|")[1] for record in records][index]
                return Users(user_id, username, password)
            else:
                return None

    @staticmethod
    def get_user_by_name(username):
        with open("./text files/users.txt", "r") as user_file:
            records = user_file.readlines()
            usernames = [record.split("|")[1] for record in records]
            if username in usernames:
                index = usernames.index(username)
                password = [record.split("|")[2] for record in records][index]
                user_id = [record.split("|")[0] for record in records][index]
                return Users(user_id, username, password)
            else:
                return None
