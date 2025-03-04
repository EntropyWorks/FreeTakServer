#######################################################
# 
# ClientReceptionHandler.py
# Python implementation of the Class ClientReceptionHandler
# Generated by Enterprise Architect
# Created on:      19-May-2020 7:17:21 PM
# Original author: Natha Paquette
# 
#######################################################
import time
import socket
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from defusedxml import ElementTree as etree

logger = CreateLoggerController("ClientReceptionHandler").getLogger()
from FreeTAKServer.controllers.configuration.ClientReceptionLoggingConstants import ClientReceptionLoggingConstants

loggingConstants = ClientReceptionLoggingConstants()



class ClientReceptionHandler:
    def __init__(self):
        self.dataPipe = []
        self.socketCount = 0

    def startup(self, clientInformationArray):
        try:
            self.clientInformationArray = clientInformationArray
            '''logger.propagate = False
            logger.info(loggingConstants.CLIENTRECEPTIONHANDLERSTART)
            logger.propagate = True'''
            output = self.monitorForData(self.dataPipe)
            if output == 1:
                return self.dataPipe
            else:
                return -1
            '''
            time.sleep(600)
            # temporarily remove due to being unnecessary and excessively flooding logs
            logger.info('the number of threads is ' + str(threading.active_count()) + ' monitor event process alive is ' + str(monitorEventProcess.is_alive()) +
                        ' return data to Orchestrator process alive is ' + str(monitorForData.is_alive()))
            '''
        except Exception as e:
            logger.error(loggingConstants.CLIENTRECEPTIONHANDLERSTARTUPERROR + str(e))

    def monitorForData(self, queue):
        '''
        updated receive all
        '''
        try:
            for client in self.clientInformationArray:
                sock = client.socket
                try:
                    try:
                        BUFF_SIZE = 8087
                        data = b''
                    except Exception as e:
                        print('\n\n disconnect A \n\n')
                        logger.error(loggingConstants.CLIENTRECEPTIONHANDLERMONITORFORDATAERRORA + str(e))
                        self.returnReceivedData(client, b'', queue)
                        self.clientInformationArray.remove(client)
                    try:
                        sock.settimeout(0.001)
                        part = sock.recv(BUFF_SIZE)
                    except socket.timeout as e:
                        continue
                    except BrokenPipeError as e:
                        print('\n\n disconnect B \n\n')
                        self.clientInformationArray.remove(client)
                        self.returnReceivedData(client, b'', queue)
                        continue
                    except Exception as e:
                        print('\n\n disconnect C ' + str(e) + "\n\n")
                        logger.error("Exception other than broken pipe in monitor for data function "+str(e))
                        self.returnReceivedData(client, b'', queue)
                        self.clientInformationArray.remove(client)
                        continue
                    try:
                        if part == b'' or part == None:
                            print('\n\n disconnect D \n\n')
                            self.returnReceivedData(client, b'', queue)
                            self.clientInformationArray.remove(client)
                            continue
                        else:
                            try:
                                timeout = time.time() + 1
                                while time.time() < timeout:
                                    try:
                                        event = etree.fromstring(part)
                                        if event.tag == "event":
                                            self.returnReceivedData(client, part, queue)
                                            break
                                        else:
                                            break
                                    except:
                                        try:
                                            sock.settimeout(0.1)
                                            part += sock.recv(BUFF_SIZE)
                                        except socket.timeout as e:
                                            logger.error('there has been an exception in client reception handler ' + str(e))
                                            break
                                        except BrokenPipeError as e:
                                            self.clientInformationArray.remove(client)
                                            break
                                        except Exception as e:
                                            print('\n\n disconnect E \n\n')
                                            logger.error("Exception other than broken pipe in monitor for data function")
                                            self.returnReceivedData(client, b'', queue)
                                            break
                            except Exception as e:
                                logger.error('error in buffer ' + str(e))
                                return -1

                    except Exception as e:
                        print('\n\n disconnect F \n\n')
                        logger.error(loggingConstants.CLIENTRECEPTIONHANDLERMONITORFORDATAERRORC + str(e))
                        self.returnReceivedData(client, b'', queue)
                        self.clientInformationArray.remove(client)
                        return -1

                except Exception as e:
                    print('\n\n disconnect G \n\n')
                    logger.error(loggingConstants.CLIENTRECEPTIONHANDLERMONITORFORDATAERRORD + str(e))
                    self.returnReceivedData(client, b'', queue)
                    return -1
            return 1
        except Exception as e:
            logger.error('exception in monitor for data '+str(e))
            return -1

    def returnReceivedData(self, clientInformation, data, queue):
        try:
            from FreeTAKServer.model.RawCoT import RawCoT
            # print(data)
            RawCoT = RawCoT()
            RawCoT.clientInformation = clientInformation
            RawCoT.xmlString = data
            self.dataPipe.append(RawCoT)
            return 1
        except Exception as e:
            logger.error(loggingConstants.CLIENTRECEPTIONHANDLERRETURNRECEIVEDDATAERROR + str(e))
            return -1