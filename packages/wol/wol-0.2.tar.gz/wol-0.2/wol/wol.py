import requests
import sys
import argparse
import wolframalpha as wa
import os

def wol_cli():
	# wapp_id should be in your environment variable
	app_id = os.environ['wapp_id']
	client = wa.Client(app_id)
	res = client.query(sys.argv[1])
	print res.pods[0].text

if __name__ == '__main__':
	wol_cli()