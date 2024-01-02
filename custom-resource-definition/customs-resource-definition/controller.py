import json
import yaml
from kubernetes import client, config, watch
import os
from pprint import pprint



DOMAIN = "crds.cloudyuga.guru"
indian = ['maruti', 'tata', 'ashokleyland', 'swarazmazda']
foreign = ['landrover', 'laferrari', 'lamborghini', 'pagani', 'bmw', 'porsche', 'merc']

def classify_car(crds, obj):
    metadata = obj.get("metadata")
    if not metadata:
        print("No metadata in object, skipping: %s" % json.dumps(obj, indent=1))
        return
    name = metadata.get("name")
    namespace = metadata.get("namespace")
    obj["spec"]["review"] = True
    brand = obj["spec"]["brand"]
    print(brand)

    if brand in indian:
        obj["spec"]["comment"] = "this is an indian brand"
    elif brand in foreign:
        obj["spec"]["comment"] = "this is foreign brand"
    else:
        obj["spec"]["comment"] = "No idea about it"

    print("Updating: %s" % name)
    crds.replace_namespaced_custom_object(DOMAIN, "v1", namespace, "cars", name, obj)



if __name__ == "__main__":
    if 'KUBERNETES_PORT' in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()
    configuration = client.Configuration()
    configuration.assert_hostname = False 
    api_client = client.AppsV1Api(configuration=configuration)
    v1 = client.AppsV1Api(api_client)
    current_crds = [x['spec']['names']['kind'].lower() for x in v1.list_custom_resource_definition().to_dict()['items']]
    print("=== Crds ===")
    for crd in current_crds:
        print(crd)
        print(dir(crd))
    print("============")
    if 'car' not in current_crds:
        print("car not found, please apply crd first")
        print("Creating guitar definition")
        # with open(definition) as data:
        #     body = yaml.load(data)
        # v1.create_custom_resource_definition(body)
    crds = client.CustomObjectsApi(api_client)

    print("Waiting for new cars ...")
    resource_version = ''
    while True:
        stream = watch.Watch().stream(crds.list_cluster_custom_object, DOMAIN, "v1", "cars", resource_version=resource_version)
        for event in stream:
            obj = event["object"]
            operation = event['type']
            spec = obj.get("spec")
            if not spec:
                continue
            metadata = obj.get("metadata")
            resource_version = metadata['resourceVersion']
            name = metadata['name']
            print("Handling %s on %s" % (operation, name))
            done = spec.get("review", False)
            if done:
                continue
            classify_car(crds, obj)

