# Clair

Clair is an open source project for the static analysis of vulnerabilities in appc and docker containers (https://github.com/coreos/clair).

This Python package provides methods to analyse a local Docker image and injects image layers to a Clair server.

# License

All code is under Apache 2.0 or more.

    Copyright 2015 Olivier Sallou <olivier.sallou@irisa.fr>
    .
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    .
    http://www.apache.org/licenses/LICENSE-2.0
    .
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

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
