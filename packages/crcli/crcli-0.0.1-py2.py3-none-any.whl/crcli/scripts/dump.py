import click
import json
import boto3
import gzip

client = boto3.client('dynamodb')

@click.command(short_help="Download a database into a gzipped file")
@click.argument('table', default='-', required=True)
@click.argument('filepath', default='dump.gz', required=False)
@click.pass_context
def dump(ctx, table, filepath):
    """This command dumps the contents of a dynamodb table into a gzipped file.

    To get the dump of the game-test table, do:

        $ cr dump 'game-test' ./path/to/dump.gz

    To get the dump of the pad-test table, do:

        $ cr dump 'pad-test' ./path/to/dump.gz
    """

    items = []

    response = client.scan(TableName=table)
    items += response.get('Items')

    while response.has_key('LastEvaluatedKey'):
        response = client.scan(TableName=table, ExclusiveStartKey=response.get('LastEvaluatedKey'))
        items += response.get('Items')

    itemstring = json.dumps(items)
    
    with gzip.open(filepath, 'wb') as f_out:
        f_out.write(itemstring)
        f_out.close()
