import json, random
import random, math
from flask import Flask, render_template, request
w=json.load(open('worldl.json'))
	
app=Flask(__name__)


@app.route('/')
def index():
	'''ref from https://gist.github.com/ywrac/9006329'''	

	dic={}
	for c in w:
		dic[c['population']]=c['name']
		afs=max(sorted(dic.keys()))
		bigpop=dic[afs]
	return render_template('index.html', w=w, bigpop=bigpop, 
		letters = [chr(i) for i in range(ord('A'), ord('Z')+1)],
		 cl=sorted(list(set([c["continent"] for c in w]))))



@app.route('/countriesBeginningWith/<a>')
def countriesBeginningWith(a):
	return render_template('list.html', a=a, letters = [chr(i) for i in range(ord('A'), ord('Z')+1)],  
cl=sorted(list(set([c["continent"] for c in w]))),
		w=[c for c in w if c['name'].startswith(a)])



@app.route('/continent/<name>')
def continent(name):
	return render_template('continent.html', name = name,
	 letters = [chr(i) for i in range(ord('A'), ord('Z')+1)]
	,cl=sorted(list(set([c["continent"] for c in w]))),	
	w = [c for c in w if c['continent'] == name])






@app.route('/country/<id>')
def country(id):
	c=None
	if int(id) >= len(w):
		c=w[int(0)]
	else:
		c=w[int(id)]
	for i in w:
		if i['area']== None:
			i['area'] = 0

		s=sorted(list(set([j['area'] for j in w if c['continent']==j['continent']])), reverse=True)
	return render_template('country.html', s=s, c=c, 
		letters = [chr(i) for i in range(ord('A'), ord('Z')+1)],
		cl=sorted(list(set([c["continent"] for c in w]))))





@app.route('/editcountryByName/<n>')
def editcountryByName(n):
	return render_template('editcountry.html', 
		letters = [chr(i) for i in range(ord('A'), ord('Z')+1)],
		c=next(c for c in w if c['name']==n), 
		cl=sorted(list(set([c["continent"] for c in w]))))
	


@app.route('/updatecountrybyname')
def updatecountryByNamePage():
	n=request.args.get('name')
	c=next(c for c in w if c['name']==n)
	c['capital']=request.args.get('capital')
	c['continent']=request.args.get('continent')
	c['area']=int(request.args.get('area'))
	c['gdp']=float(request.args.get('gdp'))
	c['population']=int(request.args.get('population'))
	c['flag']=request.args.get('flag')
	return redirect('/country/'+ request.args.get(''), c=c, 
		letters = [chr(i) for i in range(ord('A'), ord('Z')+1)],
		cl=sorted(list(set([c["continent"] for c in w]))))



@app.template_filter()
def nf(value):
	return format(int(value), ',d')




@app.route('/quiz')
def quiz():

	stem1=w[random.randint(0,len(w))]
	stem2=w[random.randint(0,len(w))]
	stem3=w[random.randint(0,len(w))]
	stem4=w[random.randint(0,len(w))]

	distractors =[]
	
	distractors.append(stem1)
	distractors.append(stem2)
	distractors.append(stem3)
	distractors.append(stem4)
	# distractors.append(w[random.randint(0,len(w))])
	# distractors.append(w[random.randint(0,len(w))])
	# distractors.append(w[random.randint(0,len(w))])
	random.shuffle(distractors)
	return render_template('quiz.html', w=w, stem1= stem1, letters = [chr(i) for i in range(ord('A'), ord('Z')+1)],
		distractors = distractors, stem2= stem2,stem3= stem3,stem4= stem4,
		
		  cl=sorted(list(set([c["continent"] for c in w]))))




@app.route('/delete/<id>')
def delete(id):
	del w[int(id)]
	for id in range(0, len(w)):
		w[id]['id']=id
	# del w[int(id)]={'name': 'Detected'}
	return render_template('index.html', letters = [chr(i) for i in range(ord('A'), ord('Z')+1)],
		 cl=sorted(list(set([c["continent"] for c in w]))))




@app.route('/createcountry')
def createCountry():
	newID=len(w)
	return render_template('createcountry.html',  newID=newID,
		letters = [chr(i) for i in range(ord('A'), ord('Z')+1)],  w=w,
		 cl=sorted(list(set([c["continent"] for c in w]))))




@app.route('/savecountry')
def savecountry():
	newCountry={}

	#newCountry['key']=request.args.get(textBoxName)
	newCountry['id']=int(request.args.get('id'))

	newCountry['name']=request.args.get('name')
	newCountry['capital']=request.args.get('capital')
	newCountry['continent']=request.args.get('continent')
	newCountry['area']=int(request.args.get('area'))
	newCountry['gdp']=float(request.args.get('gdp'))
	newCountry['tld']=request.args.get('tld')
	newCountry['population']=int(request.args.get('population'))

	newCountry['flag']=request.args.get('flag')
	w.append(newCountry)
	# sorted(key = lambda c: c['name'])
	newID=len(w)
	return render_template('country.html', c=newCountry)




if __name__ =='__main__':
	app.run(host='0.0.0.0',port=5310,debug=True)
