from server import Server
from client import Client
from queue_system_utils import *
import statistics

class Queue:
    def __init__(self, lmax, s, arrival, lambd, service, mu):
        self.lmax = lmax
        self.s = s
        self.arrival = arrival # Degenerate or markovian
        # function
        self.lambd = lambd
        self.service = service # Degenerate or markovian
        # function
        self.mu = mu
        
        # For simulation
        self.clients_waiting = []
        #self.clients_on_servers = [None] * self.s
        self.clients_finished = []
        self.time = 0
        self.clients_served = 0
        self.clients_lost = 0

        self.servers = []

        #[Arrival, Exit]
        self.events = [0,None]

        self.init_servers()

    
    """
        Initialize servers of the system.
    """
    def init_servers(self):
        for i in range(self.s):
            self.servers.append(Server())

    def simulation(self, time_limit, initial_clients, maximum_arrivals):
        assert(initial_clients >= 0), "initial_clients should be > 0"

        self.clients_waiting = [Client(arrival_time=self.time)] * initial_clients
        self.lmax = maximum_arrivals


        while (self.time < time_limit):

            # Si llegan clientes al sistema
            if self.time == self.events[0]:
                #Calcular cuándo va a llegar el próximo cliente
                if (self.arrival == "degenerate"):
                    self.events[0] += degenerate(lambd(len(self.clients_waiting) + len([s for s in self.servers if s.current_client != None])))
                elif (self.arrival == "markovian"):
                    self.events[0] += markovian(lambd(len(self.clients_waiting) + len([s for s in self.servers if s.current_client != None])))
                    
                # Si la cola tiene campo, se agrega el cliente a la cola o servidor libre
                if (len(self.clients_waiting) < self.lmax):
                    self.clients_waiting.append(Client(arrival_time=self.time))
                    idle_servers = [s for s in self.servers if s.current_client == None]
                    # Si el servidor está libre
                    if (len(idle_servers) != 0):
                        idle_servers[0].current_client = self.clients_waiting.pop(0)
                        # Client's attention time
                        idle_servers[0].current_client.attention_time = self.time
                        # Server's idle time
                        idle_servers[0].calc_idle_time(self.time)
                        # Se calcula cuándo va a salir el nuevo cliente
                        if (self.service == "degenerate"):
                            idle_servers[0].current_client_service_finishing_time = self.time + degenerate(mu(len(self.clients_waiting) + len([s for s in self.servers if s.current_client != None])))
                        elif (self.service == "markovian"):
                            idle_servers[0].current_client_service_finishing_time = self.time + markovian(mu(len(self.clients_waiting) + len([s for s in self.servers if s.current_client != None])))

                        # agregamos service time.
                        idle_servers[0].serving_time += idle_servers[0].current_client_service_finishing_time

                        self.events[1] = min([s.current_client_service_finishing_time for s in self.servers if s.current_client_service_finishing_time != None])

                        self.clients_served += 1

                    #else:
                        #self.clients_waiting.append(Client())
                else:
                # Sino se pierde el cliente
                    self.clients_lost += 1

            # Si salen clientes de la cola
            if self.time == self.events[1]:
                for server in self.servers:
                    if (server.current_client_service_finishing_time == self.time):
                        # Si hay clientes en la cola, se saca uno y se agrega al servidor
                        if (len(self.clients_waiting) > 0):
                            # Se calcula cuándo va a salir el nuevo cliente
                            if (self.service == "degenerate"):
                                server.current_client_service_finishing_time = self.time + degenerate(mu(len(self.clients_waiting) + len([s for s in self.servers if s.current_client != None])))
                            elif (self.service == "markovian"):
                                server.current_client_service_finishing_time = self.time + markovian(mu(len(self.clients_waiting) + len([s for s in self.servers if s.current_client != None])))
                            
                            # Exit of current client
                            server.current_client.exit_time = self.time
                            self.clients_finished.append(server.current_client)

                            # agregamos cliente al servidor:
                            server.current_client = self.clients_waiting.pop(0)
                            server.current_client.attention_time = self.time
                            # agregamos service time.
                            server.serving_time += self.time - server.current_client_service_finishing_time

                            self.clients_served += 1

                        # Sino calculamos tiempo del servidor desocupado
                        else:
                            server.idle_start = self.time
                            server.current_client_service_finishing_time = None

                if len([s.current_client_service_finishing_time for s in self.servers if s.current_client_service_finishing_time != None]) > 0:
                    self.events[1] = min([s.current_client_service_finishing_time for s in self.servers if s.current_client_service_finishing_time != None])
                #else:
                    #print(self.time)
                    #self.events[1] = time_limit+1
            # Advance to next event.
            #print(self.events)
            self.time = min(self.events[0], self.events[1])
        
        # Get results
        #self.avg_serving_time = statistics.mean(self.servers, key=lambda x: x.serving_time).serving_time
        self.avg_idle_time = statistics.mean([s.serving_time for s in self.servers])

        # TODO: print results of simulation
        print("clients served:       ", self.clients_served)
        print('clients lost:         ', self.clients_lost)
        print('Avg client\'s waiting time:     ', self.get_average_waiting_time())
        print('Avg client\'s Serving time:     ', self.get_average_attention_time())
        print('Avg server Idle time: ', self.get_average_idle_time())

    def get_average_waiting_time(self):
        waiting_times = 0
        for client in self.clients_finished:
            waiting_times += client.calc_waiting_time()
        return waiting_times/len(self.clients_finished)
    
    def get_average_attention_time(self):
        attention_times = 0
        for client in self.clients_finished:
            attention_times += client.calc_attention_time()
        return attention_times/len(self.clients_finished)
    
    def get_average_idle_time(self):
        idle_times = 0
        for server in self.servers:
            idle_times += server.idle_time
        return idle_times/self.s