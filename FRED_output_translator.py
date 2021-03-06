import base_output_translator
import pandas as pd
import csv
import os
import getopt, sys


def main(argv):
    filename = ''
    try:
      opts, args = getopt.getopt(argv,"hi:o:t:",["ifile="])
    except getopt.GetoptError:
      print('test.py -i <inputfile>')
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputlocation>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            filename = arg
        elif opt in("-o", "--olocation"):
            output_location = arg
        elif opt in("-t", "--tempdir"):
            temp_file = arg

    translate_output(filename, output_location, temp_file)

def translate_output(filename, output_location, temp_file):
    # age,gender,race,location,simulator_time,infection_state,disease_state,count
    df = base_output_translator.hdf5_to_dataframe(filename)
    df.to_csv(temp_file, encoding='utf-8')

    data = {}
    data.setdefault('age', [])
    data.setdefault('race', [])
    data.setdefault('location', [])
    data.setdefault('gender', [])
    data.setdefault('day', [])
    data.setdefault('infection_state', [])
    data.setdefault('disease_state', [])
    data.setdefault('count', [])

    print("Beginning processing")
    i = 0
    with open(temp_file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if(i!=0):
                age = row[1]
                race = row[2]
                location = row[3]
                gender = row[4]
                day = row[5]

                #pop_inc = df['N_i'][i]
                #pop_prev = df['N_p']
                #s_inc = df['S_i']
                count = row[9]
                # data['infection_state'].append('susceptible_prevalent')
                # data['disease_state'].append('asymptomatic')
                data['infection_state'].append(1)
                data['disease_state'].append(0)
                data['age'].append(age)
                data['race'].append(race)
                data['location'].append(location)
                data['gender'].append(gender)
                data['day'].append(day)
                data['count'].append(count)

                #e_inc = df['E_i']
                count = row[11]
                # data['infection_state'].append('latent_prevalent')
                # data['disease_state'].append('asymptomatic')
                data['infection_state'].append(2)
                data['disease_state'].append(0)
                data['age'].append(age)
                data['race'].append(race)
                data['location'].append(location)
                data['gender'].append(gender)
                data['day'].append(day)
                data['count'].append(count)

                #i_inc = df['I_i']
                count = row[13]
                # data['infection_state'].append('infectious_prevalent')
                # data['disease_state'].append('asymptomatic')
                data['infection_state'].append(3)
                data['disease_state'].append(0)
                data['age'].append(age)
                data['race'].append(race)
                data['location'].append(location)
                data['gender'].append(gender)
                data['day'].append(day)
                data['count'].append(count)

                #symp_inc = df['Y_i']
                count = row[15]
                # data['infection_state'].append('infectious_prevalent')
                # data['disease_state'].append('symptomatic')
                data['infection_state'].append(3)
                data['disease_state'].append(1)
                data['age'].append(age)
                data['race'].append(race)
                data['location'].append(location)
                data['gender'].append(gender)
                data['day'].append(day)
                data['count'].append(count)

                #r_inc = df['R_i']
                count = row[17]
                # data['infection_state'].append('recovered_prevalent')
                # data['disease_state'].append('asymptomatic')
                data['infection_state'].append(4)
                data['disease_state'].append(0)
                data['age'].append(age)
                data['race'].append(race)
                data['location'].append(location)
                data['gender'].append(gender)
                data['day'].append(day)
                data['count'].append(count)
            i = i+1
            if(i%1000000==0):
                print(row)

    print("Processing complete")
    os.remove(temp_file)
    dataFrame = pd.DataFrame(data)
    print(dataFrame.shape)
    dataFrame.to_hdf(output_location+'modifiedOutput_compressed.h5','df',format='table',mode='w', complevel=9, complib='zlib')
    print("Modified hdf5 file created")

    # hdf5_file = h5py.File('modifiedOutput_compressed.h5', 'r')
    #
    # dataset = list(hdf5_file.keys())[0]
    # hdf5_file.close()

    # testDF = pd.read_hdf('modifiedOutput_compressed.h5', key=dataset)
    # print(testDF.shape)
    # print(testDF[:10])

if __name__ == "__main__":
   main(sys.argv[1:])

