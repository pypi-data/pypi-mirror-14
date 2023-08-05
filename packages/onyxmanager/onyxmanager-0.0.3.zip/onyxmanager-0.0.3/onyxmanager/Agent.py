from pathlib import Path
import os, logging, socket, json, platform, uuid, re


class Trigger:
    def __init__(self, filePath, data, module):
        self.filePath = filePath
        self.data = data
        self.module = module
        self.name = self.getData()["name"]
        self.conditions = self.getData()["condition"]
        self.fact = self.getModule().getDevice().getFact(self.getConditions()["node"], self.getConditions()["fact"])

    def getFilePath(self):
        return self.filePath

    def getData(self):
        return self.data

    def getModule(self):
        return self.module

    def getFact(self):
        return self.fact

    def getName(self):
        return self.name

    def getConditions(self):
        return self.conditions

    def triggerConditional(self):
        try:
            conditions = self.getConditions()
            operator = conditions["operator"]
            value = conditions["value"]
            fact = self.getFact()

            if operator == "=":
                return fact == value
            elif operator == "!=":
                return fact != value
            elif operator == ">=":
                return fact >= value
            elif operator == "<=":
                return fact <= value
            elif operator == "!=":
                return fact != value
            else:
                raise ValueError(operator)
        except ValueError as e:
            raise
            exit(1)

    def getOutcome(self) -> bool:
        if self.triggerConditional():
            logging.info("Trigger '{0}' tripped in the '{1}' module because '{2}' was '{3}' to '{4}'".format(self.getName(),
                                                                                                      self.getModule().getName(),
                                                                                                      self.getFact(),
                                                                                                      self.getConditions()["operator"],
                                                                                                      self.getConditions()["value"]))
            return self.triggerConditional()


class Device:
    def __init__(self, name=""):
        self.OS = "OS"
        self.GENERAL = "general"
        self.SYSTEM = "system"
        self.NETWORK = "network"

        self.facts = {
            "OS": {},
            "general": {},
            "system": {},
            "network": {}
        }

        # Build Facts
        self.buildGeneralFacts(name).buildOSFacts().buildNetworkFacts()

    def buildGeneralFacts(self, name=""):
        self.facts[self.GENERAL]["name"] = socket.gethostname() if name == "" else name
        try:
            self.getFact(self.GENERAL, "uuid")
        except KeyError:
            self.facts[self.GENERAL]["uuid"] = str(uuid.uuid4())
        else:
            self.facts[self.GENERAL]["uuid"] = self.getFact(self.GENERAL, "uuid")
        return self

    def buildOSFacts(self):
        self.facts[self.OS]["platform"] = platform.platform(0, 1).replace('-', ' ').split(' ', 1)[0]
        self.facts[self.OS]["isWindows"] = self.getFact(self.OS, "platform") == "Windows"
        self.facts[self.OS]["bit"] = re.match(r'(?P<pre>(\S*))(?P<bit>([63][42])|(armv[0-9]))(?P<post>(\S*))', str(platform.machine())).group("bit")
        return self

    def buildNetworkFacts(self):
        if self.getFact(self.OS, "isWindows"):
            hostIPs = socket.gethostbyname_ex(socket.gethostname())[2]
            hostname = socket.gethostbyname_ex(socket.gethostname())[0]
            print("""
            Hostname: {0}
            IP(s): {1}
            """.format(hostname, hostIPs))
            primaryIP = socket.gethostbyname_ex(socket.gethostname())[2][0]

            self.facts[self.NETWORK]["hostIP"] = primaryIP
        return self

    def buildFacts(self):
        self.buildGeneralFacts(self.getFact(self.GENERAL, "name")).buildOSFacts().buildNetworkFacts()

    def getFact(self, node, key) -> str:
        return self.facts[node][key]

    def getFacts(self):
        for fact in self.facts.items():
            yield fact

    def dumpFactsToJSON(self, fileName):
        with open(fileName, 'w') as outfile:
            json.dump(self.facts, outfile, indent=4)


class Module:
    def __init__(self, name, filePath, device):
        self.triggers = {}
        self.name = name
        self.filePath = filePath
        self.device = device

        self.loadData()

    def getDevice(self) -> Device:
        return self.device

    def getTrigger(self, triggerName) -> Trigger:
        return self.triggers[triggerName]

    def getTriggers(self):
        for trigger in self.triggers.values():
            yield trigger

    def getName(self) -> str:
        return self.name

    def getFilePath(self) -> Path:
        return self.filePath

    def loadData(self):
        j_obj = json.load(open(str(self.getFilePath())))
        triggerData = j_obj["trigger"]
        self.triggers[triggerData["name"]] = Trigger(self.getFilePath(), triggerData, self)


class Agent:
    def __init__(self, deviceName="", workingDir="", logDir=""):
        self.modules = {}
        self.device = Device(deviceName)

        workingDir = workingDir if workingDir != "" else (r"C:\onyxmanager" if self.getDevice().getFact(self.getDevice().OS, "isWindows") else "/etc/OnyxManager")
        self.workingDir = Path(os.path.abspath(workingDir))

        logDir = logDir if logDir != "" else (r"C:\onyxmanager\logs" if self.getDevice().getFact(self.getDevice().OS, "isWindows") else "/var/log/OnyxManager")
        self.logDir = Path(os.path.abspath(logDir))

        if not self.getLogDir().exists():
            self.getLogDir().mkdir()
        logFile = "\\agent.log" if self.getDevice().getFact(self.getDevice().OS, "platform") == "Windows" else "/agent.log"
        logging.basicConfig(filename=(str(self.getLogDir()) + "\\agent.log"),level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

        logging.info("")
        logging.info("OnyxManager v{0} - Started".format("0.0.3"))
        logging.info("Log directory set to '{0}'".format(str(self.getLogDir())))
        logging.info("Working directory set to '{0}'".format(str(self.getWorkingDir())))

        self.loadModules()

    def getDevice(self) -> Device:
        return self.device

    def getWorkingDir(self) -> Path:
        return self.workingDir

    def getLogDir(self) -> Path:
        return self.logDir

    def loadModules(self):
        if not self.getWorkingDir().exists():
            self.getWorkingDir().mkdir()
        for file in self.getWorkingDir().iterdir():
            if file.is_file() and file.name[-5:] == ".json":
                try:
                    self.modules[file.name[:-5]] = Module(file.name[:-5], file, self.getDevice())
                    logging.info("Module '{0}' added - path='{1}'".format(file.name[:-5], file))
                except FileNotFoundError as FileE:
                    logging.error("Module '{0}' failed to load, missing file! - path='{1}'".format(file.name[:-5], file))
                    raise

    def getModule(self, moduleName) -> Module:
        return self.modules[moduleName]

    def getModules(self) -> dict:
        return self.modules.values()

    def dumpDeviceFactsToJSON(self):
        self.getDevice().dumpFactsToJSON(str(self.getWorkingDir()) + "/device.facts")
        logging.info("Device facts dumped to '{0}'".format(str(self.getWorkingDir()) + "/device.facts"))