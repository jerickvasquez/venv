from devsnets.client import Client
from devsnets.computer_vision.object_detection.utils import Video, show_frame
from owlready2 import *
import json
import os
from cv2 import cv2
from tkinter import *
import tkinter
import tkinter as tk
from tkinter import ttk, font
from tkinter import scrolledtext as st
import statistics as stats
from ttkthemes import ThemedTk
import ttkthemes
import random

onto = get_ontology("file://C:/Users/achev/Documents/Carro.owl")
onto.load(reload = True)
Carro = "Carro." 
reemplazar_por = "" 
raiz = Tk()

NombreUsuario = StringVar ()
Mensaje = StringVar ()
EdadUsuario = IntVar ()
MarcaWE234 = StringVar ()
MarcaRTY456 = StringVar ()
MarcaZX1922 = StringVar ()
GeneroUsuario = StringVar ()
SelCarro = StringVar()
NivelDeEstudioUsuario = StringVar ()
FacilidadPercibidadUsuario = IntVar ()
DisfrutePercibidoUsuario = IntVar ()
ObtenerWE234 = StringVar ()
ObtenerRTY456 = StringVar ()
ObtenerZX1922 = StringVar ()
ReputacionWE234 = StringVar ()
ReputacionRTY456 = StringVar ()
ReputacionZX1922 = StringVar ()
ComentariosWE234 = StringVar ()
ComentariosZX1922 = StringVar ()
ComentariosRTY456 = StringVar ()
Inicio = StringVar ()
FinalWE234 = StringVar ()
FinalRTY456 = StringVar ()
FinalZX1922 = StringVar ()
resultadopromedio = StringVar()
resultadofacilidad = StringVar()
resultadodisfrute = StringVar ()
MayorEdad = StringVar ()

class Ontologia:
    def Inferencias(self):
        """ Se hacen una variedad de inferencias relacionadas con la ontologia
        """
        self.GeneroMasculinoDisfrute = 0
        self.GeneroFemeninoDisfrute = 0
        self.GeneroMasculinoFacilidad = 0
        self.GeneroFemeninoFacilidad = 0
        self.EdadValor = 0
        self.NumeroUsuarios = 0
        self.ValorGeneroFacilidad = ""
        self.ValorGeneroDisfrute = ""
        self.valoredad = 0
        self.EdadMayor = 0
        for i in onto.Usuario.instances(): 
            self.NumeroUsuarios = 1 + self.NumeroUsuarios
            for prop in i.get_properties():
                for value in prop[i]:
                    if prop.python_name == "Facilidad_percibida_de_uso" and value>59:
                        for prop in i.get_properties():
                            for value in prop[i]:
                                if prop.python_name == "Genero":
                                    if str(value) == "Masculino":
                                        self.GeneroMasculinoFacilidad = 1 + self.GeneroMasculinoFacilidad
                                    elif str(value) == "Femenino":
                                        self.GeneroFemeninoFacilidad = 1 + self.GeneroFemeninoFacilidad             
                        if self.GeneroMasculinoFacilidad >= self.GeneroFemeninoFacilidad:
                            self.ValorGeneroFacilidad = "Masculino"
                        if self.GeneroMasculinoFacilidad <= self.GeneroFemeninoFacilidad:
                            self.ValorGeneroFacilidad = "Femenino"
                    if prop.python_name == "Disfrute_percibido" and value>59:
                        for prop in i.get_properties():
                            for value in prop[i]:
                                if prop.python_name == "Genero":
                                    if str(value) == "Masculino":
                                        self.GeneroMasculinoDisfrute = 1 + self.GeneroMasculinoDisfrute
                                    elif str(value) == "Femenino":
                                        self.GeneroFemeninoDisfrute = 1 + self.GeneroFemeninoDisfrute
                        if self.GeneroMasculinoDisfrute >= self.GeneroFemeninoDisfrute:
                            self.ValorGeneroDisfrute= "Masculino"
                        if self.GeneroMasculinoDisfrute <= self.GeneroFemeninoDisfrute:
                            self.ValorGeneroDisfrute = "Femenino"
                    if prop.python_name == "Edad":
                        self.EdadValor = int(value) + self.EdadValor
                        self.valoredad = int(value)
                    if self.EdadMayor < self.valoredad:
                        self.EdadMayor = self.valoredad

        if self.NumeroUsuarios==0:
            self.NumeroUsuarios=1
        PromedioEdad = (self.EdadValor / self.NumeroUsuarios)
        MayorEdad.set(self.EdadMayor)           
        resultadopromedio.set(round(PromedioEdad))
        resultadodisfrute.set(self.ValorGeneroDisfrute)
        resultadofacilidad.set(self.ValorGeneroFacilidad)
class Detecciones:
    
    def DeteccionObjetos(self):
        """Implementacion de la deteccion de objetos
        Se utiliza Yolo el cual es uno de los modelos de detección de objetos más versatiles y modernos.
        El modelo usado es Yolov5 Pytorch 
        """

        nuevo = Persona()
        print ("El carro selecionado es :",SelCarro.get())
        client = Client(logging=True, inputs='data/inputs', outputs='data/outputs')
        yolov5 = client.get('yolov5', version='extra-large')
        yolov5.load_weights('coco')
        yolov5.to_cpu()
        conteototal = 0
        conteo80= 0
        certezas = {}
        PromedioCerteza = []
        #El iou es sobre que tan bien hace el recuadro. Que tan preciso es en encuadrar los objetos
        #El conf es que tan preciso es en detectar la clase de objeto
        yolov5.set(iou_thres=0.01, conf_thres=0.6)
        if SelCarro.get() == "rty456":
            video = Video(os.path.join('videos', 'rty456.mp4'))
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            out_video = cv2.VideoWriter(os.path.join('data','outputs', 'rty456.avi'), fourcc, video.fps, (video.width, video.height))

        elif SelCarro.get() == 'we234':
            video = Video(os.path.join('videos', 'we234.mp4'))
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            out_video = cv2.VideoWriter(os.path.join('data','outputs', 'we234.avi'), fourcc, video.fps, (video.width, video.height))
        elif SelCarro.get() == 'zx1922':
            video = Video(os.path.join('videos', 'zx1922.mp4'))
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            out_video = cv2.VideoWriter(os.path.join('data','outputs', 'zx1922.avi'), fourcc, video.fps, (video.width, video.height))
        
        try:
            for output in yolov5.detect(video, draw_detections=True):
                    conteototal = conteototal + len(output['detections'])
                    print(f'\n[{output["frame_number"]}/{output["frames_count"]}]:', json.dumps(output["detections"], indent=4))
                    show_frame(output['detected_frame'])
                    out_video.write(output['detected_frame'])
                    for detection in output['detections']:
                        if detection['class_name'] not in certezas:
                            certezas[detection['class_name']] = [detection['confidence']]
                        else:
                            certezas[detection['class_name']].append(detection['confidence'])
                        
                        if detection['confidence'] >= 0.70:
                            conteo80 = conteo80 + 1
            
        except KeyboardInterrupt:
            pass
        
        out_video.release()
        yolov5.unload()
        client.close()
        print()
        self.probabilidad = (conteo80/conteototal)*100

        
        for class_name in certezas.keys():
            certeza_promedio = int(stats.mean(certezas[class_name])*100)
            PromedioCerteza.append(str(class_name) + ": " + str(certeza_promedio) + "%")
        
        self.certeza = '\n'.join([str(i) for i in PromedioCerteza])
        


class Persona:
    def NuevoUsuario(self):
        """Se crea un nuevo usuario en la ontología el cual decidio realizar un viaje 
        """
        d = Detecciones()
        d.DeteccionObjetos()
        self.probabilidad = d.probabilidad
        self.window = tk.Toplevel(p1)
        self.window.resizable(True, True)
        self.PromedioObjetoCerteza = d.certeza
        ttk.Label(self.window,text="Carro seleccionado : ").grid(row=0, column=0)
        ttk.Entry(self.window, justify=CENTER, state=DISABLED, textvariable=SelCarro).grid(row=0, column=1)
        print("La probabilidad es : ",self.probabilidad)
        Label(self.window)

        ttk.Label(self.window, text="\nPromedio de certezas por cada clase : ").grid(row=1, column=0)

        scrolledtext4=st.ScrolledText(self.window, width=60, height=1)
        scrolledtext4.grid(column=1,row=1 ,padx=10, pady=5)
        scrolledtext4.insert("1.0",self.PromedioObjetoCerteza)
        scrolledtext4.configure(state ='disabled') 

        ttk.Label(self.window, text="Indique su nombre : ").grid(row=2, column=0)
        ttk.Entry(self.window, justify=CENTER, textvariable=NombreUsuario, width=25).grid(row=2, column=1)

        Label(self.window)

        ttk.Label(self.window, text="Indique su edad : ").grid(row=3, column=0)
        ttk.Entry(self.window, justify=CENTER, textvariable=EdadUsuario, width=25).grid(row=3, column=1)

        Label(self.window)

        ttk.Label(self.window, text="Indique su genero : ").grid(row=4, column=0)
        ttk.Entry(self.window, justify=CENTER, textvariable=GeneroUsuario, width=25).grid(row=4, column=1)

        Label(self.window)

        ttk.Label(self.window, text="Indique su nivel de estudio").grid(row=5, column=0)
        ttk.Entry(self.window, justify=CENTER, textvariable=NivelDeEstudioUsuario, width=25).grid(row=5, column=1)

        Label(self.window)

        ttk.Label(self.window, text="Indique el disfrute que percibio").grid(row=6, column=0)
        ttk.Entry(self.window, justify=CENTER, textvariable=DisfrutePercibidoUsuario, width=25).grid(row=6, column=1)

        Label(self.window)

        ttk.Label(self.window, text="Indique la facilidad que percibio").grid(row=7, column=0)
        ttk.Entry(self.window, justify=CENTER, textvariable=FacilidadPercibidadUsuario, width=25).grid(row=7, column=1)

        Label(self.window)

        ttk.Label(self.window, text="Como fue la experiencia vivida").grid(row=8, column=0)
        ttk.Entry(self.window, justify=CENTER, textvariable=Mensaje, width=25).grid(row=8, column=1)

        ttk.Button(self.window, text="Registrar", command=self.BotonUsuario).grid(row=10, column=1)
        
        self.window.style = ttkthemes.ThemedStyle()
        self.window.style.theme_use('breeze')
    def BotonUsuario(self):
        """ Metodo donde se realiza el ingreso del nuevo usuario y se guarda la ontologia con los
        cambios correspondiente"""
        carroau = CarroAutonomo()
        print("La probabilidad es : ",self.probabilidad)
        print("El mensaje es : ",Mensaje.get())
        Usuarios = onto.Usuario(NombreUsuario.get(), Edad = [(EdadUsuario.get())],Genero = [GeneroUsuario.get()], Nivel_de_estudio=[NivelDeEstudioUsuario.get()],Facilidad_percibida_de_uso=[(FacilidadPercibidadUsuario.get())], Disfrute_percibido=[(DisfrutePercibidoUsuario.get())] )
        if SelCarro.get()== 'we234':
            onto.WE234.comment.append(Mensaje.get() +". Autor:" + NombreUsuario.get())
        elif SelCarro.get() == 'rty456':
            onto.RTY456.comment.append(Mensaje.get() +". Autor:" + NombreUsuario.get())
        elif SelCarro.get() == 'zx1922':
            onto.ZX1922.comment.append(Mensaje.get() +". Autor:" + NombreUsuario.get())
        carroau.Reputacion(SelCarro.get(),round(self.probabilidad),Usuarios,FacilidadPercibidadUsuario.get(),DisfrutePercibidoUsuario.get())
        onto.save(file = "C:/Users/achev/Documents/Carro.owl" , format = "rdfxml")
        SelCarro.set('')
        NombreUsuario.set('')
        EdadUsuario.set('')
        GeneroUsuario.set('')
        NivelDeEstudioUsuario.set('')
        DisfrutePercibidoUsuario.set('')
        FacilidadPercibidadUsuario.set('')
        Mensaje.set('')
        carroau.SeleccionCarro()
        self.window.destroy()
        raiz.destroy()
        

class CarroAutonomo:
    def Reputacion(self, Carro, Probabilidad, Persona, Facilidad, Disfrute):
        """
        Se asigna la nueva reputación en la ontologia al vehiculo el cual fue seleccionado por el usuario.

        A partir de la investigación se decidio realizar la formula donde intervienen diferentes
        aspectos como Los sensores del vehiculo, el historico de reputación que posee este, entre otros.

        Parametros:
        Carro --> Cual fue el carro seleccionado por el usuario
        Probabilidad --> Cual fue la probabilidad de que un objeto tenga una certeza del 80% o mayor 
        Persona --> La persona la cual decidio realizar un viaje en un determinado carro
        Facilidad --> Cual fue la facilidad que encontro la persona en el vehiculo al realizar el viaje
        Disfrute --> Cual fue el disfrute que encontro la persona en el vehiculo al realizar el viaje 
        
        Variables importantes:
        Percepcioninicial --> Es el número de sensores que posee el vehiculo
        """
        PercepcionInicial = 0
        CarroWE234Lleva = 0
        CarroRTY456Lleva = 0
        CarroZX1922Lleva = 0
        if Carro == 'rty456':
            onto.RTY456.Lleva.append(Persona)
            for prop in onto.RTY456.get_properties():
                for value in prop[onto.RTY456]:
                    if value is True:
                        PercepcionInicial = PercepcionInicial +1
                    if prop.python_name == "Lleva":
                        CarroRTY456Lleva = CarroRTY456Lleva + 1
            onto.RTY456.Percepción_inicial.clear()
            if CarroRTY456Lleva ==0:
                CarroRTY456Lleva =1
            onto.RTY456.Percepción_inicial.append(PercepcionInicial*10)
            HistoricoReputacion = onto.RTY456.Historico_reputacion[0]
            Reputacion = onto.RTY456.Reputacion_Carro[0]
            onto.RTY456.Reputacion_Carro.clear()
            #Dividir el historico de reputación sobre CarroRTY45Lleva
            print("El historico de reputacion es :", HistoricoReputacion)
            Reputacion = ((((PercepcionInicial*10)+ round(Probabilidad))/2) * 0.20) + round(HistoricoReputacion/CarroRTY456Lleva) * 0.50 + (((Facilidad)+(Disfrute))/2) * 0.30
            onto.RTY456.Reputacion_Carro.append(round(Reputacion))
            onto.RTY456.Historico_reputacion.clear()
            print("La reputacion es ", Reputacion)
            #Sumar Historico de reputación a la formula siguiente
            HistoricoReputacion =  Reputacion + HistoricoReputacion
            print("El historico de reputacion es despues de la formula:", HistoricoReputacion)
            onto.RTY456.Historico_reputacion.append(round(HistoricoReputacion))
            print("La nueva reputación del carro RTY456 es :",Reputacion)

        if Carro == 'we234':
            onto.WE234.Lleva.append(Persona)
            for prop in onto.WE234.get_properties():
                for value in prop[onto.WE234]:
                    if value is True:
                        PercepcionInicial = PercepcionInicial +1
                    if prop.python_name == "Lleva":
                        CarroWE234Lleva = CarroWE234Lleva + 1
            onto.WE234.Percepción_inicial.clear()
            if CarroWE234Lleva ==0:
                CarroWE234Lleva =1
            onto.WE234.Percepción_inicial.append(PercepcionInicial*10)
            HistoricoReputacion = onto.WE234.Historico_reputacion[0]
            Reputacion = onto.WE234.Reputacion_Carro[0]
            onto.WE234.Reputacion_Carro.clear()
            Reputacion = ((((PercepcionInicial*10)+ round(Probabilidad))/2) * 0.20) + round(HistoricoReputacion/CarroWE234Lleva) * 0.50 + (((Facilidad)+(Disfrute))/2) * 0.30
            onto.WE234.Reputacion_Carro.append(round(Reputacion))
            onto.WE234.Historico_reputacion.clear()
            HistoricoReputacion =  Reputacion + HistoricoReputacion
            onto.WE234.Historico_reputacion.append(round(HistoricoReputacion))
            print("La nueva reputación del carro WE234 es :",Reputacion)

        if Carro == 'zx1922':
            onto.ZX1922.Lleva.append(Persona)
            for prop in onto.ZX1922.get_properties():
                for value in prop[onto.ZX1922]:
                    if value is True:
                        PercepcionInicial = PercepcionInicial +1
                    if prop.python_name == "Lleva":
                        CarroZX1922Lleva = CarroZX1922Lleva + 1
            onto.ZX1922.Percepción_inicial.clear()
            if CarroZX1922Lleva ==0:
                CarroZX1922Lleva =1
            onto.ZX1922.Percepción_inicial.append(PercepcionInicial*10)
            HistoricoReputacion = onto.ZX1922.Historico_reputacion[0]
            print("Historico de reputación viejo :",HistoricoReputacion)
            Reputacion = onto.ZX1922.Reputacion_Carro[0]
            onto.ZX1922.Reputacion_Carro.clear()
            Reputacion = ((((PercepcionInicial*10)+ round(Probabilidad))/2) * 0.20) + round(HistoricoReputacion/CarroZX1922Lleva) * 0.50 + (((Facilidad)+(Disfrute))/2) * 0.30
            onto.ZX1922.Reputacion_Carro.append(round(Reputacion))
            onto.ZX1922.Historico_reputacion.clear()
            HistoricoReputacion =  Reputacion + HistoricoReputacion
            print("Historico de reputación nuevo :",HistoricoReputacion)
            onto.ZX1922.Historico_reputacion.append(round(HistoricoReputacion))
            print("La nueva reputación del carro ZX1922 es :",Reputacion)

    def SeleccionCarro(self):
        """El usuario selecciona el vehiculo el cual usara para el viaje 
        """
        for i in list(onto.individuals()):
            if str(i) == "Carro.WE234":
                pcomenwe234 = '\n'.join([str(i) for i in onto.WE234.comment])
                ComentariosWE234.set(pcomenwe234)
                for prop in onto.WE234.get_properties():
                    for value in prop[onto.WE234]:
                        if prop.python_name == "Inicia":
                            valorinicio = str(value)
                            Inicio.set(valorinicio.replace(Carro, reemplazar_por))
                        elif prop.python_name== "Termina":
                            valorfinal = str(value)
                            FinalWE234.set(valorfinal.replace(Carro, reemplazar_por))
                        elif prop.python_name== "Reputacion_Carro":
                            valorreputacion = int(value)
                            ReputacionWE234.set(valorreputacion)
                        elif prop.python_name== "Marca_Carro":
                            valorMarca = str(value)
                            MarcaWE234.set(valorMarca)
                print("")            
            if str(i) == "Carro.RTY456":
                pcomenrty456 = '\n'.join([str(i) for i in onto.RTY456.comment])
                ComentariosRTY456.set(pcomenrty456)     
                for prop in onto.RTY456.get_properties():
                    for value in prop[onto.RTY456]:
                        if prop.python_name == "Inicia":
                            valorinicio = str(value)
                            Inicio.set(valorinicio.replace(Carro, reemplazar_por))
                        elif prop.python_name== "Termina":
                            valorfinal = str(value)
                            FinalRTY456.set(valorfinal.replace(Carro, reemplazar_por))
                        elif prop.python_name== "Reputacion_Carro":
                            valorreputacion = int(value)
                            ReputacionRTY456.set(valorreputacion)
                        elif prop.python_name== "Marca_Carro":
                            valorMarca = str(value)
                            MarcaRTY456.set(valorMarca)
                print("")
            if str(i) == "Carro.ZX1922":
                pcomenzx1922 = '\n'.join([str(i) for i in onto.ZX1922.comment])
                ComentariosZX1922.set(pcomenzx1922)  
                for prop in onto.ZX1922.get_properties():
                    for value in prop[onto.ZX1922]:
                        if prop.python_name == "Inicia":
                            valorinicio = str(value)
                            Inicio.set(valorinicio.replace(Carro, reemplazar_por))
                        elif prop.python_name== "Termina":
                            valorfinal = str(value)
                            FinalZX1922.set(valorfinal.replace(Carro, reemplazar_por))
                        elif prop.python_name== "Reputacion_Carro":
                            valorreputacion = int(value)
                            ReputacionZX1922.set(valorreputacion)
                        elif prop.python_name== "Marca_Carro":
                            valorMarca = str(value)
                            MarcaZX1922.set(valorMarca)


d = Detecciones()
onty = Ontologia()
per = Persona ()
car = CarroAutonomo()
onty.Inferencias()
car.SeleccionCarro()

raiz.title("Modelado de confianza en los vehiculos autonomos")
fuente = font.Font(weight='bold')
raiz.config(bd=15)
raiz.resizable(True, True)
raiz.grid_columnconfigure((0,1), weight=1)

""" Incluimos el panel de pestañas"""
nb = ttk.Notebook(raiz)
nb.pack(fill='both', expand='yes')

p1 = ttk.Frame(nb)
p1.pack()
p2 = ttk.Frame(nb)

nb.add(p1,text='Viaje')
nb.add(p2,text='Inferencias')



"""Campos pertenecientes al vehiculo WE234 """
ttk.Label(p1, text="\nComentarios del vehiculo WE234").grid(row=0, column=0)

scrolledtext1=st.ScrolledText(p1, width=60, height=1)
scrolledtext1.grid(column=1,row=0 ,padx=10, pady=5)
scrolledtext1.insert("1.0", ComentariosWE234.get())
scrolledtext1.configure(state ='disabled')  

ttk.Label(p1, text="\nMarca de Carro").grid(row=1, column=0)
ttk.Entry(p1, justify=CENTER, state=DISABLED, textvariable=MarcaWE234, width=25).grid(row=1, column=1)

ttk.Label(p1, text="\nInicio del viaje").grid(row=2, column=0)
ttk.Entry(p1, justify=CENTER, state=DISABLED, textvariable=Inicio, width=25).grid(row=2, column=1)

ttk.Label(p1, text="\nFinal del viaje").grid(row=3, column=0)
ttk.Entry(p1, justify=CENTER, state=DISABLED, textvariable=FinalWE234, width=25).grid(row=3, column=1)

ttk.Label(p1, text="\nReputación actual").grid(row=4, column=0)
ttk.Entry(p1, justify=CENTER, state=DISABLED, textvariable=ReputacionWE234, width=25).grid(row=4, column=1)

Label(p1)

"""Campos pertenecientes al vehiculo RTY456 """
ttk.Label(p1, text="\nComentarios del vehiculo RTY456").grid(row=5, column=0)

scrolledtext2=st.ScrolledText(p1, width=60, height=1)
scrolledtext2.grid(column=1,row=5 ,padx=10, pady=5)
scrolledtext2.insert("1.0", ComentariosRTY456.get())
scrolledtext2.configure(state ='disabled')  

ttk.Label(p1, text="\nMarca de Carro").grid(row=6, column=0)
ttk.Entry(p1, justify=CENTER, state=DISABLED, textvariable=MarcaRTY456, width=25).grid(row=6, column=1)

ttk.Label(p1, text="\nInicio del viaje").grid(row=7, column=0)
ttk.Entry(p1, justify=CENTER, state=DISABLED, textvariable=Inicio, width=25).grid(row=7, column=1)



ttk.Label(p1, text="\nFinal del viaje").grid(row=8, column=0)
ttk.Entry(p1, justify=CENTER, state=DISABLED, textvariable=FinalRTY456, width=25).grid(row=8, column=1)

ttk.Label(p1, text="\nReputación actual").grid(row=9, column=0)
ttk.Entry(p1, justify=CENTER, state=DISABLED, textvariable=ReputacionRTY456, width=25).grid(row=9, column=1)

Label(p1)

"""Campos pertenecientes al vehiculo ZX1922 """
ttk.Label(p1, text="\nComentarios del vehiculo ZX1922").grid(row=10, column=0)

scrolledtext3=st.ScrolledText(p1, width=60, height=1)
scrolledtext3.grid(column=1,row=10 ,padx=10, pady=5)
scrolledtext3.insert("1.0", ComentariosZX1922.get())
scrolledtext3.configure(state ='disabled')  

ttk.Label(p1, text="\nMarca de Carro").grid(row=11, column=0)
ttk.Entry(p1, justify=CENTER, state=DISABLED, textvariable=MarcaZX1922, width=25).grid(row=11, column=1)

ttk.Label(p1, text="\nInicio del viaje").grid(row=12, column=0)
ttk.Entry(p1, justify=CENTER, state=DISABLED, textvariable=Inicio, width=25).grid(row=12, column=1)

ttk.Label(p1, text="\nFinal del viaje").grid(row=13, column=0)
ttk.Entry(p1, justify=CENTER, state=DISABLED, textvariable=FinalZX1922, width=25).grid(row=13, column=1)

ttk.Label(p1, text="\nReputación actual").grid(row=14, column=0)
ttk.Entry(p1, justify=CENTER, state=DISABLED, textvariable=ReputacionZX1922, width=25).grid(row=14, column=1)

ttk.Separator(p1, orient='horizontal')

ttk.Label(p1, text="Seleccione un carro").grid(row=15, column=0)


CampoSeleccionVehiculo = ttk.Entry(p1, justify=CENTER, textvariable=SelCarro, width=25)

CampoSeleccionVehiculo.grid(row=15, column=1)
ttk.Button(p1, text="Seleccionar", command=per.NuevoUsuario).grid(row=15, column=2)

""" Campos pertenecientes a la pestaña inferencias """
ttk.Label(p2, text="\nPromedio de edad de los usuarios").pack()
ttk.Entry(p2, justify=CENTER, state=DISABLED, textvariable=resultadopromedio).pack()

ttk.Label(p2, text="\nGenero que asigno más veces una valoracion mayor a 60 en el atributo de Facilidad").pack()
ttk.Entry(p2, justify=CENTER, state=DISABLED, textvariable=resultadofacilidad).pack()

ttk.Label(p2, text="\nGenero que asigno más veces una valoracion mayor a 60 en el atributo de Disfrute").pack()
ttk.Entry(p2, justify=CENTER, state=DISABLED, textvariable=resultadodisfrute).pack()

ttk.Label(p2, text="\nUsuario el cual posee más edad").pack()
ttk.Entry(p2, justify=CENTER, state=DISABLED, textvariable=MayorEdad).pack()

raiz.style = ttkthemes.ThemedStyle()
raiz.style.theme_use('breeze')
raiz.mainloop()

