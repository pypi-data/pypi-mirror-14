import os
import sys
import logging
import tempfile
import shutil
import tarfile
import json

from docker import Client
import requests

class Clair(object):

    def __init__(self, cfg):
        '''
        Cfg is a dict:

            cfg = {
                'clair.host': 'http://localhost:6060',
                'docker.connect': 'tcp://127.0.0.1:2375' or None for socks.

                }
        '''
        self.cfg = cfg
        if self.cfg['docker.connect']:
            self.docker_cli = Client(
                                    base_url=self.cfg['docker.connect'],
                                    timeout=1800)
        else:
            self.docker_cli = Client(timeout=1800)

    def analyse_layer(self, layer):
        '''
        POST http://localhost:6060/v1/layers HTTP/1.1

            {
              "Layer": {
                "Name": "523ef1d23f222195488575f52a39c729c76a8c5630c9a194139cb246fb212da6",
                "Path": "/mnt/layers/523ef1d23f222195488575f52a39c729c76a8c5630c9a194139cb246fb212da6/layer.tar",
                "ParentName": "140f9bdfeb9784cf8730e9dab5dd12fbd704151cf555ac8cae650451794e5ac2",
                "Format": "Docker"
              }
            }
        '''
        clair_layer = {
            'Layer': {
                'Name': layer['id'],
                'Path': layer['path'],
                'ParentName': layer['parent'],
                'Format': 'Docker'
            }
        }
        r = requests.post(self.cfg['clair.host']+'/v1/layers', data = json.dumps(clair_layer))
        if r.status_code != 201:
            logging.error(layer['image'] + ':Failed to analyse layer ' + layer['name'])

    def analyse(self, image):
        (image_tar, tmp_path) = tempfile.mkstemp(suffix="-bioshadock-image")
        docker_image = self.docker_cli.get_image(image)
        file_tar = open(tmp_path, 'w')
        file_tar.write(docker_image.data)
        file_tar.close()
        logging.debug('Image '+image+' tar: '+tmp_path)

        tmp_dir = tempfile.mkdtemp(suffix='-bioshadock-image-archive')

        image_archive = tarfile.TarFile(name=tmp_path)
        image_archive.extractall(path=tmp_dir)
        image_archive.close()
        logging.debug('Image '+image+' tar: '+tmp_dir)

        layers = []
        with open(os.path.join(tmp_dir, 'manifest.json'), 'r') as content_file:
            content = content_file.read()
            manifest = json.loads(content)
            logging.debug(str(manifest))
            parent_layer = ""
            for layer in manifest[0]['Layers']:
                layers.append({'id': layer.replace('/layer.tar', ''),
                               'path': os.path.join(tmp_dir, layer),
                               'parent': parent_layer,
                               'image': image
                })
                parent_layer = layer.replace('/layer.tar', '')

        for layer in layers:
            self.analyse_layer(layer)

        os.remove(tmp_path)
        shutil.rmtree(tmp_dir)
        return layers


    def get_layers_vulnerabilities(self, layer_ids):
        vulnerabilities = []
        for layer_id in layer_ids:
            layer_vulnerabilities = self.get_layer_vulnerabilities(layer_id)
            if layer_vulnerabilities is not None:
                vulnerabilities.append(layer_vulnerabilities)
        return vulnerabilities

    def get_layer_vulnerabilities(self, layer_id):
        '''
        GET http://localhost:6060/v1/layers/17675ec01494d651e1ccf81dc9cf63959ebfeed4f978fddb1666b6ead008ed52?features&vulnerabilities
        '''
        r = requests.get(self.cfg['clair.host']+'/v1/layers/'+layer_id+'?features&vulnerabilities')
        if r.status_code != 200:
            logging.error('Could not get info on layer '+layer_id)
            return None
        return r.json()
