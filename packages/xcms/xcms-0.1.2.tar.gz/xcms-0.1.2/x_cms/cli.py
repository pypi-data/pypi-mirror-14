import click


@click.command()
@click.option('--template-protein',
              help='template protein file path, in PDB format')
@click.option('--query-protein', help='query protein file path, in PDB format')
@click.option('--query-ligand', help='query ligand file path, in SDF format')
@click.option('--template-ligand',
              help='template ligand file path, in SDF format')
def main(template_protein, query_protein, template_ligand, query_ligand):
    """calculated extended contact mode score provided the query and template protein-ligand structures"""
    click.echo('{0}, {1}, {2}, {3}'.format(template_protein, template_ligand,
                                           query_protein, query_ligand))
