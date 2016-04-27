import pickle

data = [{'name':'sunday'},{'name':'erika'}]

# with open('pickletest.pkl','wb') as file:
# 	pickle.dump(data,file)
# 	print 'pickle saved'


with open('pickletest.pkl','rb') as file:
	data = pickle.load(file)
	print data #[0]['name'] 

data.append({'name':'nengi'})

with open('pickletest.pkl','wb') as file:
    pickle.dump(data,file)
    print 'pickle saved'


with open('pickletest.pkl','rb') as file:
    data = pickle.load(file)
    print data
