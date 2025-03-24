import matplotlib.pyplot as plt
import numpy as np
import math

LAMBDA = 10
M1 = 5
M2 = 5
SCALE = 100
TICK = 1
MODELLING_TIME = 450
INTERVAL = 20
SEED = 11


class SMO:
    def __init__(self):
        self.current_time = 0
        self.is_active_serve1 = False
        self.is_active_serve2 = False
        self.is_active_queue = False

        self.request_goal = 0
        self.serve1_goal = -1
        self.serve2_goal = -1
        self.queue_goal = -1

        self.prev_request_goal = 0
        self.prev_serve1_goal = 0
        self.prev_serve2_goal = 0
        self.prev_queue_goal = 0

        # stats
        self.served = 0
        self.refused = 0
        self.machine_cnt = 0

        self.time_zanyatosti_pervogo_ili_vtorogo_kanalov = 0
        self.time_zanyatosti_dvuh_kanalov = 0

        self.time_prostoya_pervogo_kanala = 0
        self.time_prostoya_vtorogo_kanala = 0
        self.time_prostoya_sistemi = 0

        self.time_v_queue = 0

        self.time_obslujivaniya = 0

        self.interval = INTERVAL
        self.zayavki_kanal_1 = []
        self.zayavki_kanal_2 = []
        self.zayavki_queue = []

        self.flag_novaya_zayavka_kanal_1 = True
        self.flag_novaya_zayavka_kanal_2 = True
        self.flag_novaya_zayavka_queue = True

        self.kolichestvo_podintervalov = 0

        #visuals
        self.request_data = []
        self.serve1_data = []
        self.serve2_data = []
        self.queue_data = []
        self.served_data = []
        self.refused_data = []
        ...
    
    @staticmethod
    def get_tau(constant, scale):
        rval = np.random.rand()
        req_tau = (-1 / constant) * math.log(rval) * scale
        return req_tau

    @staticmethod
    def get_tau_with_restrictions(prev_tau, constant, scale, trim=False):
        req_tau = 0
        while (req_tau < 1 or abs(prev_tau - req_tau) < 1):
            req_tau = SMO.get_tau(constant, scale)

        if (trim):
            return int(req_tau)
        return req_tau

    def get_status(self):
        tick_log = ""
        tick_log += f"<TICK NR          {self.current_time}>    \n"
        tick_log += f"Request goal:     {self.request_goal}     \n"
        tick_log += f"Serve1 goal:      {self.serve1_goal}      \n"
        tick_log += f"Serve2 goal:      {self.serve2_goal}      \n"
        tick_log += f"Queue goal:       {self.queue_goal}       \n\n"

        tick_log += f"Served:           {self.served}           \n"
        tick_log += f"Refused:          {self.refused}          \n"
        tick_log += f"Machine_cnt:      {self.machine_cnt}      \n"

        tick_log += f"</TICK NR         {self.current_time}>    \n\n\n"
        return tick_log

    

    def update_ticks(self):         # popravit' 0 v vizovah functsiy        # dobavit vremena na diagrammu   # dobavit statistiku
        if (self.serve1_goal == self.current_time):
            # obrabotka dannikh
            self.served += 1
            self.is_active_serve1 = False

            self.serve1_data.append( (self.current_time, TICK) )

            self.served_data.append( (self.current_time, TICK) )
            ...

        if (self.serve2_goal == self.current_time):
            # obrabotka dannikh
            self.served += 1
            self.is_active_serve2 = False

            self.serve2_data.append( (self.current_time, TICK) )

            self.served_data.append( (self.current_time, TICK) )
            ...
        
        if (self.queue_goal == self.current_time):              # vihod iz ocheredi

            if (not self.is_active_serve1):
                self.prev_serve1_goal = self.serve1_goal
                self.serve1_goal = self.current_time + self.get_tau_with_restrictions(0, M1, SCALE, True)
                self.is_active_serve1 = True
                ...
    
            elif (not self.is_active_serve2):
                self.prev_serve2_goal = self.serve2_goal
                self.serve2_goal = self.current_time + self.get_tau_with_restrictions(0, M2, SCALE, True)
                self.is_active_serve2 = True
                ...

            else:
                raise Exception("Problema v logike")
            self.is_active_queue = False
            
            ...

        if (self.request_goal == self.current_time):            # new machine
            self.machine_cnt += 1
            
            self.prev_request_goal = self.request_goal
            self.request_goal = self.current_time + self.get_tau_with_restrictions(0, LAMBDA, SCALE, True)

            self.request_data.append( (self.current_time, TICK) )

            if (not self.is_active_serve1):              # here go in serve 1
                self.prev_serve1_goal = self.serve1_goal
                self.serve1_goal = self.current_time + self.get_tau_with_restrictions(0, M1, SCALE, True)
                self.is_active_serve1 = True

                #self.serve1_data.append( (self.current_time, self.serve1_goal - self.current_time) )
                self.serve1_data.append( (self.current_time, TICK) )
                ...
            
            elif (not self.is_active_serve2):            # here go in serve 2
                self.prev_serve2_goal = self.serve2_goal
                self.serve2_goal = self.current_time + self.get_tau_with_restrictions(0, M2, SCALE, True)
                self.is_active_serve2 = True
                
                #self.serve2_data.append( (self.current_time, self.serve2_goal - self.current_time) )
                self.serve2_data.append( (self.current_time, TICK) )
                ...

            elif (not self.is_active_queue):             # here the place in queue
                self.prev_queue_goal = self.queue_goal
                self.queue_goal = min(self.serve1_goal, self.serve2_goal)
                self.is_active_queue = True

                #self.queue_data.append( (self.current_time, self.queue_goal - self.current_time) )
                self.queue_data.append( (self.current_time, TICK) )

            else:
                self.refused += 1

                self.refused_data.append( (self.current_time, TICK) )
                ...

    def collect_tick_stats(self):
        if ((self.is_active_serve1 or self.is_active_serve2) and not (self.is_active_serve1 and self.is_active_serve2)):
            self.time_zanyatosti_pervogo_ili_vtorogo_kanalov += 1
            
        if (self.is_active_serve1 and self.is_active_serve2):
            self.time_zanyatosti_dvuh_kanalov += 1

        if (not self.is_active_serve1):
            self.time_prostoya_pervogo_kanala += 1
        
        if (not self.is_active_serve2):
            self.time_prostoya_vtorogo_kanala += 1
        
        if (not self.is_active_serve1 and not self.is_active_serve2):
            self.time_prostoya_sistemi += 1

        if (self.is_active_queue):
            self.time_v_queue += 1

        if (self.is_active_serve1):
            self.time_obslujivaniya += 1
        
        if (self.is_active_serve2):
            self.time_obslujivaniya += 1
        
        if (self.is_active_serve1 and self.is_active_serve2):
            self.time_obslujivaniya -= 1


        if (self.current_time % self.interval == 0):
            self.zayavki_kanal_1.append(0)
            self.zayavki_kanal_2.append(0)
            self.zayavki_queue.append(0)

            if (self.current_time != 0):
                self.kolichestvo_podintervalov += 1

            self.flag_novaya_zayavka_kanal_1 = True
            self.flag_novaya_zayavka_kanal_2 = True
            self.flag_novaya_zayavka_queue = True


        if (not self.is_active_serve1):
            self.flag_novaya_zayavka_kanal_1 = True
        
        if (not self.is_active_serve2):
            self.flag_novaya_zayavka_kanal_2 = True

        if (not self.is_active_queue):
            self.flag_novaya_zayavka_queue = True

        if (self.is_active_serve1 and self.flag_novaya_zayavka_kanal_1):
            self.zayavki_kanal_1[-1] += 1
            self.flag_novaya_zayavka_kanal_1 = False
        
        if (self.is_active_serve2 and self.flag_novaya_zayavka_kanal_2):
            self.zayavki_kanal_2[-1] += 1
            self.flag_novaya_zayavka_kanal_2 = False

        if (self.is_active_queue and self.flag_novaya_zayavka_queue):
            self.zayavki_queue[-1] += 1
            self.flag_novaya_zayavka_queue = False
                

    def loop(self, modelling_time, trace=False):
        file = None
        if (trace):
            file = open("log", "w+")

        while (self.current_time < modelling_time):
            self.update_ticks()

            self.collect_tick_stats()        

            if (trace):
                file.write(self.get_status())
            
            self.current_time += 1

        print(f"Modelling time: {MODELLING_TIME}")
        print(f"Machine count: {self.machine_cnt}")
        print(f"Served: {self.served}")
        print(f"Refused: {self.refused}")

        print("\nSTATS:")
        print(f"1.Propusknaya: Served/Time:                     {self.served / MODELLING_TIME * SCALE}")
        print(f"2.Ver.Obsl: Served/Request:                     {self.served / self.machine_cnt}")
        print(f"3.Ver.Otkaza: Refused/Request:                  {self.refused / self.machine_cnt}")
        print(f"4.1.Ver.Zanyatosti pervogo ili vtorogo:         {self.time_zanyatosti_pervogo_ili_vtorogo_kanalov / MODELLING_TIME}")
        print(f"4.2.Ver.Zanyatosti pervogo i vtorogo:           {self.time_zanyatosti_dvuh_kanalov / MODELLING_TIME}")
        print(f"5.Srednee chislo zanyatikh:                     {self.time_zanyatosti_pervogo_ili_vtorogo_kanalov / MODELLING_TIME + \
                                                                 2 * self.time_zanyatosti_dvuh_kanalov / MODELLING_TIME} ")
        print(f"6.1.Vremya prostoya pervogo kanala:             {self.time_prostoya_pervogo_kanala / MODELLING_TIME}")
        print(f"6.2.Vremya prostoya vtorogo kanala:             {self.time_prostoya_vtorogo_kanala / MODELLING_TIME}")
        print(f"6.3.Vremya prostoya sistemi:                    {self.time_prostoya_sistemi / MODELLING_TIME}")

        print(f"7. Srednee chislo zayavok v ocheredI:           {self.time_v_queue / MODELLING_TIME}")
        print(f"8. Srednee vremya ojidaniya zayavok v ocheredi: {self.time_v_queue / self.machine_cnt}")
        print(f"9. Srednee vremya obslujivaniya zayavok:        {self.time_obslujivaniya / self.machine_cnt}")

        print(f"10. Srednee vremya zayavki v sisteme:           {(self.time_v_queue / self.machine_cnt) +\
                                                                 (self.time_obslujivaniya / self.machine_cnt)}")
        
        print(f"11. Srednee kolichestvo zayavok v sisteme:      {(sum(self.zayavki_kanal_1) +\
                                                                 sum(self.zayavki_kanal_2) +\
                                                                 sum(self.zayavki_queue)) \
                                                                / (self.kolichestvo_podintervalov - 1)}")
        
        if (trace):
            file.close()
        ...    


def draw():
    fig, [pool_request, pool_serve1, pool_serve2, pool_queue, pool_served, pool_refused] = plt.subplots(6, 1)

    inc = (0.2, 2)
    pool_request.broken_barh(smo.request_data, inc)
    
    pool_serve1.broken_barh(smo.serve1_data[::2], inc)
    pool_serve1.broken_barh(smo.serve1_data[1::2], inc, color="tab:orange")

    pool_serve2.broken_barh(smo.serve2_data, inc)
    pool_queue.broken_barh(smo.queue_data, inc)
    pool_served.broken_barh(smo.served_data, inc)
    pool_refused.broken_barh(smo.refused_data, inc)

    pool_request    .grid(linewidth = 1)
    pool_serve1     .grid(linewidth = 1)
    pool_serve2     .grid(linewidth = 1)
    pool_queue      .grid(linewidth = 1)
    pool_served     .grid(linewidth = 1)
    pool_refused    .grid(linewidth = 1)

    plt.xlim(0, 450)
    plt.ylim(0, 1)

    plt.show()


if __name__ == "__main__":
    np.random.seed(SEED)
    smo = SMO()
    smo.loop(MODELLING_TIME, True)
    draw()
