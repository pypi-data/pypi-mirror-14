#!/usr/bin/python
#
# Copyright (c) 2016 Mikkel Schubert <MSchubert@snm.ku.dk>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import logging
import os
import time

import paleomix
import paleomix.yaml
import paleomix.logger

import paleomix.common.fileutils as fileutils

from paleomix.common.console import \
    print_err, \
    print_warn

from paleomix.pipeline import \
    Pypeline

from paleomix.nodes.samtools import \
    BAMIndexNode

from paleomix.nodes.raxml import \
    RAxMLRapidBSNode

import paleomix.tools.bam_pipeline.mkfile as bam_mkfile

import paleomix.tools.zonkey.config as zonkey_config
import paleomix.tools.zonkey.parts.mitochondria as mitochondria
import paleomix.tools.zonkey.parts.nuclear as nuclear
import paleomix.tools.zonkey.parts.report as report
import paleomix.tools.zonkey.parts.summary as summary
import paleomix.tools.zonkey.parts.common as common_nodes


def run_pipeline(config, nodes, msg):
    pipeline = Pypeline(config)
    pipeline.add_nodes(nodes)

    logfile_template = time.strftime("zonkey_pipeline.%Y%m%d_%H%M%S_%%02i.log")
    paleomix.logger.initialize(config, logfile_template)

    logger = logging.getLogger(__name__)
    logger.info(msg)

    if config.list_executables:
        pipeline.print_required_executables()
        return True
    elif config.list_output_files:
        pipeline.print_output_files()
        return True
    elif config.dot_file:
        logger.info("Writing dependency graph to %r ...", config.dot_file)
        return pipeline.to_dot(config.dot_file)

    return pipeline.run(max_threads=config.max_threads,
                        progress_ui=config.progress_ui,
                        dry_run=config.dry_run)


def build_plink_nodes(config, data, root, bamfile, dependencies=()):
    plink = {"root": os.path.join(root, 'plink')}

    ped_node = nuclear.BuildTPEDFilesNode(output_root=plink["root"],
                                          table=config.tablefile,
                                          downsample=config.downsample_to,
                                          bamfile=bamfile,
                                          dependencies=dependencies)

    for postfix in ('incl_ts', 'excl_ts'):
        parameters = {
            "output_prefix": os.path.join(plink["root"], postfix),
            "tfam": os.path.join(plink["root"], "common.tfam"),
            "tped": os.path.join(plink["root"], postfix + ".tped"),
            "plink_parameters": config.database.settings["Plink"],
            "dependencies": (ped_node,),
        }

        if config.indep:
            parameters["indep_filter"] = config.indep
            parameters["indep_parameters"] = config.indep_params

            bed_node = nuclear.BuildFilteredBEDFilesNode(**parameters)
        else:
            bed_node = nuclear.BuildBEDFilesNode(**parameters)

        plink[postfix] = bed_node

    return plink


def build_admixture_nodes(config, data, root, plink):
    nodes = []
    for postfix in ('incl_ts', 'excl_ts'):
        bed_node = plink[postfix]

        admix_root = os.path.join(root, "admixture")
        report_root = os.path.join(root, "figures", "admixture")
        for k_groups in (2, 3):
            replicates = []

            input_file = os.path.join(plink["root"], postfix + ".bed")
            for replicate in xrange(config.admixture_replicates):
                output_root = os.path.join(admix_root, "%02i" % (replicate,))

                node = nuclear.AdmixtureNode(input_file=input_file,
                                             output_root=output_root,
                                             k_groups=k_groups,
                                             samples=data.samples,
                                             dependencies=(bed_node,))

                replicates.append(node)

            node = nuclear.SelectBestAdmixtureNode(replicates=replicates,
                                                   output_root=admix_root)

            if config.admixture_only:
                nodes.append(node)
            else:
                samples = os.path.join(root, "figures", "samples.txt")
                plot = nuclear.AdmixturePlotNode(input_file=os.path.join(admix_root, "%s.%i.Q" % (postfix, k_groups)),
                                                 output_prefix=os.path.join(report_root, "%s_k%i" % (postfix, k_groups)),
                                                 samples=samples,
                                                 order=data.sample_order,
                                                 dependencies=node)

                nodes.append(plot)

    return nodes


def build_treemix_nodes(config, data, root, plink):
    tmix_root = os.path.join(root, 'treemix')

    nodes = []
    for postfix in ('incl_ts', 'excl_ts'):
        plink_prefix = os.path.join(plink["root"], postfix)
        plink_nodes = plink[postfix]

        freq_node = nuclear.BuildFreqFilesNode(output_prefix=plink_prefix,
                                               input_prefix=os.path.join(plink["root"], postfix),
                                               tfam=os.path.join(plink["root"], "common.tfam"),
                                               parameters=config.database.settings["Plink"],
                                               dependencies=plink_nodes)

        tmix_prefix = os.path.join(tmix_root, postfix)
        tmix_file_node = nuclear.FreqToTreemixNode(input_file=plink_prefix + ".frq.strat.gz",
                                                   output_file=tmix_prefix + ".gz",
                                                   dependencies=(freq_node,))

        k_snps = config.treemix_k
        if k_snps is None:
            k_snps = ('n_sites_%s' % (postfix,),
                      os.path.join(plink["root"], "common.summary"))

        for n_migrations in (0, 1):
            n_prefix = "%s.%i" % (tmix_prefix, n_migrations)

            tmix_node = nuclear.TreemixNode(data=data,
                                            input_file=tmix_prefix + ".gz",
                                            output_prefix=n_prefix,
                                            m=n_migrations,
                                            k=k_snps,
                                            outgroup=config.treemix_outgroup,
                                            dependencies=(tmix_file_node,))

            samples = os.path.join(root, "figures", "samples.txt")
            output_prefix = os.path.join(root, "figures", "treemix", "%s_%i" % (postfix, n_migrations))
            plot_node = nuclear.PlotTreemixNode(samples=samples,
                                                prefix=n_prefix,
                                                output_prefix=output_prefix,
                                                dependencies=(tmix_node,))

            nodes.append(plot_node)

    return nodes


def build_pca_nodes(config, data, root, plink):
    pca_root = os.path.join(root, 'pca')

    nodes = []
    for postfix in ('incl_ts', 'excl_ts'):
        plink_prefix = os.path.join(plink["root"], postfix)
        plink_nodes = plink[postfix]

        pca_prefix = os.path.join(pca_root, postfix)
        pca_node = nuclear.SmartPCANode(input_prefix=plink_prefix,
                                        output_prefix=pca_prefix,
                                        nchroms=data.settings["NChroms"],
                                        dependencies=plink_nodes)

        samples = os.path.join(root, "figures", "samples.txt")
        pca_plots = os.path.join(root, "figures", "pca", postfix)
        pca_plot_node = nuclear.PlotPCANode(samples=samples,
                                            prefix=pca_prefix,
                                            output_prefix=pca_plots,
                                            dependencies=pca_node)

        nodes.append(pca_plot_node)

    return nodes


def build_coverage_nodes(data, root, nuc_bam, dependencies=()):
    output_prefix = os.path.join(root, 'figures', 'coverage', 'coverage')

    return nuclear.PlotCoverageNode(contigs=data.contigs,
                                    input_file=nuc_bam,
                                    output_prefix=output_prefix,
                                    dependencies=dependencies),


def build_mito_nodes(config, root, bamfile, dependencies=()):
    if config.database.mitochondria is None:
        print_warn("WARNING: Zonkey database %r does not contain "
                   "mitochondrial  sequences; cannot analyze MT BAM %r!\n"
                   % (config.tablefile, bamfile))
        return ()

    samples = os.path.join(root, "figures", "samples.txt")

    index = BAMIndexNode(infile=bamfile, dependencies=dependencies)

    mt_prefix = os.path.join(root, "mitochondria", "sequences")
    alignment = mitochondria.MitoConsensusNode(database=config.tablefile,
                                               bamfile=bamfile,
                                               output_prefix=mt_prefix,
                                               dependencies=(index,))

    raxml_template = os.path.join(root, "mitochondria", "raxml_%s")
    phylo = RAxMLRapidBSNode.customize(input_alignment=mt_prefix + ".phy",
                                       output_template=raxml_template,
                                       dependencies=(alignment,))

    phylo.command.set_option("-N", 100)
    phylo.command.set_option("-m", "GTRGAMMA")
    phylo = phylo.build_node()

    output_prefix = os.path.join(root, "figures", "mitochondria", "mito_phylo")
    trees = mitochondria.DrawPhylogenyNode(samples=samples,
                                           treefile=raxml_template % ("bestTree",),
                                           bootstraps=raxml_template % ("bootstrap",),
                                           output_prefix=output_prefix,
                                           dependencies=(phylo,))

    return (trees,)


def build_pipeline(config, root, nuc_bam, mito_bam):
    nodes = []
    sample_tbl = os.path.join(root, "figures", "samples.txt")
    samples = common_nodes.WriteSampleList(config=config,
                                           output_file=sample_tbl)

    if nuc_bam is not None:
        # When not sampling, BuildTPED relies on indexed access to ease
        # processing of one chromosome at a time. The index is further required
        # for idxstats used by the PlotCoverageNode.
        index = BAMIndexNode(infile=nuc_bam)

        plink = build_plink_nodes(config, config.database, root, nuc_bam,
                                  (samples, index))

        nodes.extend(build_admixture_nodes(config, config.database, root,
                                           plink))

        if not config.admixture_only:
            nodes.extend(build_coverage_nodes(config.database,
                                              root, nuc_bam, (index,)))
            nodes.extend(build_pca_nodes(config, config.database,
                                         root, plink))
            nodes.extend(build_treemix_nodes(config, config.database,
                                             root, plink))

    if mito_bam is not None and not config.admixture_only:
        nodes.extend(build_mito_nodes(config, root, mito_bam, samples))

    if not config.admixture_only:
        nodes.append(report.ReportNode(config, root, nuc_bam, mito_bam,
                                       dependencies=nodes))

    return nodes


def run_admix_pipeline(config):
    config.temp_root = os.path.join(config.destination, "temp")
    if not config.dry_run:
        fileutils.make_dirs(config.temp_root)

    nodes = []
    for sample in config.samples.itervalues():
        root = sample["Root"]
        nuc_bam = sample["Files"].get("Nuc")
        mito_bam = sample["Files"].get("Mito")

        nodes.extend(build_pipeline(config, root, nuc_bam, mito_bam))

    if config.multisample and not config.admixture_only:
        nodes = [summary.SummaryNode(config, nodes)]

    if not run_pipeline(config, nodes, "\nRunning Zonkey ..."):
        return 1


def setup_mito_mapping(config):
    if os.path.exists(config.destination):
        # A bit strict, but avoid accidential overwrites
        print_err("ERROR: Destination folder already exists, "
                  "cannot proceed:\n  - %r" % (config.destination,))
        return 1

    genomes_root = os.path.join(config.destination, "genomes")
    fileutils.make_dirs(genomes_root)

    mkfile_fpath = os.path.join(config.destination, "makefile.yaml")
    with open(mkfile_fpath, "w") as mkfile:
        mkfile.write(bam_mkfile.build_makefile(add_prefix_tmpl=False,
                                               add_sample_tmpl=False))

        mkfile.write("\n\nPrefixes:\n")

        for name, record in sorted(config.database.mitochondria.iteritems()):
            meta = (record.meta or "").upper()
            if "EXCLUDE" in meta:
                continue

            mkfile.write("  %s:\n" % (record.name,))
            mkfile.write("    Path: genomes/%s.fasta\n\n" % (record.name,))

            fasta_fpath = os.path.join(genomes_root,
                                       "%s.fasta" % (record.name,))

            with open(fasta_fpath, "w") as fasta_handle:
                fasta_handle.write(str(record))
                fasta_handle.write("\n")

        mkfile.write("\n")

    return 0


def main(argv):
    try:
        config = zonkey_config.parse_config(argv)
        if config is None:
            return 1
    except zonkey_config.ConfigError, error:
        print_err(error)
        return 1

    if config.command == "run":
        return run_admix_pipeline(config)
    elif config.command == "mito":
        return setup_mito_mapping(config)

    return 1
