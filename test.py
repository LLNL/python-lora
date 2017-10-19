#! /usr/bin/env python

import logging
import json
import lora


try:
    input = raw_input  # Python 2
except NameError:
    pass

logging.basicConfig(level=logging.INFO, format='%(message)s')


def test_endpoint(json_obj):
    """
    Helper function for verifying desired output from tests
    """
    print(json.dumps(json_obj, indent=4, sort_keys=True))
    print('If everything looks normal, press Enter to continue:')
    input()


if __name__ == '__main__':
    session = lora.LoraSession()
    session.login()

    print('\n-- User Endpoints --')
    test_endpoint(session.getUserInfo())
    test_endpoint(session.getUserInfo('jwlong'))

    print('\n-- User Groups --')
    test_endpoint(session.getUserGroups())
    test_endpoint(session.getUserGroups('jwlong'))

    print('\n-- Groups --')
    test_endpoint(session.getAllGroups())

    print('\n-- User Banks --')
    test_endpoint(session.getUserBanks())
    test_endpoint(session.getUserBanks('jwlong'))

    print('\n-- Banks --')
    test_endpoint(session.getAllBanks())

    print('\n-- User Banks By Host --')
    test_endpoint(session.getUserBanksByHost())
    test_endpoint(session.getUserBanksByHost('jwlong'))

    print('\n-- User Accounts --')
    test_endpoint(session.getUserAccounts())
    test_endpoint(session.getUserAccounts('jwlong'))

    print('\n-- User Clusters --')
    test_endpoint(session.getUserClusters())
    test_endpoint(session.getUserClusters('jwlong'))

    print('\n-- Job Details --')
    test_endpoint(session.getAllJobDetails())

    print('\n-- Job Counts By User --')
    test_endpoint(session.getAllJobCountsByUser())

    print('\n-- Jobs For Host --')
    test_endpoint(session.getAllJobDetailsForHost('cab'))

    print('\n-- User Default Host --')
    test_endpoint(session.getUserDefaultHost())
    test_endpoint(session.getUserDefaultHost('jwlong'))

    print('\n-- Group Info --')
    test_endpoint(session.getGroupInfo('stg'))

    print('\n-- Bank Info --')
    test_endpoint(session.getBankInfo('lc'))

    print('\n-- All Clusters --')
    test_endpoint(session.getAllClusters())

    print('\n-- All Clusters Mounts --')
    test_endpoint(session.getAllClustersMounts())

    print('\n-- Host Info --')
    test_endpoint(session.getHostInfo('cab'))

    print('\n-- Host Job Limits --')
    test_endpoint(session.getHostJobLimits('cab'))

    print('\n-- Host Details --')
    test_endpoint(session.getHostDetails('cab'))

    print('\n-- Host Topology --')
    test_endpoint(session.getHostTopology('cab'))

    print('\n-- All Machine Loads --')
    test_endpoint(session.getAllMachineLoads())

    print('\n-- All Cluster Utilizations --')
    test_endpoint(session.getAllClusterUtilizations())

    print('\n-- LC Organizations --')
    test_endpoint(session.getAllLcOrganizations())

    print('\n-- Core Coordinators --')
    test_endpoint(session.getAllCoreCoordinators())

    print('\n-- All News --')
    test_endpoint(session.getAllNews())

    print('\n-- User News --')
    test_endpoint(session.getUserNews())
    test_endpoint(session.getUserNews('jwlong'))

    print('\n-- News Item --')
    test_endpoint(session.getNewsItem('DotKit'))

    print('\n-- User Disk Quota Info --')
    test_endpoint(session.getUserDiskQuotaInfo('choate5'))

    print('\n-- User Cpu Usage --')
    test_endpoint(session.getUserCpuUsage('mrhee'))

    print('\n-- User Jobs --')
    test_endpoint(session.getUserJobs('mrhee'))

    print('\n-- User Jobs for Host --')
    test_endpoint(session.getUserJobsForHost('cab', 'mrhee'))

    print('\n-- Bank History --')
    test_endpoint(session.getBankHistory('lc'))

    print('\n-- Bank History for Host --')
    test_endpoint(session.getBankHistoryForHost('lc', 'cab'))

    print('\n-- User Info --')
    test_endpoint(session.getUserInfo())
    test_endpoint(session.getUserInfo('lee1001'))

    print('\n-- User Mappings --')
    test_endpoint(session.getUserMappings())
    test_endpoint(session.getUserMappings('jwlong'))

    print('\n-- User Oun --')
    test_endpoint(session.getUserOun('jwlong'))

    print('\n-- Job Details --')
#    Suggestion: get jobid from the getUserJobsForHost() func, then use here
#    jwl 7/18/2016
#    test_endpoint(session.getJobDetails('cab', jobid))

    print('\n-- Filesystem Status (all) --')
    test_endpoint(session.getFilesystemStatus())

    print('\n-- Filesystem Status (one) --')
    test_endpoint(session.getFilesystemStatus('/p/lscratche'))

    print('\n-- Printer Info --')
    test_endpoint(session.getPrinterInfo('p049'))

    print('\n-- All Printer Info --')
    test_endpoint(session.getAllPrinterInfo())

    print('\n-- TOSS Stats --')
    test_endpoint(session.getTossStats())

    print('\n-- User Completed Jobs --')
    test_endpoint(session.getUserCompletedJobs(3))
    test_endpoint(session.getUserCompletedJobs(3, 'mrhee'))

    print('\n-- Path Stat --')
    test_endpoint(session.getPathStat('oslic', '/g/g0/choate5/tmpfile'))

    print('\n-- Exec Command--')
    test_endpoint(session.execCommand('vulcan', 'ls', {'timeout': 30, 'mode': 'nofail'}))

    print('\n-- Licenses --')
    test_endpoint(session.getAllLicenses())

    print('\n-- License Info --')
    test_endpoint(session.getLicenseInfo('ddt'))

    print('\n-- All License Info --')
    test_endpoint(session.getAllLicenseInfo())

    print('\n-- My Give Take --')
    test_endpoint(session.getMyGiveTake())

    print('\n-- Take File--')
    test_endpoint(session.takeMyFiles('~/test', 'choatea'))
    test_endpoint(session.takeMyFiles('~/test', ['choatea', 'choatez']))

    print('\n-- Give File --')
    test_endpoint(session.giveMyFiles('~/notes', 'choatea'))
    test_endpoint(session.giveMyFiles(['~/notes, ~/tmpfile'], ['choatea', 'choatez']))

    print('\n-- Get User SSH hosts --')
    test_endpoint(session.getUserSshHosts())
    test_endpoint(session.getUserSshHosts('jwlong'))

    print('\n-- Get bank membership --')
    test_endpoint(session.getBankMembership('lc', 'cab'))

    print('\n-- Get scratch filesystems --')
    test_endpoint(session.getScratchFilesystems())

    print('\n-- Get parallel filesystems --')
    test_endpoint(session.getParallelFilesystems())

    print('\n-- Get my purged files --')
    test_endpoint(session.getMyPurgedFiles())
    test_endpoint(session.getMyPurgedFiles(3))

    print('\n-- Get all users --')
    test_endpoint(session.getAllUsers())

    print('\n-- Get all users info --')
    test_endpoint(session.getAllUsersInfo())
    test_endpoint(session.getAllUsersInfo('array'))

    print('\n-- Is user in group --')
    test_endpoint(session.isUserInGroup('hotline'))
    test_endpoint(session.isUserInGroup('hotline', 'lee1001'))

    print('\n-- Get user POC contactees --')
    test_endpoint(session.getUserPocContactees('long6'))

    print('\n-- Get file url --')
    test_endpoint(session.getFileUrl('cab', '/g/g0/choate5/notes'))

    print('\n-- Get directory listing --')
    test_endpoint(session.getDirListing('cab', '/g/g0/choate5/test'))

    print('\n-- Get user transfer hosts --')
    test_endpoint(session.getUserTransferHosts())
    test_endpoint(session.getUserTransferHosts('choatez'))

    print('\n-- Get network info --')
    test_endpoint(session.getNetworkInfo())

    print('\n-- Get machine statuses --')
    test_endpoint(session.getMachineStatus())

    print('\n-- Get user enclave status --')
    test_endpoint(session.getUserEnclaveStatus())
    test_endpoint(session.getUserEnclaveStatus('choatea'))

    print('\n-- Read file --')
    test_endpoint(session.readFile('cab', '/g/g0/choate5/notes'))

    print('\n-- Get lustre nickname --')
    test_endpoint(session.getLustreNickname())
    test_endpoint(session.getLustreNickname('lscratche'))

    print('\n-- Weather --')
    test_endpoint(session.getWeather())

    print('\n-- Cluster Backfill --')
    test_endpoint(session.getClusterBackfill())

    print('\n-- Login Node Status --')
    test_endpoint(session.getLoginNodeStatus())

    print('\n-- User Processes on Host --')
    test_endpoint(session.getUserProcessesForHost('cab', 'choate5'))
    test_endpoint(session.getUserProcessesForHost('cab'))

    print('\n-- User Processes on All Hosts --')
    test_endpoint(session.getAllUserProcesses('choate5'))

    print('\n-- Kill Process --')
    # Suggestion: get pid from getUserProcessesForHost() func, then use here
    # jwl 8/4/2016
    # test_endpoint(session.killProcess('cab689-pub', 240402))
    # test_endpoint(session.killProcess(['cab669-pub','cab669-pub'], [77978,75010]))

    print('\n-- Tail File --')
    test_endpoint(session.tailFile('cab', '/etc/passwd', 5))

    print('\n-- Get Luster Downtimes --')
    test_endpoint(session.getLustreDowntime({'monthly': 'all'}))

    print('\n-- Get Machine Evenets --')
    test_endpoint(session.getMachineEvents('calendar', {'category': 'all'}))

    print('\n-- Get Sacct Job Details --')
    test_endpoint(session.getSacctJobDetails('cab', 2093226, '2016-08-03 00:00:00', '2016-08-05 00:00:00'))

    print('\n-- Get Job Script --')
    test_endpoint(session.getJobScript('cab', 419131, '2016-08-04'))

    print('\n-- Get Cluster Batch Details --')
    test_endpoint(session.getClusterBatchDetails('cab', 'jwlong'))

    print('\n-- Get All Cluster Batch Details --')
    test_endpoint(session.getAllClusterBatchDetails())
