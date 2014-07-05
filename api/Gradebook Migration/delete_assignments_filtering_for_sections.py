#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
'''
delete assignments after they've been migrated
'''

import qs
import pickle
import pprint
import requests
from tqdm import *


def main():
    # =========
    # = Setup =
    # =========
    api_key = qs.api_key
    filename = qs.get_filename()
    use_live_server = qs.use_live_server
    base_url = qs.get_base_url(use_live_server)

    qs.check(filename, use_live_server)
    valid_assignments = pickle.load(open(filename))
    # posted_assignment_ids = pickle.load(open("posted_{}".format(filename)))
    # len = 33
    posted_section_ids = ['563712', '564604', '564606', '564519', '552762', '564516', '552764', '552600', '552602', '552624', '552626', '565785', '552625', '563648', '552698', '552756', '552754', '552755', '552772', '568438', '568441', '552631', '552633', '552635', '568437']
    # posted_section_ids = ['552698', '552756', '552754', '552755', '552772', '568438', '568441', '552631', '552633', '552635', '568437']

    success = []
    error = []

    # =============================
    # = Loop through old sections =
    # =============================
    print valid_assignments.keys()
    for i trange(0, len(valid_assignments), desc='DEL', leave=True):
        section_id = valid_assignments.keys()[i]
        if not section_id in posted_section_ids:
            continue

        # =======================================
        # = Loop through assignments in section =
        # =======================================
        for assignment in valid_assignments[section_id]:
            assignment_id = assignment['assignmentId']

            # if assignment_id in posted_assignment_ids:
            d = requests.delete("{}sections/{}/assignments/{}".format(base_url,
                                                                      section_id,
                                                                      assignment_id),
                                params={'apiKey': api_key})
            log = qs.ser(d.json(), {'section_id': section_id,
                                       'assignment': assignment})
            if d.json()['success']:
                success.append(log)
            else:
                error.append(log)

    qs.dump_logs(success, error)

if __name__ == '__main__':
    main()
