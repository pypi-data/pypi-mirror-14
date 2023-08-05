#!/usr/bin/env python

import argparse
import logging
import os
import sys

import pysam
import sqlalchemy

from cdis_pipe_utils import pipe_util
from cdis_pipe_utils import time_util


def get_readgroup_dict(bam_path):
    samfile = pysam.AlignmentFile(bam_path, 'rb')
    samfile_header = samfile.header
    readgroup_dict_list = samfile_header['RG']
    return readgroup_dict_list

def add_readgroup_platform(readgroup_dict_list, platform_name):
    for readgroup_dict in readgroup_dict_list:
        if readgroup_dict['PL']:
            continue
        else:
            readgroup_dict['PL'] = platform_name
    return readgroup_dict_list

def write_header_to_file(case_id, bam_path, engin, logger):
    bam_name = os.path.basename(bam_path)
    header_name = bam_name + '.header'
    step_dir = os.getcwd()
    
    if pipe_util.already_step(step_dir, header_name, logger):
        logger.info('already written header: %s' % header_name)
    else:
        cmd = ['samtools', 'view', '-H', bam_path, '>', header_name]
        shell_cmd = ' '.join(cmd)
        output = pipe_util.do_shell_command(shell_cmd, logger)
        df = time_util.store_time(case_id, shell_cmd, output, logger)
        df['bam_name'] = bam_name
        unique_key_dict = {'uuid': case_id, 'bam_name': bam_name }
        table_name = 'time_mem_samtools_view_header'
        #df_util.save_df_tosqlalchemy(df, unique_key_dict, table_name, engine, logger)
        pipe_util.create_already_step(step_dir, header_name, logger)
    return header_name

def substitute_readgroup(readgroup_dict_list, header_name, engine, logger):
    in_name, in_ext = os.path.splitext(header_name)
    reheader_name = in_name + '.reheader'
    step_dir = os.getcwd()
    
    if pipe_util.already_step(step_dir, reheader_name, logger):
        logger.info('already written reheader: %s' % reheader_name)
    else:
        cnt = 0
        outfile_open = open(reheader_name, 'w')
        with open(header_name, 'r') as header_open:
            for line in header_open:
                if line.startswith('@RG'):
                    readgroup_line = '@RG\t' + '\t'.join([ key+':'+value for key, value in sorted(readgroup_dict_list[cnt].items()) ])
                    cnt += 1
                    outfile_open.write(readgroup_line)
                else:
                    outfile_open.write(line)
        pipe_util.create_already_step(step_dir, reheader_name, logger)
    return reheader_name

def do_reheader_bam(case_id, reheader_name, bam_path, engine, logger):
    step_dir = os.getcwd()
    bam_name = os.path.basename(bam_path)
    if pipe_util.already_step(step_dir, bam_name + '_rhdr_complete', logger):
        logger.info('already reheadered BAM: %s' % bam_name)
    else:
        cmd = ['samtools', 'reheader', reheader_name, bam_path, '>', bam_name]
        shell_cmd = ' '.join(cmd)
        output = do_shell_command(shell_cmd, logger)
        df = time_util.store_time(case_id, shell_cmd, output, logger)
        df['bam_name'] = bam_name
        unique_key_dict = {'uuid': case_id, 'bam_name': bam_name }
        table_name = 'time_mem_samtools_reheader'
        df_util.save_df_tosqlalchemy(df, unique_key_dict, table_name, engine, logger)
        pipe_util.create_already_step(step_dir, bam_name + '_rhdr_complete', logger)
    return bam_name
        
def write_platformed_bam(case_id, bam_path, readgroup_dict_list, engine, logger):
    header_name = write_header_to_file(case_id, bam_path, engine, logger)
    reheader_name = substitute_readgroup(readgroup_dict_list, header_name, engine, logger)
    reheader_bam = do_reheader_bam(case_id, reheader_name, bam_path, engine, logger)
    return reheader_bam

def main():
    parser = argparse.ArgumentParser('reheader a BAM to include readgroup PL, if not present')

    # Logging flags.
    parser.add_argument('-d', '--debug',
        action = 'store_const',
        const = logging.DEBUG,
        dest = 'level',
        help = 'Enable debug logging.',
    )
    parser.set_defaults(level = logging.INFO)


    # Optional db flags
    parser.add_argument('--db_cred_s3url',
                        required = False
    )
    parser.add_argument('--s3cfg_path',
                        required = False
    )

    
    # Tool flags
    parser.add_argument('-b', '--bam_path',
                        required = True
    )
    parser.add_argument('-c', '--case_id',
                        required = True
    )
    parser.add_argument('-p', '--platform_name',
                        required = True
    )

    args = parser.parse_args()
    bam_path = args.bam_path
    case_id = args.case_id

    bam_name = os.path.basename(bam_path)
    
    logger = pipe_util.setup_logging('readgroup_platform_insertion', args, bam_name)

    if db_cred_s3url is not None: #db server case
        conn_dict = pipe_util.get_connect_dict(db_cred_s3url, s3cfg_path, logger)
        engine = sqlalchemy.create_engine(sqlalchemy.engine.url.URL(**conn_dict))
    else: # local sqlite case
        sqlite_name =  bam_name + '_RGPL.db'
        engine_path = 'sqlite:///' + sqlite_name
        engine = sqlalchemy.create_engine(engine_path, isolation_level='SERIALIZABLE')

    hostname = os.uname()[1]
    logger.info('hostname=%s' % hostname)

    original_readgroup_dict_list = get_readgroup_dict(bam_path)
    platformed_readgroup_dict_list = add_readgroup_platform(original_readgroup_dict, platform_name)
    reheader_bam = write_platformed_bam(case_id, bam_path, platformed_readgroup_dict_list, engine, logger)
    return


if __name__ == '__main__':
    main()
