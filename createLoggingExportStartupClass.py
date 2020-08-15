from javax.management import RuntimeMBeanException
import javax.management.MBeanException
from java.lang import UnsupportedOperationException

#Function to Connect to the Server
def onlineConnect():
  loadProperties("./WLLoggingExporter.properties")
  try:
      URL="t3://"+adminServerListenAddress+":"+adminServerListenPort
      connect(userName, passWord, URL)
  except WLSTException:
      print 'No server is running at '+URL


def buildLoggingExportStartupClass():
  cd('/')
  clusters= cmo.getClusters()
  targetArray=[ObjectName('com.bea:Name=AdminServer,Type=Server')]

  for cluster in clusters:
    targetArray.append(ObjectName('com.bea:Name='+cluster.getName()+',Type=Cluster'))
  print targetArray
  startTransaction()
  cd('/')
  startup_class = getMBean('/StartupClasses/LoggingExporterStartupClass')
  if startup_class == None:
    cmo.createStartupClass('LoggingExporterStartupClass')
  cd('/StartupClasses/LoggingExporterStartupClass')
  cmo.setClassName('weblogic.logging.exporter.Startup')
  set('Targets',jarray.array(targetArray, ObjectName))
  #set('Targets',jarray.array([ObjectName('com.bea:Name=AdminServer,Type=Server'), ObjectName('com.bea:Name=apc_cluster1,Type=Cluster'), ObjectName('com.bea:Name=DynamicCluster,Type=Cluster')], ObjectName))
  cmo.setDeploymentOrder(1000)
  save()
  endTransaction()
#Define Start Transaction
def startTransaction():
  edit()
  startEdit()

#Define End Transaction
def endTransaction():
 activate()

#Start all the Functions Below
onlineConnect()
