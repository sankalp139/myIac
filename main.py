
import yaml
import json
import os
import sys
from registry import RESOURCE_REGISTRY

def load_state():
    if os.path.exists("state.json"):
        with open("state.json") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open("state.json", "w") as f:
        json.dump(state, f, indent=2)

def apply(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)

    state = load_state()

    for resource in config['resources']:
        resource_type = resource['type']
        resource_name = resource['name']
        properties = resource['properties']

        if resource_name in state:
            print(f"Resource {resource_name} already exists, skipping.")
            continue

        handler_class = RESOURCE_REGISTRY[resource_type]
        resource_obj = handler_class(resource_name, properties)
        resource_id = resource_obj.create()

        state[resource_name] = {
            "type": resource_type,
            "id": resource_id,
            "properties": properties
        }

    save_state(state)
    print("Apply complete.")

def destroy(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)

    state = load_state()

    for resource in config['resources']:
        resource_name = resource['name']
        if resource_name not in state:
            print(f"No record of {resource_name} in state. Skipping.")
            continue

        resource_type = resource['type']
        instance_id = state[resource_name]['id']
        properties = state[resource_name]['properties']

        handler_class = RESOURCE_REGISTRY[resource_type]
        resource_obj = handler_class(resource_name, properties)
        resource_obj.destroy(instance_id)

        print(f"Resource {resource_name} destroyed.")
        del state[resource_name]

    save_state(state)
    print("Destroy complete.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py [apply|destroy]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "apply":
        apply("infra.yaml")
    elif command == "destroy":
        destroy("infra.yaml")
    else:
        print(f"Unknown command: {command}")
