from onyxmanager import Agent

agent = Agent.Agent("OnyxPi-1")
for fact in agent.getDevice().getFacts():
    print(fact)

for module in agent.getModules():
    for trigger in module.getTriggers():
        print("{0}: {1}".format(trigger.getName(), trigger.getConditions()))
for module in agent.getModules():
    for trigger in module.getTriggers():
        trigger.getOutcome()

agent.dumpDeviceFactsToJSON()

# ipInfo = open()
# subprocess.call('ipconfig /all', stdout=ipInfo)
# print(ipInfo)