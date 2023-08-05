#!/usr/bin/env python

import argparse
import configparser
import datetime
import logging
import os
import time

import sqlalchemy
import pandas as pd

from cdis_pipe_utils import df_util
from cdis_pipe_utils import pipe_util
from cdis_pipe_utils import time_util
from cdis_pipe_utils import postgres

def get_db_cred(db_cred_s3url, s3cfg_path, logger):
    cmd = ['s3cmd', '-c', s3cfg_path, 'get', '--force', db_cred_s3url]
    output = pipe_util.do_command(cmd, logger)
    db_cred_path = os.path.basename(db_cred_s3url)
    return db_cred_path

def get_connect_dict(db_cred_s3url, s3cfg_path, logger):
    db_cred_path = get_db_cred(db_cred_s3url, s3cfg_path, logger)
    config = configparser.ConfigParser()
    config.read(db_cred_path)
    connect_dict = dict(config['DEFAULT'])
    os.remove(db_cred_path)
    return connect_dict
    

def main():
    parser = argparse.ArgumentParser('update status of job')
    # Logging flags.
    parser.add_argument('-d', '--debug',
        action = 'store_const',
        const = logging.DEBUG,
        dest = 'level',
        help = 'Enable debug logging.',
    )
    parser.set_defaults(level = logging.INFO)

    parser.add_argument('--case_id',
                        required=True
    )
    parser.add_argument('--gdc_id',
                        required=True
    )
    parser.add_argument('--repo',
                        required = True
    )
    parser.add_argument('--repo_hash',
                        required = True
    )
    parser.add_argument('--s3_url',
                        required = False
    )
    parser.add_argument('--status',
                        required = True
    )
    parser.add_argument('--table_name',
                        required=True
    )

    # optional for remote db access
    parser.add_argument('--db_cred_s3url',
                        required = False # optional. not req when sqlite engine
    )
    parser.add_argument('--s3cfg_path',
                        required = True
    )

    args = parser.parse_args()

    case_id = args.case_id
    gdc_id = args.gdc_id
    repo = args.repo
    repo_hash = args.repo_hash
    status = args.status
    table_name = args.table_name
    if args.s3_url is not None:
        s3_url = args.s3_url
    else:
        s3_url = None

    if args.s3cfg_path:
        s3cfg_path = args.s3cfg_path
    if args.db_cred_s3url:
        db_cred_s3url = args.db_cred_s3url
    else:
        db_cred_s3url = None # when None, then setup sqlite engine
        
        
    tool_name = 'queue_status'
    logger = pipe_util.setup_logging(tool_name, args, gdc_id)

    if db_cred_s3url is not None: #db server case
        conn_dict = pipe_util.get_connect_dict(db_cred_s3url, s3cfg_path, logger)
        engine = sqlalchemy.create_engine(sqlalchemy.engine.url.URL(**conn_dict))
    else: # local sqlite case
        sqlite_name = case_id + '.db'
        engine_path = 'sqlite:///' + sqlite_name
        engine = sqlalchemy.create_engine(engine_path, isolation_level='SERIALIZABLE')


    status_dict = dict()
    status_dict['case_id'] = case_id
    status_dict['gdc_id'] = [gdc_id]
    status_dict['repo'] = repo
    status_dict['repo_hash'] = repo_hash
    status_dict['status'] = status
    if s3_url is not None:
        status_dict['s3_url'] = s3_url
    else:
        status_dict['s3_url'] = None


    time_seconds = time.time()
    datetime_now = str(datetime.datetime.now())
    
    status_dict['time_seconds'] = time_seconds
    status_dict['datetime_now'] = datetime_now
    logger.info('writing status_dict=%s' % str(status_dict))
    df = pd.DataFrame(status_dict)
    
    unique_key_dict = {'case_id': case_id, 'gdc_id': gdc_id, 'repo_hash': repo_hash, 'status': status }
    df_util.save_df_to_sqlalchemy(df, unique_key_dict, table_name, engine, logger)

    return


if __name__ == '__main__':
    main()
