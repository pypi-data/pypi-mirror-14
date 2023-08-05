import click
import hmac
import hashlib
import requests
import json

from sblu import CONFIG

URL_SCHEME = "http"
API_ENDPOINT = "/api.php"
CP_CONFIG = CONFIG['cluspro']
FORM_KEYS = [
    'username', 'receptor', 'ligand', 'jobname', 'coeffs', 'rotations',
    'antibodymode', 'othersmode'
]
for f in ('pdb', '_chains', '_attraction', '_dssp'):
    FORM_KEYS.append("rec" + f)
    FORM_KEYS.append("lig" + f)


def make_sig(form, secret):
    sig = ""
    for k in sorted(form.keys()):
        if form[k] is not None:
            sig += "{}{}".format(k, form[k])
    return hmac.new(
        secret.encode('utf-8'), sig.encode('utf-8'), hashlib.md5).hexdigest()


@click.command('submit', short_help="Submit a job to ClusPro.")
@click.option("--username", default=CP_CONFIG['username'])
@click.option("--secret", default=CP_CONFIG['api_secret'])
@click.option("--server", default=CP_CONFIG['server'])
@click.option("--coeffs", type=click.Path(exists=True), default=None)
@click.option("--rotations", type=click.Path(exists=True), default=None)
@click.option("-j", "--jobname", required=True)
@click.option("-a", "--antibodymode", is_flag=True, default=False)
@click.option("-o", "--othersmode", is_flag=True, default=False)
@click.option("--receptor", type=click.Path(exists=True))
@click.option("--ligand", type=click.Path(exists=True))
@click.option("--recpdb")
@click.option("--ligpdb")
@click.option("--rec-chains")
@click.option("--lig-chains")
@click.option("--rec-attraction")
@click.option("--lig-attraction")
@click.option("--rec-dssp", is_flag=True, default=False)
@click.option("--lig-dssp", is_flag=True, default=False)
def cli(ctx,
        username, secret, server, coeffs, rotations, jobname, antibodymode,
        othersmode, receptor, recpdb, rec_chains, rec_attraction, rec_dssp,
        ligand, ligpdb, lig_chains, lig_attraction, lig_dssp):
    form = {
        k: v
        for k, v in list(locals().items()) if k in FORM_KEYS and v is not None
    }
    print(form)

    form['sig'] = make_sig(form, secret)

    files = {}
    if form.get("receptor") is not None:
        files['rec'] = form['receptor'].open('rb')
    if form.get("ligand") is not None:
        files['lig'] = form['ligand'].open('rb')

    api_address = "{0}://{1}{2}".format(URL_SCHEME, server, API_ENDPOINT)

    try:
        r = requests.post(api_address, data=form, files=files)
        result = json.loads(r.text)
        if result['status'] == 'success':
            print((result['id']))
        else:
            print((result['errors']))
    except Exception as e:
        print(("Error submitting job: {}".format(e)))
