import sqlite3
from sqlite3.dbapi2 import Cursor
from flask import Flask, render_template, request, url_for,redirect,flash
import datetime

app = Flask(__name__)

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/form')
def form():
     return render_template('sub.html')

@app.route('/parcourir')
def parcourir():
     return render_template('parcourir.html')

@app.route('/post',methods=['post'])
def post():
     form_data=request.form.to_dict()
     subs = sqlite3.connect('sub.db')
     cursor = subs.cursor()
     cursor.execute("""
     INSERT INTO table1(Nom,Posté_par,Mots_clés,description,création) values(?,?,?,?,?)""",(str(form_data['name']),'admin',str(form_data['domaine']),str(form_data['description']),datetime.date.today()))
     subs.commit()
     cursor.execute("""SELECT MAX(Numéro_projet) FROM table1 """)
     id = cursor.fetchall()
     subs.close()
     return redirect('/')


@app.route('/search', methods=['GET', 'POST'])
def recherche():
    search = request.form.to_dict()
    if request.method == 'POST':
        return search_results(search)
    return render_template('resultat.html', form=search)


@app.route('/results')
def search_results(search):
     resultat = []
     search_str = search['Search']
     subs = sqlite3.connect('sub.db')
     cursor = subs.cursor()
     cursor.execute("""SELECT * FROM table1""")
     contenu=cursor.fetchall()
     resultat=[]
     for row in contenu:
          if search_str in row[0] or search_str in row[3]:
               date=row[5].split('-')
               Y=int(date[0])
               M=int(date[1])
               D=int(date[2])
               resultat.append(row[:-1]+(str((datetime.date.today()-datetime.date(Y,M,D)).days)+' days ago',))
               
     subs.close()
     if not resultat:
         return render_template('resultat.html',resultat='')
     else:
         return render_template('resultat.html', resultat=resultat)

@app.route('/sub/<id>')
def viewsub(id):
     subs = sqlite3.connect('sub.db')
     cursor = subs.cursor()
     query='''SELECT Nom,description FROM table1 WHERE Numéro_projet=?'''
     cursor.execute(query,id)
     L=(cursor.fetchall(),id)
     subs.close()
     return render_template('viewsub.html',data=L)

@app.route('/sub/<id>/post')
def viewpost(id):
     return render_template('viewpost.html', data=id)


@app.route('/sub/<id>/creationpost')
def newpost(id):
     return render_template('newpost.html',data=id)

@app.route('/postsub/<id>',methods = ['GET','POST'])
def postsub(id):
     titre = request.form['titre']
     description = request.form['description']
     db = sqlite3.connect('post.db')
     cursor = db.cursor()
     cursor.execute("INSERT INTO %s(id_sub,titre,description,date_creation,nbr_visistes) values(%s,%s,%s,%s,%s)",(f"post_{id}",id,titre,description,datetime.date.today(),0))
     db.commit()
     db.close()
     return redirect('/')





if __name__=='__main__':
     app.run(debug=1)