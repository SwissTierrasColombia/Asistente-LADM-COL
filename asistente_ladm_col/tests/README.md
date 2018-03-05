## Testing

Unit tests are automatically executed after every commit made to the repository. Results are available for:

- Linux: https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL
- Windows: http://portal.proadmintierra.info:18000/

To run the tests locally you need to have *docker* and *docker-compose* installed. We suggest to:
- Download *docker* from the [official site](https://www.docker.com/community-edition#/download). For instance, for Ubuntu / Linux_Mint follow the steps in [Install using the convenience script](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-using-the-convenience-script).
- Install *docker-compose* using the [binaries](https://github.com/docker/compose/releases/tag/1.18.0).

The command to execute unit tests is:
```sh
docker-compose run --rm qgis
```

Important to execute in root of the repository!!!

If you need to recreate docker image, you can use:
```sh
docker-compose build
```
