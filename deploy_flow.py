#!/usr/bin/env python

import ast
import argparse
from globus_automate_client import create_flows_client

# Parse input arguments
def parse_args():
    parser = argparse.ArgumentParser(description='''
        Deploy a flow for use with trigger examples.''')
    parser.add_argument('--defs', required=True,
        help='Name of file containing the flow and input schema definitions.')
    parser.add_argument('--title',
        default='Flow from Trigger Examples',
        help='Flow title. [default: "Flow from Trigger Examples"]')
    parser.add_argument('--flowid',
        help='Flow ID; used only when updating a flow definition')
    parser.set_defaults(verbose=True)
    
    return parser.parse_args()

 
def deploy_flow():

    args = parse_args()
    fc = create_flows_client()

    # Get flow and input schema definitions
    with open(args.defs, 'r') as f:
        # Not super safe, but OK for non-production use!
        flow_def = ast.literal_eval(f.read())  
    
    if args.flowid:
        # Assume we're updating an existing flow
        flow_id = args.flowid
        flow = fc.update_flow(
            flow_id=flow_id,
            flow_definition=flow_def['flow_definition'],
            title=args.title,
            input_schema=flow_def['input_schema']
        )
        print(f"Updated flow {flow_id}")

    else:
        # Deploy a new flow
        flow = fc.deploy_flow(
            flow_definition=flow_def['flow_definition'], 
            title=args.title,
            input_schema=flow_def['input_schema']
        )
        flow_id = flow['id']
        print(f"Deployed flow {flow_id}")
    
    return flow_id, flow['globus_auth_scope']

if __name__ == '__main__':
    deploy_flow()