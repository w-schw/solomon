
def image_collection():
    """

    :return: spare_ammo, mag_ammo, plate_count, money, name, noise,
    event, people_left_solo, upgrade, location, non_lethal,
    initial_jump, health, mag_ammo, lethal, circle_count, circle_time, kills, self_revive, key_card, gasmask,
    killstreak, weapon
    """
    import numpy as np
    from PIL import ImageGrab
    import os
    import cv2 as cv
    import time

    #timenow = time.time()

    #screenshot the entire screen
    original_img = np.array(ImageGrab.grab())

    #to expand left, decrease x1
    #to expand right, increase x2
    #to expand up, reduce y1
    #to expand down, increase y2

    #crop format: y1:y2, x1:x2


    # copy regions of interest - turn off ones i have enough of
    #spare_ammo = original_img[1327:1354, 2232:2296] # all 3 digits
    #mag_ammo = original_img[1276:1318, 2197:2295] # all 3 digits
    plate_count = original_img[1335:1361, 485:506]
    money = original_img[1370:1389, 86:156]
    name = original_img[1314:1329, 76:190]
    noise = original_img[1130:1190, 2163:2261]


    #people_left_solo = original_img[70:97, 2275:2313] #all digits - original mask
    people1 = original_img[72:97, 2180:2197]

    people2 = original_img[72:97,2197:2214]
    people3 = original_img[72:97, 2214:2231]
    people_all = original_img[72:97, 2180:2231]
    upgrade = original_img[1138:1194, 2435:2509]
    location = original_img[81:101, 1150:1450]
    non_lethal = original_img[1287:1338, 2343:2388]
    health = original_img[1354:1356, 76:341]
    lethal = original_img[1285:1338, 2430:2488]
    circle_count = original_img[420:440, 66:83]
    #circle_time = original_img[420:443, 105:166] # all digits
    kills = original_img[73:97, 2376:2397]
    self_revive = original_img[1368:1388, 320:343]
    key_card = original_img[1368:1390, 344:365]
    killstreak = original_img[1000:1085, 2404:2522]
    #weapon = original_img[1270:1350, 1881:2200] #warzone gun only region -- outdated??
    wz_weapon = original_img[1267: 1350, 1936: 2200]  # CORRECT WZ RANGE 22 June
    #weapon = original_img[1119:1350, 1880:2200] #warzone weapon with same size as gun game

    no_weapon = original_img[964: 1047, 1936: 2200]

    gasmask = original_img[1324:1382, 533:585]
    gg_weapon = original_img[1135:1366, 1920:2240] #CORRECT GG REGION
    event = original_img[831:860, 127:511]
    mag_ammo = original_img[1273:1317, 2261:2293]
    spare_ammo = original_img[1329:1354, 2273:2293]
    spare_ammo2 = original_img[1329:1354, 2253:2273]
    non_lethal_count = original_img[1301:1327, 2391:2409]
    circle_time = original_img[419:441, 147:163]
    spare_ammo2= original_img[1330:1354,2252:2273]

    #tbd:
    #initial_jump = original_img[75:88, 2160:2164]
    #lethal_count
    #nonlethal_count
    #players_remaining
    #groups_remaining
    # mag_ammo = original_img[1274:1316, 2227:2295]

    return(spare_ammo, mag_ammo, plate_count, money, name, noise, event, upgrade, location, non_lethal,
           health, lethal, circle_count, circle_time, kills, self_revive, key_card, gasmask, killstreak, gg_weapon,
           non_lethal_count, spare_ammo2, no_weapon, wz_weapon, people1, people2, people3, people_all)


def gg_weapon_collection():
    import numpy as np
    from PIL import ImageGrab

    original_img = np.array(ImageGrab.grab())
    #reference = original_img[1214:1366, 1920:2240]
    #name = original_img[1214:1242, 1996:2204]
    weapon = original_img[1135:1366, 1920:2240]
    #gg_weapon = np.array(ImageGrab.grab(bbox=(1920, 1270, 2240, 1366)))
    return(weapon)

def wz_weapon_collection():
    import numpy as np
    from PIL import ImageGrab

    original_img = np.array(ImageGrab.grab())
    #reference = original_img[1214:1366, 1920:2240]
    #name = original_img[1214:1242, 1996:2204]
    #weapon = original_img[1119:1350, 1880:2200] #original port from gg
    #weapon = original_img[1139:1370, 1880:2200] #adjusted
    #gg_weapon = np.array(ImageGrab.grab(bbox=(1920, 1270, 2240, 1366)))
    weapon  = original_img[1267: 1350, 1936: 2200] # CORRECT WZ RANGE 22 June

    return(weapon)

def whole_screen_collection():
    import numpy as np
    from PIL import ImageGrab
    original_img = np.array(ImageGrab.grab())
    return(original_img)

def generate_gun_dict():
    import pandas as pd
    gundb = pd.read_excel("gun_db.xlsx")
    base = gundb['python_base2']
    blue = gundb['python2']
    guns = dict(zip(blue, base))
    return(guns)

def weapon_pipeline(gun_dict, get_path, write_path, backup_path ):
    import os
    import time
    import cv2 as cv
    guns = gun_dict
    path = get_path
    writepath = write_path
    backuppath= backup_path

    add_to_backup_directory = []
    add_to_label_directory =[]
    add_to_gun_db =[]

# name images

    for subdir, dirs, files in os.walk(path):
        unique = time.time()
        for filename in files:
            unique += .000001
            filepath = subdir + os.sep + filename
            blueprint = filepath.split('\\')
            name = blueprint[-2]
            if filepath.endswith(".jpg"):
                os.rename(filepath, os.path.join(subdir, str(unique)) + " " + name + '.jpg')


# process images
    for subdir, dirs, files in os.walk(path):
        for folders in dirs:
            folderpath = os.path.join(path, folders)
            name = folders
            base = guns.get(name, 'mising')

            if base =='mising':
                print(str(name)+ " looks like a new gun, please make sure its in the gun db")
                add_to_gun_db.append(name)
            else:
                check_class_path = os.path.join(writepath, base)
                check_backup_path = os.path.join(backuppath, name)

                if os.path.isdir(check_class_path)==True:
                    if os.path.isdir(check_backup_path)==True:
                        current_files = os.listdir(folderpath)

                        for filename in current_files:
                            filepath = folderpath + os.sep + filename

                            if filepath.endswith(".jpg"):
                                img = cv.imread(filepath)
                                crop = img[140:223, 45:309]
                                newname = base + '\\' + str(filename)
                                cv.imwrite(os.path.join(writepath, newname), crop)
                                backupname = name + '\\' + str(filename)
                                cv.imwrite(os.path.join(backuppath, backupname), img)
                                os.remove(filepath)
                    else:
                        print("the backup directory for " + str(name) + " is missing")
                        add_to_backup_directory.append(name)
                        pass
                else:
                    print("the label directory " + str(base) + " is missing")
                    add_to_label_directory.append(base)
                    pass
                print(add_to_gun_db)
                print(add_to_backup_directory)
                print(add_to_label_directory)

