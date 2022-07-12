from rtve import RTVE
from protocolo import Protocolo
import json
from datetime import datetime
from time import strptime
from dateutil.relativedelta import relativedelta
from time import mktime
from caworker import Worker
from time import sleep


if __name__ == '__main__':

    worker = Worker()
    print('Worker started')

    while True:
        tasks = worker.fetch_tasks(max_tasks=10)

        for task in tasks:

            rtve = RTVE()
            requisicoes = rtve.get_requisicoes()

            tickets = {}

            for requisicao in requisicoes:
                data = datetime.fromtimestamp(mktime(strptime(requisicao['data'].split('.')[0], '%Y-%m-%dT%H:%M:%S')))
                if len(requisicao['observacao'].strip()) == 11 and data >= datetime.now() - relativedelta(months=3):
                    ticketid = requisicao['observacao'].strip()
                    if ticketid not in tickets:
                        tickets[ticketid] = str(requisicao['numeroRequisicao'].replace('WEB:', ''))
                    else:
                        tickets[ticketid] = tickets[ticketid] + ', ' + str(requisicao['numeroRequisicao'].replace('WEB:', '')) # numeroRequisicao
                
            protocolo = Protocolo()

            for ticket in tickets:
                protocolo_tickets = protocolo.get_ticket(ticket)
                for protocolo_ticket in protocolo_tickets:
                    params = dict(json.loads(protocolo_ticket.params))
                    params['ufield_34'] = tickets[ticket]
                    protocolo.update_ticket(ticket, "params = '" + json.dumps(params) + "'")
                    print(ticket, params)
            
            del rtve
            del protocolo

            print('Complete update')

            worker.complete_task(task_id=task.id_)
        
        if len(tasks) == 0:
            sleep(30)