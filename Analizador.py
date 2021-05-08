import re
from Estadistica import Estadistica
from Error import error_e
from Usuario import usuario
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom




class analizador:
    listaEstadisticas = []
    XML_inicial = None
    XML_Final = None

    def analizar(self, archivo):
        r_fecha = r"(\d*\/\d*\/\d*)"
        r_correo = r"(([\w*]+@)+\w*[.]\w*[.]\w*[.]\w*)"
        r_error = r"(\d+)"

        root = ET.fromstring(archivo)

        afec = ' Afectados:edna@ing.usac.edu.gt, bart@ing.usac.edu.gt'
        linea = 'Guatemala, 20/04/2021'
        var = re.findall(r_correo, afec)

        print()
        # var = re.findall(self.r_fecha, linea)

        for evento in root:
            una_estadistica = Estadistica()
            estado = 0
            est_nueva = None
            f_estadistica = ""
            afectados = []
            un_usuario = usuario()
            un_error = error_e()

            textoReporte = evento.text
            for linea in textoReporte.split("\n"):
                if linea.lower().__contains__("reportado"):
                    estado = 1
                elif linea.lower().__contains__("usuarios"):
                    estado = 2
                elif linea.lower().__contains__("error"):
                    estado = 3

                if estado == 0:
                    if re.search(r_fecha, linea):
                        f_evento = re.search(r_fecha, linea)
                        f = f_evento.group(0)
                        f_estadistica = f


                elif estado == 1:
                    reportador = re.search(r_correo, linea)
                    rep = reportador.group(0)
                    un_usuario.correo = rep
                    


                elif estado == 2:
                    correos = re.findall(r_correo, linea)

                    for correo in correos:
                        afectados.append(correo[0])

                elif estado == 3:
                    error = re.search(r_error, linea)
                    if error != None:
                        codigo = error.group(0)
                        un_error.codigo = codigo


            existe_fecha = None
            if self.listaEstadisticas != []:
                for estadistica in self.listaEstadisticas:
                    if estadistica.fecha == f_estadistica:
                        estadistica.mensajesFecha += 1
                        ex_usuario = self.existe(estadistica.usuarios,un_usuario.correo, "usuario")
                        if ex_usuario == False:
                            estadistica.usuarios.append(un_usuario)

                        for afectado in afectados:
                            estadistica.afectados.append(afectado)


                        ex_error = self.existe(estadistica.errores,un_error.codigo, "error")
                        if ex_error == False:
                            estadistica.errores.append(un_error)


                        existe_fecha = True
                    else:
                        continue

            if existe_fecha != True:
                una_estadistica.fecha = f_estadistica
                una_estadistica.mensajesFecha =1
                una_estadistica.usuarios.append(un_usuario)
                una_estadistica.afectados = afectados

                una_estadistica.errores.append(un_error)
                self.listaEstadisticas.append(una_estadistica)
        for final_estadistica in self.listaEstadisticas:
            final_estadistica.afectados = list(set(final_estadistica.afectados))
        self.crearXML()

    def crearXML(self):
        estadisticas_xml = Element("ESTADISTICAS")
        for estadistica_out in self.listaEstadisticas:
            estadistica_xml  = SubElement(estadisticas_xml, "ESTADISTICA")

            fecha_xml = SubElement(estadistica_xml, "FECHA")
            fecha_xml.text = estadistica_out.fecha

            mensajes_fecha_xml = SubElement(estadistica_xml, "CANTIDAD_MENSAJES")
            mensajes_fecha_xml.text = str(estadistica_out.mensajesFecha)

            reportados_xml = SubElement(estadistica_xml, "REPORTADO_POR")
            for usuario_out in estadistica_out.usuarios:
                usuario_xml = SubElement(reportados_xml, "USUARIO")

                correo_us_xml = SubElement(usuario_xml, "EMAIL")
                correo_us_xml.text = usuario_out.correo

                mensajes_us = SubElement(usuario_xml, "CANTIDAD_MENSAJES")
                mensajes_us.text = str(usuario_out.cantidad)
            afectados_xml = SubElement(estadistica_xml, "AFECTADOS")
            for afectado_out in estadistica_out.afectados:
                afectado_xml = SubElement(afectados_xml, "AFECTADO")
                afectado_xml.text = afectado_out

            errores_xml = SubElement(estadistica_xml, "ERRORES")
            for error_out in estadistica_out.errores:
                error_xml = SubElement(errores_xml, "ERROR")

                codigo_xml = SubElement(error_xml, "CODIGO")
                codigo_xml.text = error_out.codigo

                mensajes_er = SubElement(error_xml, "CANTIDAD_MENSAJES")
                mensajes_er.text = str(error_out.cantidad)


        xml_crudo = tostring(estadisticas_xml)

        reparsed = minidom.parseString(xml_crudo)
        xml_final = reparsed.toprettyxml()
        print(xml_final)

    def existe(self, elementos, posibleRep, tipo):
        atributo = ""
        for elemento in elementos:
            if tipo == "usuario":
                atributo = elemento.correo
            elif tipo == "error":
                atributo = elemento.codigo

            if atributo == posibleRep:
                elemento.cantidad += 1
                return True

            else:
                continue
        return False

'''r_fecha = "r(\d*\/\d*)"
        reportador = "r()"
        afectados = "r(([\w*]+@)+\w*[.]\w*[.]\w*[.]\w*)"
        errores = r"()"
'''

'''Guatemala, 20/04/2021
		Reportado por: homero@ing.usac.edu.gt
		Usuarios afectados: bart@ing.usac.edu.gt, lisa@ing.usac.edu.gt
		Error: 20002 - Error de destino, momento equivocado,
		lugar equivocado y medios equivocados     '''
