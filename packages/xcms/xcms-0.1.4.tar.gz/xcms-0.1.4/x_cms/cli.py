import click
import run_xcms


@click.command()
@click.option('--template-protein',
              type=click.Path(exists=True),
              help='template protein file path, in PDB format')
@click.option('--query-protein',
              type=click.Path(exists=True),
              help='query protein file path, in PDB format')
@click.option('--query-ligand',
              type=click.Path(exists=True),
              help='query ligand file path, in SDF format')
@click.option('--template-ligand',
              type=click.Path(exists=True),
              help='template ligand file path, in SDF format')
def main(template_protein, query_protein, template_ligand, query_ligand):
    """calculated extended contact mode score provided the query and template protein-ligand structures"""
    run_xcms.checkEnv()
    task = run_xcms.BioLipReferencedSpearmanR(query_ligand, query_protein)
    result = task.calculateAgainstOneSystem(template_ligand, template_protein)
    click.echo("XCMS: %.3f\np-value: %.3f" %
               (result['spearmanr'], result['pval']))
