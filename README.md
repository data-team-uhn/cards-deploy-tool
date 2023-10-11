# CARDS Deploy Tool

Deploys a CARDS project Docker container as well as its dependency
containers as a Docker Compose environment

## Usage

```bash
python3 generate_compose_yaml.py --oak_filesystem --cards_docker_image ghcr.io/data-team-uhn/cards4sparc
docker-compose build
docker-compose up -d
```
