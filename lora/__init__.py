import getpass
import logging
import requests

logger = logging.getLogger(__file__)

__url_cache__ = {}

try:
    input = raw_input  # Python 2
except NameError:
    pass

class LoraSession(requests.Session):
    domain = 'https://lc.llnl.gov'
    login_prompt = 'Pin & Token: '
    username_prompt = 'LC Username'

    def __init__(self):
        super(LoraSession, self).__init__()

        self.headers.update({
            # Only accept UTF-8 encoded data
            'Accept-Charset': 'utf-8',
            # Always sending JSON
            'Content-Type': "application/json",
        })

        self.login_url = '%s/dologin.cgi' % self.domain
        self.base_url = '%s/lorenz/lora/lora.cgi' % self.domain

    def build_url(self, *args, **kwargs):
        """
        Builds a new API url from scratch.

        Adapted from: https://github.com/sigmavirus24/github3.py/blob/develop/github3/session.py
        """
        parts = [kwargs.get('base_url') or self.base_url]
        parts.extend(args)
        parts = [str(p) for p in parts]
        key = tuple(parts)
        logger.debug('Building a url from %s', key)
        if key not in __url_cache__:
            logger.debug('Missed the cache building the url')
            __url_cache__[key] = '/'.join(parts)

        url = __url_cache__[key]
        logger.info('Built URL: %s', url)

        return url

    def login(self, username=None, password=None):
        """
        Login to Lorenz with credentials

        Raises a ConnectionError if the authentication failed for any reason
        """
        if username is None:
            env_username = getpass.getuser()
            user_prompt = "%s [%s]: " % (self.username_prompt, env_username)
            username = input(user_prompt)

            if username == '':
                username = env_username

        logger.debug('Username: %s', username)

        if password is None:
            password = getpass.getpass(self.login_prompt)

        response = self.post(self.login_url, auth=(username, password))
        logger.debug('Server response: %s', response.__dict__)

        valid_token_keys = ('crowd.token_key', 'izcrowd.token_key')
        if not any(token in response.cookies for token in valid_token_keys):
            raise requests.ConnectionError('Failed to authenticate')

        return response

    def getUserGroups(self, username='ME'):
        """
        Get list of all groups for a user

        Lora: /user/:user/groups
        """
        response = self.get(self.build_url('user', username, 'groups'))
        return response.json()

    def getAllGroups(self):
        """
        Get list of all groups

        Lora: /groups
        """
        response = self.get(self.build_url('groups'))
        return response.json()

    def getUserBanks(self, username='ME'):
        """
        Get list of all banks for a user

        Lora: /user/:user/banks
        """
        response = self.get(self.build_url('user', username, 'banks'))
        return response.json()

    def getAllBanks(self):
        """
        Get list of all banks

        Lora: /banks
        """
        response = self.get(self.build_url('banks'))
        return response.json()

    def getUserBanksByHost(self, username='ME'):
        """
        Get dict of all banks for a user by host

        Lora: /user/:user/bankhosts
        """
        response = self.get(self.build_url('user', username, 'bankhosts'))
        return response.json()

    def getUserAccounts(self, username='ME'):
        """
        Get list of all accounts for a user

        Lora: /user/:user/hosts
        """
        response = self.get(self.build_url('user', username, 'hosts'))
        return response.json()

    def getUserClusters(self, username='ME'):
        """
        Get list of all compute-only clusters for a user

        Lora: /user/:user/clusters?compute_only=1
        """
        payload = {'compute_only': '1'}
        response = self.get(self.build_url('user', username, 'clusters'), params=payload)
        return response.json()

    def getAllJobDetails(self):
        """
        Get list of all jobs with job details included

        Lora: /queue
        """
        response = self.get(self.build_url('queue'))
        return response.json()

    def getAllJobCountsByUser(self):
        """
        Get dict of all jobs counts by user and all job counts by user for each host

        Lora: /queue?filter=allJobs
        """
        payload = {'filter': 'allJobs'}
        response = self.get(self.build_url('queue'), params=payload)
        return response.json()

    def getAllJobDetailsForHost(self, host):
        """
        Get list of all jobs for a host

        Lora: /queue/:host
        """
        response = self.get(self.build_url('queue', host))
        return response.json()

    def getUserDefaultHost(self, username='ME'):
        """
        Get default host for a user

        Lora: /user/:user/default/host
        """
        response = self.get(self.build_url('user', username, 'default', 'host'))
        return response.json()

    def getGroupInfo(self, group):
        """
        Get information for a group

        Lora: /group/:group
        """
        response = self.get(self.build_url('group', group))
        return response.json()

    def getBankInfo(self, bank, username='ME'):
        """
        Get information for a bank

        Lora: /user/:user/bank/:bank
        """
        response = self.get(self.build_url('user', username, 'bank', bank))
        return response.json()

    def getAllClusters(self):
        """
        Get list of cluster

        Lora: /clusters
        """
        response = self.get(self.build_url('clusters'))
        return response.json()

    def getAllClustersMounts(self):
        """
        Get dict of cluster mounts by host

        Lora: /clusters/mounts
        """
        response = self.get(self.build_url('clusters', 'mounts'))
        return response.json()

    def getHostInfo(self, host):
        """
        Get information for a host

        Lora: /host/:host
        """
        response = self.get(self.build_url('host', host))
        return response.json()

    def getHostJobLimits(self, host):
        """
        Get job limits for a host

        Lora: /cluster/:host/joblimits
        """
        response = self.get(self.build_url('cluster', host, 'joblimits'))
        return response.json()

    def getHostDetails(self, host):
        """
        Get details for a host

        Lora: /cluster/:host/details
        """
        response = self.get(self.build_url('cluster', host, 'details'))
        return response.json()

    def getHostTopology(self, host):
        """
        Get topology for a host

        Lora: /cluster/:host/topo
        """
        response = self.get(self.build_url('cluster', host, 'topo'))
        return response.json()

    def getAllMachineLoads(self):
        """
        Get machine statuses

        Lora: /status/clusters
        """
        response = self.get(self.build_url('status', 'clusters'))
        return response.json()

    def getAllClusterUtilizations(self):
        """
        Get cluster utilizations

        Lora: /status/clusters/utilization/hourly2
        """
        response = self.get(self.build_url('status', 'clusters', 'utilization', 'hourly2'))
        return response.json()

    def getAllLcOrganizations(self):
        """
        Get dict of LC organizations

        Lora: /lc/organizations
        """
        response = self.get(self.build_url('lc', 'organizations'))
        return response.json()

    def getAllCoreCoordinators(self):
        """
        Get dict of all core coordinators

        Lora: /corecoordinators
        """
        response = self.get(self.build_url('corecoordinators'))
        return response.json()

    def getAllNews(self):
        """
        Get list of all news items

        Lora: /news
        """
        response = self.get(self.build_url('news'))
        return response.json()

    def getUserNews(self, username='ME'):
        """
        Get list of all news items for a user

        Lora: /user/:user/news
        """
        response = self.get(self.build_url('user', username, 'news'))
        return response.json()

    def getNewsItem(self, item):
        """
        Get information for a news item

        Lora: /news/:item
        """
        response = self.get(self.build_url('news', item))
        return response.json()

    def getUserDiskQuotaInfo(self, username='ME'):
        """
        Get disk quota info for given user

        Lora: /user/:user/quotas
        """
        response = self.get(self.build_url('user', username, 'quotas'))
        return response.json()

    def getUserCpuUsage(self, username='ME'):
        """
        Get cpu usage info for given user

        Lora: /user/:user/cpuutil/daily
        """
        response = self.get(self.build_url('user', username, 'cpuutil', 'daily'))
        return response.json()

    def getUserJobs(self, username='ME'):
        """
        Get job info for given user

        Lora: /user/:user/queue
        """
        response = self.get(self.build_url('user', username, 'queue'))
        return response.json()

    def getUserJobsForHost(self, host, username='ME'):
        """
        Get job info for given user on given host

        Lora: /user/:user/queue?host=host
        """
        payload = {'filter': 'allJobs'}
        response = self.get(self.build_url('user', username, 'queue'),
                            params=payload)
        return response.json()

    def getBankHistory(self, bank):
        """
        Get history of a bank's usage

        Lora: /bank/:bank/cpuutil/daily
        """
        response = self.get(self.build_url('bank', bank, 'cpuutil', 'daily'))
        return response.json()

    def getBankHistoryForHost(self, bank, host):
        """
        Get history of a bank's usage on a host

        Lora: /cluster/:host/bank/:bank/cpuutil/daily
        """
        response = self.get(self.build_url('cluster', host, 'bank', bank, 'cpuutil', 'daily'))
        return response.json()

    def getUserInfo(self, username='ME'):
        """
        Get LDAP info for given user

        Lora: /user/:user
        """
        response = self.get(self.build_url('user', username))
        return response.json()

    def getUserMappings(self, username='ME'):
        """
        Get LC mappings (alternate usernames) corresponding to given username

        Lora: /user/:user/mappings
        """
        response = self.get(self.build_url('user', username, 'mappings'))
        return response.json()

    def getUserOun(self, username='ME'):
        """
        Get OUN corresponding to given username

        Lora: /user/:user/oun
        """
        response = self.get(self.build_url('user', username, 'oun'))
        return response.json()

    def getFilesystemStatus(self, filesystem=''):
        """
        Get status of filesystem

        Lora: /status/filesystem/:filesystem
        """
        if filesystem == '':
            response = self.get(self.build_url('status', 'filesystem'))
        else:
            response = self.get(self.build_url('status', 'filesystem', filesystem))
        return response.json()

    def getPrinterInfo(self, printerQueue):
        """
        Get information for a given printer

        Lora: /printer/:printerQueue
        """
        response = self.get(self.build_url('printer', printerQueue))
        return response.json()

    def getAllPrinterInfo(self):
        """
        Get information for all printers

        Lora: /printers/details
        """
        response = self.get(self.build_url('printers', 'details'))
        return response.json()

    def getTossStats(self):
        """
        Get update statistics for CHAOS and TOSS

        Lora: /chaos
        """
        response = self.get(self.build_url('chaos'))
        return response.json()

    def getUserCompletedJobs(self, period, username='ME'):
        """
        Get list of a user's completed jobs for a given time period

        Lora: /user/:user/queue?type=completed&period=:period
        """
        payload = {'type': 'completed', 'period': period}
        response = self.get(self.build_url('user', username, 'queue'), params=payload)
        return response.json()

    def getPathStat(self, host, path):
        """
        Get the information provided by 'stat' on a given path

        Lora: /file/:host:path?view=stat
        """
        payload = {'view': 'stat'}
        response = self.get(self.build_url('file', host, path), params=payload)
        return response.json()

    def execCommand(self, host, command, options={}):
        """
        Run a command on a host

        Lora: /command/:host
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = options
        payload['command'] = command
        response = self.post(self.build_url('command', host), headers=headers, data=payload)
        return response.json()

    # Job-Related Functions

    def submitJob(self, host, options={}):
        """
        Submit a job on a host

        Lora: /queue/:host
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = self.post(self.build_url('queue', host), headers=headers, data=options)
        return response.json()

    def getJobDetails(self, host, jobid):
        """
        Get details about given job on given host

        Lora: /queue/:host/:jobid?livedata=1
        """
        payload = {'livedata': 1}
        response = self.get(self.build_url('queue', host, jobid), params=payload)
        return response.json()

    def getSacctJobDetails(self, host, jobid, startDate, endDate):
        """
        Get details about a job using Slurm sacct command

        Lora: /queue/:host/:jobid/jobdetails?startDate=:startDate&endDate=:endDate
        """
        payload = {'startDate': startDate, 'endDate': endDate}
        response = self.get(self.build_url('queue', host, jobid, 'jobdetails'), params=payload)
        return response.json()

    def getJobScript(self, host, jobid, date):
        """
        Get job script for given job; requires special access

        Lora: /queue/:host/:jobid/:date/jobscript
        """
        response = self.get(self.build_url('queue', host, jobid, date, 'jobscript'))
        return response.json()

    def getJobSteps(self, host, jobid):
        """
        Get the job steps for a job on a host

        Lora: /queue/:host/:jobid/steps
        """
        response = self.get(self.build_url('queue', host, jobid, 'steps'))
        return response.json()

    def checkJob(self, host, jobid):
        """
        Run checkjob on a job on a host

        Lora: /queue/:host/:jobid/check
        """
        response = self.get(self.build_url('queue', host, jobid, 'check'))
        return response.json()

    def editJobParams(self, host, jobid, options={}):
        """
        Edit parameters for a job on a host

        Lora: /queue/:host/:jobid
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = options
        payload['operator'] = 'modify'
        response = self.put(self.build_url('queue', host, jobid), headers=headers, data=payload)
        return response.json()

    def sendJobSignal(self, host, jobid, signal):
        """
        Send a signal to a job on a host

        Lora: /queue/:host/:jobid
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'operator': 'signal', 'signal': signal}
        response = self.put(self.build_url('queue', host, jobid), headers=headers, data=payload)
        return response.json()

    def holdJob(self, host, jobid):
        """
        Hold a job on a host

        Lora: /queue/:host/:jobid
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'operator': 'hold'}
        response = self.put(self.build_url('queue', host, jobid), headers=headers, data=payload)
        return response.json()

    def unholdJob(self, host, jobid):
        """
        Unhold a job on a host

        Lora: /queue/:host/:jobid
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'operator': 'unhold'}
        response = self.put(self.build_url('queue', host, jobid), headers=headers, data=payload)
        return response.json()

    def cancelJob(self, host, jobid):
        """
        Cancel a job on a host

        Lora: /queue/:host/:jobid
        """
        response = self.delete(self.build_url('queue', host, jobid))
        return response.json()

    # License Functions

    def getAllLicenses(self):
        """
        Get a list of all licenses

        Lora: /status/license
        """
        response = self.get(self.build_url('status', 'license'))
        return response.json()

    def getLicenseInfo(self, licenseName):
        """
        Get information on a license

        Lora: /status/license/:license
        """
        response = self.get(self.build_url('status', 'license', licenseName))
        return response.json()

    def getAllLicenseInfo(self):
        """
        Get information on all licenses

        Lora: /status/license/all
        """
        response = self.get(self.build_url('status', 'license', 'all'))
        return response.json()

    # GiveTake Functions

    def getMyGiveTake(self):
        """
        Get my give take status

        Lora: /user/ME/givetake
        """
        response = self.get(self.build_url('user', 'ME', 'givetake'))
        return response.json()

    def takeMyFiles(self, targetDir, fromUsers, force=0):
        """
        Take files given to you

        Lora: /user/ME/take

        Note: 'fromUsers' arg must be a list for multiple

        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'target': targetDir, 'from[]': fromUsers, 'force': force}
        response = self.post(self.build_url('user', 'ME', 'take'), headers=headers, data=payload)
        return response.json()

    def giveMyFiles(self, files, to, force=0):
        """
        Give files to another user

        Lora: /user/ME/give

        Note: 'files' arg must be a list for multiple, 'to' arg must be a list for multiple
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'files[]': files, 'to[]': to, 'force': force}
        response = self.post(self.build_url('user', 'ME', 'give'), headers=headers, data=payload)
        return response.json()

    # Other Functions

    def getUserSshHosts(self, username='ME'):
        """
        Get a list of the given user's ssh hosts

        LORA: /user/:user/sshhosts
        """
        response = self.get(self.build_url('user', username, 'sshhosts'))
        return response.json()

    def getBankMembership(self, bank, host):
        """
        Get membership list of a bank on a host

        LORA: /bank/:bank/membership/:host
        """
        response = self.get(self.build_url('bank', bank, 'membership', host))
        return response.json()

    def getScratchFilesystems(self):
        """
        Get a list of scratch filesystems

        LORA: /scratchfs
        """
        response = self.get(self.build_url('scratchfs'))
        return response.json()

    def getParallelFilesystems(self):
        """
        Get a list of parallel filesystems

        LORA: /parallelfs
        """
        response = self.get(self.build_url('parallelfs'))
        return response.json()

    def getMyPurgedFiles(self, days=''):
        """
        Get your purged files for a given number of days

        LORA: /user/ME/purgedFiles?days=:days
        """
        if days == '':
            response = self.get(self.build_url('user', 'ME', 'purgedFiles'))
        else:
            payload = {'days': days}
            response = self.get(self.build_url('user', 'ME', 'purgedFiles'), params=payload)
        return response.json()

    def getAllUsers(self):
        """
        Get a list of all users

        LORA: /users
        """
        response = self.get(self.build_url('users'))
        return response.json()

    def getAllUsersInfo(self, dataType=''):
        """
        Get info for all users in dict or list format

        LORA: /users?info=all&type=:dataType
        """
        payload = {'info': 'all'}
        if dataType != '':
            payload['type'] = 'array'
        response = self.get(self.build_url('user'), params=payload)
        return response.json()

    def isUserInGroup(self, group, username='ME'):
        """
        Check if user is a member of a group

        LORA: /user/:user/group/:group
        """
        response = self.get(self.build_url('user', username, 'group', group))
        return response.json()

    def getUserPocContactees(self, oun):
        """
        Get a list of who the user (by oun) is POC for

        LORA: /user/:oun/contactees
        """
        response = self.get(self.build_url('user', oun, 'contactees'))
        return response.json()

    def getFileUrl(self, host, path):
        """
        Get the url for a file

        LORA: /lorenz/lora/lora.cgi/file/:host/:path?view=read&format=auto
        """
        return self.build_url('file', host, path) + '?view=read&format=auto'

    def getDirListing(self, host, path):
        """
        Get the directory listing for path on host

        LORA: /file/:host/:path?view=list
        """
        payload = {'view': 'list'}
        response = self.get(self.build_url('file', host, path), params=payload)
        return response.json()

    def getRecentImage(self, host, path, nameFormat):
        """
        Get a recent image

        LORA: /file/image/:host:path?nameFormat=:nameFormat
        """
        payload = {'nameFormat': nameFormat}
        response = self.get(self.build_url('file', 'image', host, path), params=payload)
        return response.json()

    def readFile(self, host, path):
        """
        Read a file from host

        LORA: /file/:host/:path?view=read&format=auto
        """
        payload = {'view': 'read', 'format': 'auto'}
        response = self.get(self.build_url('file', host, path), params=payload)
        return response.text

    def getUserTransferHosts(self, username='ME'):
        """
        Get a list of transfer hosts for a user

        LORA: /user/:user/transferhosts
        """
        response = self.get(self.build_url('user', username, 'transferhosts'))
        return response.json()

    def getNetworkInfo(self):
        """
        Get info from the network you are on

        LORA: /support/network
        """
        response = self.get(self.build_url('support', 'network'))
        return response.json()

    def getMachineStatus(self):
        """
        Get statuses of machines

        LORA: /status/machines
        """
        response = self.get(self.build_url('status', 'machines'))
        return response.json()

    def getUserEnclaveStatus(self, username='ME'):
        """
        Get the enclave status of a user

        LORA: /user/:user/enclavestatus
        """
        response = self.get(self.build_url('user', username, 'enclavestatus'))
        return response.json()

    def getWeather(self):
        """
        Get weather information from local source

        Lora: /weather
        """
        response = self.get(self.build_url('weather'))
        return response.json()

    def getClusterBackfill(self):
        """
        Get backfill info for all clustersLDAP info for given user

        Lora: /clusters/backfill
        """
        response = self.get(self.build_url('clusters', 'backfill'))
        return response.json()

    def getLoginNodeStatus(self):
        """
        Get status for all login nodes

        Lora: /status/loginNode
        """
        response = self.get(self.build_url('status', 'loginNode'))
        return response.json()

    def getUserProcessesForHost(self, host, username='ME'):
        """
        Get processes for given user on given host

        Lora: /user:user/cluster/:host/processes
        """
        response = self.get(self.build_url('user', username, 'cluster', host, 'processes'))
        return response.json()

    def getAllUserProcesses(self, username='ME'):
        """
        Get processes for given user on all hosts

        Lora: /user:user/cluster/processes
        """
        response = self.get(self.build_url('user', username, 'cluster', 'processes'))
        return response.json()

    def killProcess(self, hosts, pids):
        """
        Kill specified processes on given hosts

        Lora: /cluster/processes [POST]

        Note: 'pids' arg must be a list for multiple
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'clusters[]': hosts, 'processes[]': pids}
        response = self.post(self.build_url('cluster', 'processes'), headers=headers, data=payload)
        return response.json()

    def tailFile(self, host, path, nlines):
        """
        Get trailing lines from given file

        Lora: /data/:host [POST]
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'host': host, 'path': path, 'tail': nlines, 'type': 'text'}
        response = self.post(self.build_url('data', host), headers=headers, data=payload)
        return response.json()

    def getLustreDowntime(self, lustreArgs):
        """
        Get details about past Lustre downtimes

        Lora: /lustre/downtime [POST]
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = lustreArgs
        response = self.post(self.build_url('lustre', 'downtime'), headers=headers, data=payload)
        return response.json()

    def getLustreNickname(self, filesystem=''):
        """
        Get the nickname of a filesystem or all filesystems

        LORA: /lustre/nickname/?filesys=:filesystem
        """
        if(filesystem == ''):
            response = self.get(self.build_url('lustre', 'nickname') + '/')
        else:
            payload = {'filesys': filesystem}
            response = self.get(self.build_url('lustre', 'nickname') + '/', params=payload)
        return response.json()

    def getMachineEvents(self, eventType, eventArgs):
        """
        Get details about events on machines

        Lora: /events/:type [POST]
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = eventArgs
        response = self.post(self.build_url('events', eventType), headers=headers, data=payload)
        return response.json()

    def getClusterBatchDetails(self, host, username='ME'):
        """
        Get batch details for given host and user

        Lora: /user/:user/cluster/:host/batchdetails
        """
        response = self.get(self.build_url('user', username, 'cluster', host, 'batchdetails'))
        return response.json()

    def getAllClusterBatchDetails(self):
        """
        Get batch details for all hosts

        Lora: /clusters/batchdetails
        """
        response = self.get(self.build_url('clusters', 'batchdetails'))
        return response.json()

class RZLoraSession(LoraSession):
    domain = 'https://rzlc.llnl.gov'
    login_prompt = 'Pin & Cryptocard: '
