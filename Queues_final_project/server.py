from client import Client

#  Cada vez que un servidor termina de atender un cliente,
#  inmediatamente recibe alc
# siguiente de la cola. Si no hay clientes por atender entonces
#  contará el tiempo que pasó desocupado con el fin de generar
#  las estadísticas finales.
class Server:
    def __init__(self):
        self.current_client = None
        self.serving_time = 0
        self.idle_time = 0
        self.idle_start = 0
        self.current_client_service_finishing_time = None
        #self.total_idle_time = 0

    def calc_idle_time(self, time):
        self.idle_time += time - self.idle_start
