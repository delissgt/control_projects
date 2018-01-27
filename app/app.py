# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os, time
import re
from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, Form
from wtforms.validators import InputRequired, Length, EqualTo
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError, TimeoutError

from sqlalchemy import create_engine, MetaData, Table

#paginacion numero de proyectos a mostrar en la pagina del profesor
POSTS_PER_PAGE = 3

UPLOAD_FOLDER = '/home/deliss/Downloads/ss/ProSS/newproj/venv/app/imagenes'
ALLOWED_EXTENSIONS = set(['png'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mixi@localhost/Quimica'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGHT'] = 30 * 1024 * 1024
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class TblDatosI(db.Model):
    __tablename__ = "tblDatosI"
    conAlumno = db.Column(db.TEXT)
    conProfesor = db.Column(db.TEXT)
    usuProfesor = db.Column(db.String(30), primary_key=True)

    def __init__(self, conAlumno, conProfesor, usuProfesor):
        self.conAlumno = conAlumno
        self.conProfesor = conProfesor
        self.usuProfesor = usuProfesor

class Equipo(db.Model):
    __tablename__ = "equipo"
    idEquipo = db.Column(db.Integer, primary_key=True)
    carrera = db.Column(db.String(30))
    periodo = db.Column(db.String(20))
    lider = db.Column(db.String(50))
    carreraLider = db.Column(db.String(50))
    secretario = db.Column(db.String(50))
    carreraSecre = db.Column(db.String(50))
    investigador = db.Column(db.String(50))
    carreraInves = db.Column(db.String(50))
    diablo = db.Column(db.String(50))
    carreraDia = db.Column(db.String(50))
    proyecto = db.relationship("Proyecto", back_populates="equipo", uselist=False)

    def __init__(self, carrera, periodo, lider, carreraLider, secretario, carreraSecre,
                 investigador, carreraInves, diablo, carreraDia):
        self.carrera = carrera
        self.periodo = periodo
        self.lider = lider
        self.carreraLider = carreraLider
        self.secretario = secretario
        self.carreraSecre = carreraSecre
        self.investigador = investigador
        self.carreraInves = carreraInves
        self.diablo = diablo
        self.carreraDia = carreraDia

class Proyecto(db.Model):
    __tablename__ = "proyecto"
    idProyecto = db.Column(db.Integer, db.ForeignKey(Equipo.idEquipo), primary_key=True)
    nombreProyecto = db.Column(db.String(40))
    descripcionProyecto = db.Column(db.TEXT)
    sloganProyecto = db.Column(db.String(30))
    mision = db.Column(db.String(300))
    vision = db.Column(db.String(300))

    unoObjetivoEstrategico = db.Column(db.TEXT)
    unoObjetivoTactico = db.Column(db.TEXT)
    unounoObjetivoOPerativo = db.Column(db.TEXT)
    unodosObjetivoOPerativo = db.Column(db.TEXT)
    dosObjetivoEstrategico = db.Column(db.TEXT)
    dosObjetivoTactico = db.Column(db.TEXT)
    dosunoObjetivoOPerativo = db.Column(db.TEXT)
    dosdosObjetivoOPerativo = db.Column(db.TEXT)

    pais = db.Column(db.String(50))
    region = db.Column(db.String(50))
    ciudad = db.Column(db.String(50))
    coloniazona = db.Column(db.String(100))
    nivelEducacion = db.Column(db.String(100))
    edad = db.Column(db.String(50))
    sexo = db.Column(db.String(30))
    profesion = db.Column(db.String(100))
    estiloVida = db.Column(db.String(100))
    gustos = db.Column(db.String(100))
    costumbres = db.Column(db.String(200))
    habitosCompra = db.Column(db.String(200))

    nombreEmpresaUno = db.Column(db.String(50))
    nombreEmpresaDos = db.Column(db.String(50))
    nombreEmpresaTres = db.Column(db.String(50))
    sloganEmpresaUno = db.Column(db.String(50))
    sloganEmpresaDos = db.Column(db.String(50))
    sloganEmpresaTres = db.Column(db.String(50))
    estrategiasPublicidad = db.Column(db.TEXT)

    preguntaUno = db.Column(db.String(200))
    preguntaDos = db.Column(db.String(200))
    preguntaTres = db.Column(db.String(200))
    preguntaCuatro = db.Column(db.String(200))
    preguntaCinco = db.Column(db.String(200))
    preguntaSeis = db.Column(db.String(200))
    preguntaSiete = db.Column(db.String(200))
    preguntaOcho = db.Column(db.String(200))
    preguntaNueve = db.Column(db.String(200))
    preguntaDiez = db.Column(db.String(200))

    fortalezas = db.Column(db.String(500))
    oportunidades = db.Column(db.String(500))
    debilidades = db.Column(db.String(500))
    amenazas = db.Column(db.String(500))

    inicio = db.Column(db.TEXT)
    desarrollo = db.Column(db.TEXT)
    resultados = db.Column(db.TEXT)


    carpetaImagenes = db.Column(db.String(30))

    equipo = db.relationship('Equipo', back_populates="proyecto", uselist=False)

    def __init__(self, idProyecto, nombreProyecto, descripcionProyecto, sloganProyecto, carpetaImagenes,
                 mision, vision, unoObjetivoEstrategico, unoObjetivoTactico, unounoObjetivoOPerativo, unodosObjetivoOPerativo,
                 dosObjetivoEstrategico, dosObjetivoTactico, dosunoObjetivoOPerativo, dosdosObjetivoOPerativo,
                 pais, region, ciudad, coloniazona, nivelEducacion, edad, sexo, profesion, estiloVida, gustos, costumbres,
                 habitosCompra, nombreEmpresaUno, nombreEmpresaDos, nombreEmpresaTres, sloganEmpresaUno, sloganEmpresaDos,
                 sloganEmpresaTres, estrategiasPublicidad, preguntaUno, preguntaDos, preguntaTres, preguntaCuatro,
                 preguntaCinco, preguntaSeis, preguntaSiete, preguntaOcho, preguntaNueve, preguntaDiez, fortalezas,
                 oportunidades, debilidades, amenazas, inicio, desarrollo, resultados):
        self.idProyecto = idProyecto
        self.nombreProyecto = nombreProyecto
        self.descripcionProyecto = descripcionProyecto
        self.sloganProyecto = sloganProyecto
        self.carpetaImagenes = carpetaImagenes
        self.mision = mision
        self.vision = vision
        self.unoObjetivoEstrategico = unoObjetivoEstrategico
        self.unoObjetivoTactico = unoObjetivoTactico
        self.unounoObjetivoOPerativo = unounoObjetivoOPerativo
        self.unodosObjetivoOPerativo = unodosObjetivoOPerativo
        self.dosObjetivoEstrategico = dosObjetivoEstrategico
        self.dosObjetivoTactico = dosObjetivoTactico
        self.dosunoObjetivoOPerativo = dosunoObjetivoOPerativo
        self.dosdosObjetivoOPerativo = dosdosObjetivoOPerativo
        self.pais = pais
        self.region = region
        self.ciudad = ciudad
        self.coloniazona = coloniazona
        self.nivelEducacion = nivelEducacion
        self.edad = edad
        self.sexo = sexo
        self.profesion = profesion
        self.estiloVida = estiloVida
        self.gustos = gustos
        self.costumbres = costumbres
        self.habitosCompra = habitosCompra
        self.nombreEmpresaUno = nombreEmpresaUno
        self.nombreEmpresaDos = nombreEmpresaDos
        self.nombreEmpresaTres = nombreEmpresaTres
        self.sloganEmpresaUno = sloganEmpresaUno
        self.sloganEmpresaDos = sloganEmpresaDos
        self.sloganEmpresaTres = sloganEmpresaTres
        self.estrategiasPublicidad = estrategiasPublicidad
        self.preguntaUno = preguntaUno
        self.preguntaDos = preguntaDos
        self.preguntaTres = preguntaTres
        self.preguntaCuatro = preguntaCuatro
        self.preguntaCinco = preguntaCinco
        self.preguntaSeis = preguntaSeis
        self.preguntaSiete = preguntaSiete
        self.preguntaOcho = preguntaOcho
        self.preguntaNueve = preguntaNueve
        self.preguntaDiez = preguntaDiez
        self.fortalezas = fortalezas
        self.oportunidades = oportunidades
        self.debilidades = debilidades
        self.amenazas = amenazas
        self.inicio = inicio
        self.desarrollo = desarrollo
        self.resultados = resultados#funcional


@app.route('/base/<path:filename>')
def base_static(filename):
    return send_from_directory(app.root_path + '/imagenes', filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')


#ALUMNO
@app.route('/alumno')
def alumno():
    if 'username' in session:
        respuesta = make_response(redirect(url_for('formularioAlumno')))
        respuesta.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return respuesta
    else:
        return render_template("conAlumno.html")


@app.route('/loginAlumno', methods=['POST', 'GET'])
def loginAlumno():
    if request.method == 'POST':
        contraAlumno = request.form['contraAlumno']

        try:
            contraA = TblDatosI.query.filter_by(usuProfesor="gema").first()
            con = contraA.conAlumno
        except TimeoutError:
            flash('Error  no se puede cargar datos', 'error')

        if bcrypt.check_password_hash(con, contraAlumno):
            session['username'] = 'alu'
            return redirect(url_for('formularioAlumno'))
        else:
            return redirect(url_for('alumno'))
    else:
        return redirect(url_for('alumno'))


@app.route('/logouta')
def logouta():
    session.pop('username', None)
    session.pop('usernameProfesor', None)
    return redirect(url_for('index'))


@app.route('/formularioAlumno')
def formularioAlumno():
    if 'username' in session:
        respuesta = make_response(render_template('proyecto.html'))
        respuesta.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return respuesta
    else:
        return redirect(url_for('alumno'))


@app.route('/validarFormularioAlumno',  methods=['POST', 'GET'])
def validarFormularioAlumno():
    if request.method == "POST":
        carrera = request.form['carrera']
        areadesarrollo = request.form['areadesarrollo']
        periodo = request.form['periodo']
        lider = request.form['integranteLider']
        carreraLider = request.form['carreraintegranteLider']
        secretario = request.form['integranteSecretario']
        carreraSecre = request.form['carreraintegranteSecretario']
        investigador = request.form['integranteInvestigador']
        carreraInves = request.form['carreraintegranteInvestigador']
        diablo = request.form['integranteAbogadoDiablo']
        carreraDia = request.form['carreraintegranteAbobadoDiablo']
        nombreProyecto = request.form['nombreProyecto']
        descripcionProyecto = request.form['descripcionProyecto']
        sloganProyecto = request.form['slogan']
        logotipoProyecto = request.files['logotipo']
        mision = request.form['misionEmpresa']
        vision = request.form['visionEmpresa']
        unoObjetivoEstrategico = request.form['unoObjetivoEstrategico']
        unoObjetivoTactico = request.form['unoObjetivoTactico']
        unounoObjetivoOPerativo = request.form['unounoObjetivoOPerativo']
        unodosObjetivoOPerativo = request.form['unodosObjetivoOPerativo']
        dosObjetivoEstrategico = request.form['dosObjetivoEstrategico']
        dosObjetivoTactico = request.form['dosObjetivoTactico']
        dosunoObjetivoOPerativo = request.form['dosunoObjetivoOPerativo']
        dosdosObjetivoOPerativo = request.form['dosdosObjetivoOPerativo']
        pais = request.form['pais']
        region = request.form['region']
        ciudad = request.form['ciudad']
        coloniazona = request.form['coloniazona']
        nivelEducacion = request.form['niveldeeducacion']
        edad = request.form['edad']
        sexo = request.form['sexo']
        profesion = request.form['profesion']
        estiloVida = request.form['estilodevida']
        gustos = request.form['gustos']
        costumbres = request.form['costumbres']
        habitosCompra = request.form['habitosdecompra']
        nombreEmpresaUno = request.form['nombreempresauno']
        nombreEmpresaDos = request.form['nombreempresados']
        nombreEmpresaTres = request.form['nombreempresatres']
        sloganEmpresaUno = request.form['sloganempresauno']
        sloganEmpresaDos = request.form['sloganempresados']
        sloganEmpresaTres = request.form['sloganempresatres']
        logotipoEmpresas = request.files['logotipoempresas']
        estrategiasPublicidad = request.form['estrategiasdepublicidad']
        tablaCotizaciones = request.files['tabladecotizaciones']
        preguntaUno = request.form['pregunta1']
        preguntaUnoGrafica = request.files['pregunta1grafica']
        preguntaDos = request.form['pregunta2']
        preguntaDosGrafica = request.files['pregunta2grafica']
        preguntaTres = request.form['pregunta3']
        preguntaTresGrafica = request.files['pregunta3grafica']
        preguntaCuatro = request.form['pregunta4']
        preguntaCuatroGrafica = request.files['pregunta4grafica']
        preguntaCinco = request.form['pregunta5']
        preguntaCincoGrafica = request.files['pregunta5grafica']
        preguntaSeis = request.form['pregunta6']
        preguntaSeisGrafica = request.files['pregunta6grafica']
        preguntaSiete = request.form['pregunta7']
        preguntaSieteGrafica = request.files['pregunta7grafica']
        preguntaOcho = request.form['pregunta8']
        preguntaOchoGrafica = request.files['pregunta8grafica']
        preguntaNueve = request.form['pregunta9']
        preguntaNueveGrafica = request.files['pregunta9grafica']
        preguntaDiez = request.form['pregunta10']
        preguntaDiezGrafica = request.files['pregunta10grafica']
        fortalezas = request.form['fortalezas']
        oportunidades = request.form['oportunidades']
        debilidades = request.form['debilidades']
        amenazas = request.form['amenazas']
        diagramaFlujo = request.files['diagramadeflujo']
        inicio = request.form['inicio']
        inicioFotoUno = request.files['iniciofoto1']
        inicioFotoDos = request.files['iniciofoto2']
        desarrollo = request.form['desarrollo']
        desarrolloFotoUno = request.files['desarrollofoto1']
        desarrolloFotoDos = request.files['desarrollofoto2']
        resultados = request.form['resultados']
        resultadosFotoUno = request.files['resultadosfoto1']
        resultadosFotoDos = request.files['resultadosfoto2']

        #carpeta donde se guardaran imagenes de cada proyecto
        carpetaIma = time.strftime("%d-%m-%y-") + time.strftime("%H-%M-%S")
        os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma))

        #guardo el nombre carpeta en base de datos
        carpetaImagenes = carpetaIma

        #imagenes mejoramiento Quita cosas feas a la imagen
        if logotipoProyecto and allowed_file(logotipoProyecto.filename):
            nombreLogotipo = secure_filename(logotipoProyecto.filename)
            logotipoProyecto.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'Logotipo.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if logotipoEmpresas and allowed_file(logotipoEmpresas.filename):
            nombre = secure_filename(logotipoEmpresas.filename)
            logotipoEmpresas.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'LogotipoEmpresas.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if tablaCotizaciones and allowed_file(tablaCotizaciones.filename):
            nombreTabla = secure_filename(tablaCotizaciones.filename)
            tablaCotizaciones.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'TablaCotizaciones.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if preguntaUnoGrafica and allowed_file(preguntaUnoGrafica.filename):
            nombre = secure_filename(preguntaUnoGrafica.filename)
            preguntaUnoGrafica.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'GraficaPregunta1.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if preguntaDosGrafica and allowed_file(preguntaDosGrafica.filename):
            nombre = secure_filename(preguntaDosGrafica.filename)
            preguntaDosGrafica.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'GraficaPregunta2.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if preguntaTresGrafica and allowed_file(preguntaTresGrafica.filename):
            nombre = secure_filename(preguntaTresGrafica.filename)
            preguntaTresGrafica.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'GraficaPregunta3.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if preguntaCuatroGrafica and allowed_file(preguntaCuatroGrafica.filename):
            nombre = secure_filename(preguntaCuatroGrafica.filename)
            preguntaCuatroGrafica.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'GraficaPregunta4.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if preguntaCincoGrafica and allowed_file(preguntaCincoGrafica.filename):
            nombre = secure_filename(preguntaCincoGrafica.filename)
            preguntaCincoGrafica.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'GraficaPregunta5.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if preguntaSeisGrafica and allowed_file(preguntaSeisGrafica.filename):
            nombre = secure_filename(preguntaSeisGrafica.filename)
            preguntaSeisGrafica.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'GraficaPregunta6.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if preguntaSieteGrafica and allowed_file(preguntaSieteGrafica.filename):
            nombre = secure_filename(preguntaSieteGrafica.filename)
            preguntaSieteGrafica.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'GraficaPregunta7.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if preguntaOchoGrafica and allowed_file(preguntaOchoGrafica.filename):
            nombre = secure_filename(preguntaOchoGrafica.filename)
            preguntaOchoGrafica.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'GraficaPregunta8.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if preguntaNueveGrafica and allowed_file(preguntaNueveGrafica.filename):
            nombre = secure_filename(preguntaNueveGrafica.filename)
            preguntaNueveGrafica.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'GraficaPregunta9.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if preguntaDiezGrafica and allowed_file(preguntaDiezGrafica.filename):
            nombre = secure_filename(preguntaDiezGrafica.filename)
            preguntaDiezGrafica.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'GraficaPregunta10.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if diagramaFlujo and allowed_file(diagramaFlujo.filename):
            nombre = secure_filename(diagramaFlujo.filename)
            diagramaFlujo.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'DiagramaFlujo.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if inicioFotoUno and allowed_file(inicioFotoUno.filename):
            nombre = secure_filename(inicioFotoUno.filename)
            inicioFotoUno.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'InicioFoto1.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if inicioFotoDos and allowed_file(inicioFotoDos.filename):
            nombre = secure_filename(inicioFotoDos.filename)
            inicioFotoDos.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'InicioFoto2.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if desarrolloFotoUno and allowed_file(desarrolloFotoUno.filename):
            nombre = secure_filename(desarrolloFotoUno.filename)
            desarrolloFotoUno.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'DesarrolloFoto1.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if desarrolloFotoDos and allowed_file(desarrolloFotoDos.filename):
            nombre = secure_filename(desarrolloFotoDos.filename)
            desarrolloFotoDos.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'DesarrolloFoto2.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if resultadosFotoUno and allowed_file(resultadosFotoUno.filename):
            nombre = secure_filename(resultadosFotoUno.filename)
            resultadosFotoUno.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'ResultadosFoto1.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))


        if resultadosFotoDos and allowed_file(resultadosFotoDos.filename):
            nombre = secure_filename(resultadosFotoDos.filename)
            resultadosFotoDos.save(os.path.join(app.config['UPLOAD_FOLDER'], carpetaIma, 'ResultadosFoto2.png'))
        else:
            flash('La imagen debe ser de extencion .png', 'CategoriaError')
            return redirect(url_for('formularioAlumno'))



       #GUARDANDO EN LA BASE DE DATOS
        # tabla equipo
        try:
            if carrera == 'otro':
                equipo = Equipo(areadesarrollo, re.sub(' +', ' ', periodo).strip(), lider, carreraLider,
                            secretario, carreraSecre, investigador, carreraInves, diablo, carreraDia)
                db.session.add(equipo)
                db.session.commit()
            else:
                equipo = Equipo(carrera, re.sub(' +', ' ', periodo).strip(), lider, carreraLider,
                            secretario, carreraSecre, investigador, carreraInves, diablo, carreraDia)
                db.session.add(equipo)
                db.session.commit()
                flash('Was successfully added 1')

        except TimeoutError:
            flash('Error intente mas tarde', 'error')

        except IntegrityError:
            flash('Usuario ya existe', 'error')

        except (IOError, OSError):
            db.session.delete(equipo)
            db.session.commit()

        # tabla proyecto
        try:
            proyecto = Proyecto(equipo.idEquipo, nombreProyecto, descripcionProyecto, sloganProyecto, carpetaImagenes,
                            mision, vision, unoObjetivoEstrategico, unoObjetivoTactico, unounoObjetivoOPerativo,
                            unodosObjetivoOPerativo, dosObjetivoEstrategico, dosObjetivoTactico, dosunoObjetivoOPerativo,
                            dosdosObjetivoOPerativo, pais, region, ciudad, coloniazona, nivelEducacion, edad, sexo,
                            profesion, estiloVida, gustos, costumbres, habitosCompra, nombreEmpresaUno, nombreEmpresaDos,
                            nombreEmpresaTres, sloganEmpresaUno, sloganEmpresaDos, sloganEmpresaTres,
                            estrategiasPublicidad, preguntaUno, preguntaDos, preguntaTres, preguntaCuatro, preguntaCinco,
                            preguntaSeis, preguntaSiete, preguntaOcho, preguntaNueve, preguntaDiez, fortalezas,
                            oportunidades, debilidades, amenazas, inicio, desarrollo, resultados)
            db.session.add(proyecto)
            db.session.commit()

            flash('Was successfully added 1')

        except TimeoutError:
            flash('Error intente mas tarde', 'error')

        except IntegrityError:
            flash('Usuario ya existe', 'error')

        except (IOError,OSError):
            db.session.delete(proyecto)
            db.session.commit()

        return redirect(url_for('exito'))
    else:
        return redirect(url_for('formularioAlumno'))


@app.route('/exito')
def exito():
    if 'username' in session:
        respuesta = make_response(render_template('exito.html'))
        respuesta.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return respuesta
    else:
        return redirect(url_for('alumno'))




#PROFESOR
@app.route('/profesor')
def profesor():
    if 'usernameProfesor' in session:
        respuestaProfesor = make_response(redirect(url_for('paginaProfesor')))
        respuestaProfesor.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return respuestaProfesor
    else:
        return render_template("conProfesor.html")


@app.route('/loginProfesor', methods=['POST', 'GET'])
def loginProfesor():
    if request.method == 'POST':
        usuarioProfesor = request.form['usuarioProfesor']
        contraProfesor = request.form['contraProfesor']

        try:
            usuProf = TblDatosI.query.filter_by(usuProfesor="gema").first()
        except TimeoutError:
            flash('Error no se puede cargar datos', 'error')

        if usuarioProfesor == usuProf.usuProfesor and bcrypt.check_password_hash(usuProf.conProfesor, contraProfesor):
            session['usernameProfesor'] = 'prof'
            return redirect(url_for('paginaProfesor'))
        else:
            return redirect(url_for('profesor'))
    else:
        return redirect(url_for('profesor'))


@app.route('/paginaProfesor')
@app.route('/paginaProfesor/<int:pagina>', methods=['GET', 'POST'])
def paginaProfesor(pagina=1):

    if 'usernameProfesor' in session:
        try:
            respuestaProfesor = make_response(render_template('profesor.html',
                            proyectos=Equipo.query.join(Proyecto).add_columns(Equipo.idEquipo, Equipo.periodo,
                                        Equipo.carrera, Proyecto.nombreProyecto).paginate(pagina, POSTS_PER_PAGE,
                                                    False)))

        except TimeoutError:
            flash('Error no se puede cargar dato', 'error')

        respuestaProfesor.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return respuestaProfesor
    else:
        return redirect(url_for('profesor'))


@app.route('/paginaProfesorCarrera/<buscar>')
@app.route('/paginaProfesorCarrera/<buscar>/<int:pagina>')
def paginaProfesorCarrera(buscar, pagina=1):

    if 'usernameProfesor' in session:
        try:
            respuestaProfesor = make_response(render_template('profesorCarrera.html',
                                                              proyectos=Equipo.query.join(Proyecto).add_columns(
                                                                  Equipo.idEquipo, Equipo.periodo, Equipo.carrera,
                                                                  Proyecto.nombreProyecto).filter(Equipo.carrera.like(
                                                                  '%' + buscar + '%')).paginate(pagina,
                                                                                                       POSTS_PER_PAGE,
                                                                                                       False),
                                                              buscar=buscar))
        except TimeoutError:
            flash('Error no se puede cargar dato', 'error')

        respuestaProfesor.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return respuestaProfesor
    else:
        return redirect(url_for('profesor'))


@app.route('/paginaProfesorPeriodo/<buscar2>')
@app.route('/paginaProfesorPeriodo/<buscar2>/<int:pagina>')
def paginaProfesorPeriodo(buscar2, pagina=1):

    if 'usernameProfesor' in session:
        try:
            respuestaProfesor = make_response(render_template('profesorPeriodo.html',
                                                              proyectos=Equipo.query.join(Proyecto).add_columns(
                                                                  Equipo.idEquipo, Equipo.periodo, Equipo.carrera,
                                                                  Proyecto.nombreProyecto).filter(Equipo.periodo.like(
                                                                  '%' + buscar2 + '%')).paginate(pagina,
                                                                                                       POSTS_PER_PAGE,
                                                                                                       False),
                                                              buscar2=buscar2))

        except TimeoutError:
            flash('Error no se puede cargar dato', 'error')

        respuestaProfesor.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return respuestaProfesor
    else:
        return redirect(url_for('profesor'))


@app.route('/paginaProfesorCarreraPeriodo/<buscar>/<buscar2>')
@app.route('/paginaProfesorCarreraPeriodo/<buscar>/<buscar2>/<int:pagina>')
def paginaProfesorCarreraPeriodo(buscar, buscar2, pagina=1):

    if 'usernameProfesor' in session:
        try:
            respuestaProfesor = make_response(render_template('profesorCarreraPeriodo.html',
                                                              proyectos=Equipo.query.join(Proyecto).add_columns(Equipo.idEquipo,
                                                                        Equipo.periodo, Equipo.carrera,
                                                                        Proyecto.nombreProyecto).filter(Equipo.carrera.like('%'+buscar+'%')).filter(Equipo.periodo.like('%'+buscar2+'%')).paginate(pagina, POSTS_PER_PAGE, False),
                                                              buscar=buscar,
                                                              buscar2=buscar2))
        except TimeoutError:
            flash('Error no se puede cargar datos', 'error')

        respuestaProfesor.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return respuestaProfesor
    else:
        return redirect(url_for('profesor'))


@app.route('/cambiarContraAlumno')
def cambiarContraAlumno():
    formularioCambiarContraAlumno = CambiarContraAlumno(request.form)
    if 'usernameProfesor' in session:
        respuestaProfesor = make_response(render_template('cambiarContraAlumno.html', formularioCamContraAlum=formularioCambiarContraAlumno))
        respuestaProfesor.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return respuestaProfesor
    else:
        return redirect(url_for('profesor'))


class CambiarContraAlumno(FlaskForm):
    nuevaContraAlumno = PasswordField(u"Ingrese la nueva contraseña:", validators=[InputRequired(), Length(5, 25, u'la contraseña debe de ser minimo de 5 caracteres')])
    nuevaContraAlumnoOtraVez = PasswordField(u"Ingrese la nueva contraseña otra vez:", validators=[InputRequired(), EqualTo('nuevaContraAlumno', u'no coinciden las contraseñas') ])
    botonCambiarContra = SubmitField("Cambiar")


#
@app.route('/validarCambiarContraAlumno', methods=['POST', 'GET'])
def validarCambiarContraAlumno():
    if 'usernameProfesor' in session:
        formulario = CambiarContraAlumno(request.form)
        if request.method == 'POST' and formulario.validate():

            try:
                newconA = TblDatosI.query.filter_by(usuProfesor="gema").first()

            except TimeoutError:
                flash('Error cambiar contra')

            newconA.conAlumno = bcrypt.generate_password_hash(formulario.nuevaContraAlumno.data)
            db.session.commit()

            flash('se cambio','exito')
            return redirect(url_for('cambiarContraAlumno'))
        else:
            respuestaProfesor = make_response(render_template('cambiarContraAlumno.html', formularioCamContraAlum=formulario))
            respuestaProfesor.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
            return respuestaProfesor

    else:
        return redirect(url_for('profesor')) #TODO linea agregada


@app.route('/cambiarContraProfesor')
def cambiarContraProfesor():
    formularioCambiarContraProfe = CambiarContraProfesor(request.form)
    if 'usernameProfesor' in session:
        respuestaProfesor = make_response(render_template('cambiarContraProfesor.html',  formularioCamContraProf=formularioCambiarContraProfe))
        respuestaProfesor.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return respuestaProfesor
    else:
        return redirect(url_for('profesor'))

class CambiarContraProfesor(FlaskForm):
    nuevaContraProfesor = PasswordField(u"Ingrese la nueva contraseña", validators=[InputRequired(), Length(5, 25, u'la contraseña debe de ser minimo de 5 caracteres')])
    nuevaContraProfesorOtraVez = PasswordField(u"Ingrese la nueva contraseña otra vez:", validators=[InputRequired(), EqualTo('nuevaContraProfesor', u'no coinciden las contraseñas') ])
    botonCambiarContra = SubmitField("Cambiar")

@app.route('/validarCambiarContraProfesor', methods=['POST', 'GET'])
def validarCambiarContraProfesor():
    if 'usernameProfesor' in session:
        formulario = CambiarContraProfesor(request.form)
        if request.method == 'POST' and formulario.validate():

            try:
                newconP = TblDatosI.query.filter_by(usuProfesor="gema").first()
            except TimeoutError:
                flash('Error intente mas tarde', 'error')

            newconP.conProfesor = bcrypt.generate_password_hash(formulario.nuevaContraProfesor.data)
            db.session.commit()

            flash('se cambio contra Prof', 'exito')
            return redirect(url_for('cambiarContraProfesor'))
        else:
            respuestaProfesor = make_response(render_template('cambiarContraProfesor.html', formularioCamContraProf=formulario))
            respuestaProfesor.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
            return respuestaProfesor
    else:
        return redirect(url_for('profesor'))


@app.route('/buscarProyectos', methods=['POST', 'GET'])
def buscarProyectos():
    if 'usernameProfesor' in session:

        if request.method == 'POST':
            buscarPeriodo = request.form['BuscarPeriodo']
            buscarCarrera = request.form['BuscarCarrera']

            if buscarPeriodo == '' and buscarCarrera == '':
                pass
            else:
                if buscarPeriodo == '':
                    return redirect(url_for('paginaProfesorCarrera', buscar=buscarCarrera))

                elif buscarCarrera == '':
                    return redirect(url_for('paginaProfesorPeriodo', buscar2=buscarPeriodo))

                else:
                    return redirect(url_for('paginaProfesorCarreraPeriodo', buscar=buscarCarrera, buscar2=buscarPeriodo))

        return redirect(url_for('paginaProfesor'))
    else:
        return redirect(url_for('profesor'))


@app.route('/verProyecto/<idequipo>')
def verProyecto(idequipo):
    if 'usernameProfesor' in session:
        equipo = idequipo

        try:
            proyectos = Equipo.query.join(Proyecto).filter(Equipo.idEquipo == equipo).first()
        except TimeoutError:
            flash('Error intente mas tarde', 'error')

        try:
            respuesta = make_response(render_template('verProyecto.html', proyectos=Equipo.query.join(Proyecto).filter(Equipo.idEquipo==equipo).first()))
        except TimeoutError:
            flash('no se puede cargar los datos', 'error')

        respuesta.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return respuesta
    else:
        return render_template("conProfesor.html")




if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
