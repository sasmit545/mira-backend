from mira_sdk import MiraClient, Flow
from mira_sdk.exceptions import FlowError
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("API_KEY")

# Initialize the client
client = MiraClient(config={"API_KEY": api_key})

# Define the flows to be deployed
elemental_flows = [
    {
        "name": "Hero Image Generator",
        "file": "flow-hero.yaml"
    },
    {
        "name": "Product Showcase Generator",
        "file": "flow-prod.yaml"
    },
    {
        "name": "Promotional Banner Generator",
        "file": "flow-banner.yaml"
    },
    {
        "name":"format check",
        "file": "flow-html.yaml"


    },
    {
        "name": "content",
        "file": "flow-content.yaml"
    }

]

# Deploy each flow
for flow_config in elemental_flows:
    try:
        print(f"\nDeploying {flow_config['name']}...")
        flow = Flow(source=flow_config['file'])
        client.flow.deploy(flow)
        print(f"✓ {flow_config['name']} deployed successfully!")
        
    except FlowError as e:
        print(f"✗ Error deploying {flow_config['name']}: {str(e)}")
    except Exception as e:
        print(f"✗ Unexpected error deploying {flow_config['name']}: {str(e)}")