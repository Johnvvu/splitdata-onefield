import pandas as pd
import glob, os

dir = input("Please type in the full directory path to the CSVs:").strip()
all_files = glob.glob(dir + "/*.csv")

fn_choice = input("\nDo you want to include the filename as a new field in the dataset? (y or n)").strip()

if fn_choice.lower() == 'y':
    df = pd.concat([pd.read_csv(f).assign(filename=os.path.basename(f).split('.')[0]) for f in all_files], sort=False)
else:
    df = pd.concat((pd.read_csv(f) for f in all_files), sort=False)
    
columns = list(df.columns)

x = 0
print("\n")
for f in columns:
    print(str(x) + ". " + f)
    x += 1
field_choice = []
while len(field_choice) == 0:
    field_choice = input("Choose ONE field to split the data. Enter the number choice:").strip()
field_choice = [int(i) for i in field_choice.split()]
field_names = list(df.iloc[:,field_choice])

print("\nYou chose: ")
for choice in field_choice:
    print(columns[choice])
cont = input("Do you wish to continue? (y or n)").strip()

if cont.lower() == 'y':
    fn_choice = input("\nHow would you like to name the individual files? Please choose option 1 or 2.\n1. dataset1, dataset2, dataset3 and so on...\n2. By the unique values in " + columns[choice] + "\n").strip()
    
    newdataframe = df.iloc[:,field_choice]
    uniquevalues = newdataframe.drop_duplicates().copy()
    autoinc = 1
    if fn_choice == "1":
        for a in uniquevalues.iterrows():
            data = a[1].to_frame(name=''.join(field_names))
            result = pd.merge(data,df, on=field_names, left_index=True)
            fn = ("dataset" + str(autoinc)) + ".csv"
            autoinc += 1
            result.to_csv(fn)
        print("\nTask Completed. The files are saved at: " + os.getcwd())
    else:
        for a in uniquevalues.iterrows():
            data = a[1].to_frame(name=''.join(field_names))
            result = pd.merge(data,df, on=field_names, left_index=True)
            fn = (a[1][0] + ".csv")
            result.to_csv(fn)
        print("\nTask Completed. The files are saved at: " + os.getcwd())
