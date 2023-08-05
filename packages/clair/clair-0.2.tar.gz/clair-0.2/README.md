# Clair

Clair is an open source project for the static analysis of vulnerabilities in appc and docker containers (https://github.com/coreos/clair).

This Python package provides methods to analyse a local Docker image and injects image layers to a Clair server.


# Example


    cfg = {
        'clair.host': 'http://127.0.0.1:6060',
        'docker.connect': 'tcp://127.0.0.1:2375'
    }
    log = logging.getLogger(__name__)


    test = Clair(cfg)
    layers = test.analyse('docker-registry.genouest.org/osallou/testgit')

    layer_ids = []
    for layer in layers:
        layer_ids.append(layer['id'])
    vulnerabilities = test.get_layers_vulnerabilities(layer_ids)

    log.warn(str(vulnerabilities))
