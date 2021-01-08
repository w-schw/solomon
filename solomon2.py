from collection import wz_weapon_collection
from collection import image_collection
from collection import gg_weapon_collection
from model_building_functions import get_label_dictionary
import tensorflow as tf
import cv2 as cv
import time
import os
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing import image
with tf.device('/cpu:0'):
    #Import saved Models

    #log_path = #insert filepath for directory to save in
    #model_path = #insert path to models

    model =tf.keras.models.load_model("model_charlie_1.h5")

    #model = tf.keras.models.load_model('weapon_classification_v2_9d.h5')


    lethal_model = tf.keras.models.load_model(model_path+'lethal_v2.h5')
    non_lethal_model = tf.keras.models.load_model(model_path+'non_lethal_v2.h5')
    plate_count_model = tf.keras.models.load_model(model_path+"plate_count.h5")
    gasmask_model = tf.keras.models.load_model(model_path+'gasmask_v1.h5')
    killstreak_model = tf.keras.models.load_model(model_path+'killstreak_v1_5.h5')

    weapon_dict, lethal_dict, non_lethal_dict, killstreak_dict, gasmask_dict, plate_count_dict = get_label_dictionary()
    game_id=time.time() #initialize game ID


    '''
    #where to write the screenshots to during gameplay for later inspection
    write_weapon_path = log_path
    write_lethal_path =log_path
    write_non_lethal_path =log_path

    write_killstreak_path =log_path
    write_gasmask_path =log_path
    write_platecount_path=log_path
    '''

    mode = input('gg or wz?')
    count=0
    if mode =='gg':
        start_time=time.time()
        capture_time_list=[]
        game_time_list=[]
        weapon_label_list=[]
        lethal_list = []
        non_lethal_list = []

        while True:
            try:
                count+=1
                capture_time = time.time()


                spare_ammo, mag_ammo, plate_count, money, name , noise, event, people_left_solo, upgrade, location, non_lethal, \
                health, lethal, circle_count, circle_time, kills, self_revive, key_card, gasmask, killstreak, weapon, \
                non_lethal_count, spare_ammo_2, non_weapon = image_collection()

                weapon = gg_weapon_collection()
                crop = weapon[140:223, 46:310]

                with tf.device('/cpu:0'):

                    #weapon
                    x=tf.keras.preprocessing.image.img_to_array(crop)
                    x = x / 255
                    image = np.vstack([x])
                    image = np.expand_dims(x, axis=0)
                    type = model.predict(image)
                    type2= np.argmax(type)
                    weapon_label = weapon_dict.get(type2)

                    #lethal
                    x = tf.keras.preprocessing.image.img_to_array(lethal)
                    x = x / 255
                    image = np.vstack([x])
                    image = np.expand_dims(x, axis=0)
                    type = lethal_model.predict(image)
                    type2 = np.argmax(type)
                    lethal_label = lethal_dict.get(type2)

                    #nonlethal
                    x = tf.keras.preprocessing.image.img_to_array(non_lethal)
                    x = x / 255
                    image = np.vstack([x])
                    image = np.expand_dims(x, axis=0)
                    type = non_lethal_model.predict(image)
                    type2 = np.argmax(type)
                    non_lethal_label = non_lethal_dict.get(type2)



                    #write

                    write_time=time.time()
                    game_time=write_time-start_time

                    capture_time_list.append(count)
                    game_time_list.append(game_time)
                    weapon_label_list.append(weapon_label)
                    non_lethal_list.append(non_lethal_label)
                    lethal_list.append(lethal_label)



                    print("pass complete, it took" + str(write_time-capture_time)+' seconds' )
                    cv.imwrite(os.path.join(write_weapon_path, str(count) + ' weapon.jpg'), crop)
                    cv.imwrite(os.path.join(write_lethal_path, str(count) + ' lethal.jpg'), lethal)
                    cv.imwrite(os.path.join(write_non_lethal_path, str(count) + ' non_lethal.jpg'), non_lethal)




                    time.sleep(.86)


            except KeyboardInterrupt:
                break
        print("Ok, wrapping up...")
        output = pd.DataFrame(capture_time_list)
        output['game_time']=game_time_list
        output['weapon']=weapon_label_list
        output['lethal']=lethal_list
        output['non_lethal']=non_lethal_list

        output.to_csv(str(log_path)+'game_at'+str(game_id)+'.csv')

    if mode =='wz':
        start_time = time.time()
        capture_time_list = []
        game_time_list = []
        weapon_label_list = []
        gasmask_list = []
        plate_count_list = []
        killstreak_list = []
        # upgrade_list = []
        lethal_list = []
        non_lethal_list = []

        while True:
            try:
                count += 1
                capture_time = time.time()

                spare_ammo, mag_ammo, plate_count, money, name, noise, event, upgrade, location, non_lethal,\
                health, lethal, circle_count, circle_time, kills, self_revive, key_card, gasmask, killstreak, gg_weapon,\
                non_lethal_count, spare_ammo2, no_weapon, wz_weapon, people1, people2, people3, people_all = image_collection()

                weapon = wz_weapon
                #crop = weapon[140:223, 46:310]

                with tf.device('/cpu:0'):

                    # weapon
                    x = tf.keras.preprocessing.image.img_to_array(weapon)
                    x = x / 255
                    image = np.vstack([x])
                    image = np.expand_dims(x, axis=0)
                    type = model.predict(image)
                    type2 = np.argmax(type)
                    weapon_label = weapon_dict.get(type2)

                    # lethal
                    x = tf.keras.preprocessing.image.img_to_array(lethal)
                    x = x / 255
                    image = np.vstack([x])
                    image = np.expand_dims(x, axis=0)
                    type = lethal_model.predict(image)
                    type2 = np.argmax(type)
                    lethal_label = lethal_dict.get(type2)

                    # nonlethal
                    x = tf.keras.preprocessing.image.img_to_array(non_lethal)
                    x = x / 255
                    image = np.vstack([x])
                    image = np.expand_dims(x, axis=0)
                    type = non_lethal_model.predict(image)
                    type2 = np.argmax(type)
                    non_lethal_label = non_lethal_dict.get(type2)

                    # gasmask
                    x = tf.keras.preprocessing.image.img_to_array(gasmask)
                    x = x / 255
                    image = np.vstack([x])
                    image = np.expand_dims(x, axis=0)
                    type = gasmask_model.predict(image)
                    gasmask_label = np.argmax(type)
                    #gasmask_label = gasmask_dict.get(type2)

                    # killstreak
                    x = tf.keras.preprocessing.image.img_to_array(killstreak)
                    x = x / 255
                    image = np.vstack([x])
                    image = np.expand_dims(x, axis=0)
                    type = killstreak_model.predict(image)
                    type2 = np.argmax(type)
                    killstreak_label = killstreak_dict.get(type2)

                    # plate count
                    x = tf.keras.preprocessing.image.img_to_array(plate_count)
                    x = x / 255
                    image = np.vstack([x])
                    image = np.expand_dims(x, axis=0)
                    type = plate_count_model.predict(image)
                    type2 = np.argmax(type)
                    plate_count_label = plate_count_dict.get(type2)

                    # write

                    write_time = time.time()
                    game_time = write_time - start_time

                    capture_time_list.append(count)
                    game_time_list.append(game_time)
                    weapon_label_list.append(weapon_label)
                    non_lethal_list.append(non_lethal_label)
                    lethal_list.append(lethal_label)
                    gasmask_list.append(gasmask_label)
                    killstreak_list.append(killstreak_label)
                    plate_count_list.append(plate_count_label)

                    print("pass complete, it took" + str(write_time - capture_time) + ' seconds')
                    cv.imwrite(os.path.join(write_weapon_path, str(count) + ' weapon.jpg'), weapon)
                    cv.imwrite(os.path.join(write_lethal_path, str(count) + ' lethal.jpg'), lethal)
                    cv.imwrite(os.path.join(write_non_lethal_path, str(count) + ' non_lethal.jpg'), non_lethal)
                    cv.imwrite(os.path.join(write_gasmask_path, str(count) + ' gasmask.jpg'), gasmask)
                    cv.imwrite(os.path.join(write_killstreak_path, str(count) + ' killstreak.jpg'), killstreak)
                    cv.imwrite(os.path.join(write_platecount_path, str(count) + ' plate_count.jpg'), plate_count)

                    time.sleep(.86)


            except KeyboardInterrupt:
                break
        print("Ok, wrapping up...")
        output = pd.DataFrame(capture_time_list)
        output['game_time'] = game_time_list
        output['weapon'] = weapon_label_list
        output['lethal'] = lethal_list
        output['non_lethal'] = non_lethal_list
        output['gasmask'] = gasmask_list
        output['plate_count'] = plate_count_list
        output.to_csv(str(log_path) + 'game_at' + str(game_id) + '.csv')






    if mode != 'gg' or 'wz':
        print('gg only my dude')
