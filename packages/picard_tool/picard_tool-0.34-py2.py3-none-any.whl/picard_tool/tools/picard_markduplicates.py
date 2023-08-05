import os
import sys

import pandas as pd

from cdis_pipe_utils import df_util
from cdis_pipe_utils import fastq_util
from cdis_pipe_utils import time_util
from cdis_pipe_utils import pipe_util


def picard_markduplicates_to_dict(uuid, bam_path, metrics_path, logger):
    data_dict = dict()
    read_header = False
    with open(metrics_path, 'r') as metrics_open:
        for line in metrics_open:
            if line.startswith("## HISTOGRAM"):
                break
            if line.startswith('#') or len(line) < 5:
                continue
            if not read_header:
                value_key_list = line.strip('\n').split('\t')
                logger.info('picard_markduplicates_to_dict() header value_key_list=\n\t%s' % value_key_list)
                logger.info('len(value_key_list=%s' % len(value_key_list))
                read_header = True
            else:
                data_list = line.strip('\n').split('\t')
                logger.info('picard_markduplicates_do_dict() data_list=\n\t%s' % data_list)
                logger.info('len(data_list)=%s' % len(data_list))
                for value_pos, value_key in enumerate(value_key_list):
                    data_dict[value_key] = data_list[value_pos]
    logger.info('picard_markduplicates data_dict=%s' % data_dict)
    return data_dict


def bam_markduplicates(uuid, bam_path, engine, logger, be_lenient):
    md_dir = os.path.join(os.getcwd(), 'md')
    os.makedirs(md_dir, exist_ok=True)
    logger.info('md_dir=%s' % md_dir)
    step_dir = md_dir
    outbam = os.path.basename(bam_path)
    outbam_path = os.path.join(md_dir, outbam)
    metrics_path = outbam_path + '.metrics'
    logger.info('outbam_path=%s' % outbam_path)
    home_dir = os.path.expanduser('~')

    ## do work
    if pipe_util.already_step(step_dir, 'picard_markduplicates', logger):
        logger.info('already completed step `picard markduplicates` of: %s' % bam_path)
    else:
        logger.info('running step `picard markduplicates` of: %s' % bam_path)
        #max_fastq_length = fastq_util.get_max_fastq_length_from_db(engine, logger)
        # + 10 needed for
        # Exception in thread "main" picard.PicardException: Found a samRecordWithOrdinal with sufficiently large clipping that we may have
        #missed including it in an early duplicate marking iteration.  Please increase the minimum distance to at least 153bp
        #to ensure it is considered (was 152).
        #minimum_distance = str(2 * max_fastq_length + 10)
        cmd = ['java', '-d64', '-jar', os.path.join(home_dir, 'tools/picard-tools/picard.jar'), 'MarkDuplicates', 'INPUT=' + bam_path, 'OUTPUT=' + outbam_path, 'METRICS_FILE=' + metrics_path, 'TMP_DIR=' + md_dir ,'CREATE_INDEX=true'] # 'MINIMUM_DISTANCE=' + minimum_distance,
        if be_lenient:
            cmd.append('VALIDATION_STRINGENCY=LENIENT')
        output = pipe_util.do_command(cmd, logger, allow_fail=False)

        #store time/mem to db
        df = time_util.store_time(uuid, cmd, output, logger)
        df['bam_path'] = bam_path
        unique_key_dict = {'uuid': uuid, 'bam_path': bam_path}
        table_name = 'time_mem_picard_MarkDuplicates'
        df_util.save_df_to_sqlalchemy(df, unique_key_dict, table_name, engine, logger)
        pipe_util.create_already_step(step_dir, 'picard_markduplicates', logger)
        logger.info('completed running step `picard markduplicates` of: %s' % bam_path)

    ## save stats to db
    if pipe_util.already_step(step_dir, 'picard_markduplicates_db', logger):
        logger.info('already stored `picard markduplicates` of %s to db' % bam_path)
    else:
        data_dict = picard_markduplicates_to_dict(uuid, bam_path, metrics_path, logger)
        data_dict['uuid'] = [uuid]
        data_dict['bam_path'] = bam_path
        df = pd.DataFrame(data_dict)
        table_name = 'picard_MarkDuplicates'
        unique_key_dict = {'uuid': uuid, 'bam_path': bam_path}
        df_util.save_df_to_sqlalchemy(df, unique_key_dict, table_name, engine, logger)
        pipe_util.create_already_step(step_dir, 'picard_markduplicates_db', logger)
        logger.info('completed storing `picard markduplicates` of %s to db' % bam_path)
    return outbam_path
