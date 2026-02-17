import sys
import requests
from PyQt5.QtCore import QTimer, Qt, QTime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QLineEdit


class AppClima(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ClimaApp')

        self.line_clima = QLineEdit(self)

        self.label_ingresa = QLabel("Ingresa el nombre de una ciudad",self)
        self.label_emoji = QLabel(self)
        self.temperatura = QLabel(self)
        self.label_descripcion = QLabel(self)

        self.button_clima = QPushButton("Obtener clima",self)
        self.initUi()

    def initUi(self):
        vbox = QVBoxLayout()

        self.label_ingresa.setAlignment(Qt.AlignHCenter)
        self.label_emoji.setAlignment(Qt.AlignHCenter)
        self.temperatura.setAlignment(Qt.AlignHCenter)
        self.label_descripcion.setAlignment(Qt.AlignHCenter)
        self.line_clima.setAlignment(Qt.AlignHCenter)



        vbox.addWidget(self.label_ingresa)
        vbox.addWidget(self.line_clima)
        vbox.addWidget(self.button_clima)
        vbox.addWidget(self.temperatura)
        vbox.addWidget(self.label_emoji)
        vbox.addWidget(self.label_descripcion)

        self.setLayout(vbox)

        self.line_clima.setObjectName("line_clima")
        self.label_emoji.setObjectName("label_emoji")
        self.label_descripcion.setObjectName("label_descripcion")
        self.button_clima.setObjectName("button_clima")
        self.temperatura.setObjectName("temperatura")
        self.label_ingresa.setObjectName("label_ingresa")

        self.setStyleSheet("""
        
            QLabel, QPushButton{
                
                font-family: calibri;
            
            }
            QLabel#label_ingresa{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#line_clima{
                font-size: 40px;
            }
            QPushButton#button_clima{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperatura{
                font-size: 75px;
            }
            QLabel#label_emoji{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#label_descripcion{
                font-size: 50px;
            }
        
        """)

        self.button_clima.clicked.connect(self.obtenerClima)


    def obtenerClima(self):
        api_key = "5820cb966a0898dd6d4ea48733ff4921"
        ciudad = self.line_clima.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            datos = response.json()

            if datos["cod"] == 200:
                self.darClima(datos)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.darError("Bad Request")
                case 401:
                    self.darError("No autorizado\nAPI Key invalido")
                case 403:
                    self.darError("Denegado\nAcceso denegado")
                case 404:
                    self.darError("No encontrado\nCiudad no encontrada")
                case 500:
                    self.darError("Porblema interno del servidor\nIntenta mas tarde")
                case 502:
                    self.darError("Invalid response")
                case 503:
                    self.darError("Servidor caido")
                case 504:
                    self.darError("Timeout")
                case _:
                    self.darError(f"Error: {http_error}")
        except requests.exceptions.ConnectionError:
            self.darError("Error de conexion")
        except requests.exceptions.Timeout:
            self.darError("Tiempo agotado")
        except requests.exceptions.TooManyRedirects:
            self.darError("Muchas redirecciones")
        except requests.exceptions.RequestException as req_error:
            self.darError(f"Request error: {req_error}")


    def darError(self, mensaje):
        self.temperatura.setStyleSheet("font-size: 30px;")
        self.temperatura.setText(mensaje)
        self.label_emoji.clear()
        self.label_descripcion.clear()

    def darClima(self, datos):
        self.temperatura.setStyleSheet("font-size: 75px;")
        temperatura_k = datos["main"]["temp"]
        temperatura_c = temperatura_k - 273.15

        climaId = datos["weather"][0]["id"]
        des_clima = datos["weather"][0]["description"]

        self.temperatura.setText(f"{temperatura_c:.0f}°C")
        self.label_descripcion.setText(des_clima)
        self.label_emoji.setText(self.getEmoji(climaId))

    @staticmethod
    def getEmoji(climaId):
        if 200 <= climaId <= 232:
            return "⛈️"
        elif 300 <= climaId <= 321:
            return "☁️"
        elif 500 <= climaId <= 531:
            return "🌧️"
        elif 600 <= climaId <= 622:
            return "❄️"
        elif 701 <= climaId <= 741:
            return "🌫️"
        elif climaId == 762:
            return "🌋"
        elif climaId == 771:
            return "💨"
        elif climaId == 781:
            return "🌪️"
        elif climaId == 800:
            return "☀️"
        elif 801 <= climaId <= 804:
            return "☁️"
        else:
            return ""


def main():
    app = QApplication(sys.argv) #El sys.argv es Para manejarlo desde la terminal (nose usa aqui)
    climaApp = AppClima()
    climaApp.show()
    sys.exit(app.exec_()) #Espera a que el usuario haga algo, como cerrar la ventana por ejemplo

if __name__ == '__main__':
    main()


