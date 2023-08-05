import os

from cdis_pipe_utils import df_util
from cdis_pipe_utils import pipe_util
from cdis_pipe_utils import time_util

def bamtofastq(uuid, bam_path, engine, logger):
    step_dir = os.getcwd()
    fastq_dir = os.path.join(step_dir, 'fastq')
    logger.info('fastq_dir is: %s' % fastq_dir)
    if pipe_util.already_step(fastq_dir, 'fastq', logger):
        logger.info('already completed step `bamtofastq` of: %s' % bam_path)
    else:
        logger.info('running step `bamtofastq` of %s: ' % bam_path)
        os.makedirs(fastq_dir, exist_ok=True)
        tempfq = os.path.join(fastq_dir, 'tempfq')
        cmd = ['bamtofastq', 'filename=' + bam_path, 'outputdir=' + fastq_dir, 'tryoq=1', 'collate=1', 'outputperreadgroup=1', 'T=' + tempfq, 'gz=1', 'level=1', 'outputperreadgroupsuffixF=_1.fq.gz', 'outputperreadgroupsuffixF2=_2.fq.gz', 'outputperreadgroupsuffixO=_o1.fq.gz', 'outputperreadgroupsuffixO2=_o2.fq.gz', 'outputperreadgroupsuffixS=_s.fq.gz', 'exclude=QCFAIL,SECONDARY,SUPPLEMENTARY']
        output = pipe_util.do_command(cmd, logger)
        df = time_util.store_time(uuid, cmd, output, logger)
        df['bam_path'] = bam_path
        unique_key_dict = {'uuid': uuid, 'bam_path': bam_path}
        table_name = 'time_mem_biobambam_bamtofastq'
        df_util.save_df_to_sqlalchemy(df, unique_key_dict, table_name, engine, logger)
        pipe_util.create_already_step(fastq_dir, 'fastq', logger)
        logger.info('completed running step `bamtofastq` of: %s' % bam_path)
    return
