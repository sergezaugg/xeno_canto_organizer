


# map to original sound-types like in CAR 
sound_type_mapping_dict = { 
    'Amazona festiva' : 'festive_amazon_call',
    'Attila bolivianus' : 'dull_capped_attila_song',
    'Cacicus cela' : 's000040',
    'Capito aurovirens' : 's000015',
    'Crotophaga major' : 's000031',
    'Crypturellus undulatus' : 'undulated_tinamou_song',
    'Glaucidium brasilianum' : 's000014',
    'Leptotila rufaxilla' : 'grayfronted_dove_song',
    'Monasa nigrifrons' : 'black_fronted_nunbird_song',
    'Myrmelastes hyperythrus' : 's000010',
    'Nasica longirostris' : 'updownsweep_2kHz_dur1s_01',
    'Nyctibius grandis' : 's000003',
    'Nyctibius griseus' : 's000021',
    'Pitangus sulphuratus' : 's000038',
    'Psarocolius angustifrons' : 's000020',
    'Ramphastos tucanus' : 's000025',
    'Taraba major' : 's000022',
    'Trogon melanurus' : 's000016',
    'Xiphorhynchus guttatus' : 's000011',
    'Xiphorhynchus obsoletus' : 's000023',
    }

def map_to_sound_type(spec_name):
    return(sound_type_mapping_dict[spec_name])

# map_to_sound_type('Leptotila rufaxilla')
# df_all['sound_type'] = df_all['full_spec_name'].apply(map_to_sound_type)
# temp 



