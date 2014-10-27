import pickle
## label fly1 frame fly2 
#create new dict
labels = dict.fromkeys(['t0','t1','names','labels']);
#add fly names
labels['names']=[1,3];

#add labels to fly 1
labels['labels'] = [[]];
labels['labels'][0].append('multifly');
labels['labels'][0].append('multifly_none');
labels['labels'][0].append('female');
labels['labels'][0].append('female_none');
labels['labels'][0].append('chase');
labels['labels'][0].append('chase_none');


#add labels to fly 2
labels['labels'].append(list());
labels['labels'][1].append('multifly');
labels['labels'][1].append('multifly_none');
labels['labels'][1].append('female');
labels['labels'][1].append('female_none');
labels['labels'][1].append('chase');
labels['labels'][1].append('chase_none');


#add start and end frame to fly 1

labels['t0']=[[]];
labels['t0'][0].append(689);
labels['t0'][0].append(693);
labels['t0'][0].append(650);
labels['t0'][0].append(730);
labels['t0'][0].append(720);
labels['t0'][0].append(760);

labels['t1']=[[]];
labels['t1'][0].append(692);
labels['t1'][0].append(700);
labels['t1'][0].append(710);
labels['t1'][0].append(740);
labels['t1'][0].append(755);
labels['t1'][0].append(764);


#add start and end frame to fly 2

labels['t0'].append(list());
labels['t0'][1].append(2380);
labels['t0'][1].append(2390);
labels['t0'][1].append(2430);
labels['t0'][1].append(2450);
labels['t0'][1].append(2470);
labels['t0'][1].append(2500);

labels['t1'].append(list());
labels['t1'][1].append(2389);
labels['t1'][1].append(2400);
labels['t1'][1].append(2440);
labels['t1'][1].append(2460);
labels['t1'][1].append(2490);
labels['t1'][1].append(2530);

print labels

# w=csv.writer(open("output.csv","w"))
# for key,val in labels.items():
# 	w.writerow([key,val])

pickle.dump( labels, open( "save.p", "wb" ) )


























