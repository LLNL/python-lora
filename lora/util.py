"""
A collection of utilities and examples for working with the Lora REST API
"""

from collections import Counter


def get_num_jobs_per_host(lora_session):
    """
    Returns the number of jobs on each host in the center
    """
    jobs = lora_session.getAllJobDetails()['output']['jobs']
    hosts = [j['Host'] for j in jobs]
    return Counter(hosts)
