# CARDS Deploy Tool

Deploys a CARDS project Docker container as well as its dependency
containers as a Docker Compose environment.

## Usage

```bash
# Generate a docker-compose file for the specified project
# Run this to find out more about the supported configurations:
python3 generate_compose_yaml.py --help
# For a standalone cards4sparc instance using the latest published version, run:
python3 generate_compose_yaml.py --oak_filesystem --cards_docker_image ghcr.io/data-team-uhn/cards4sparc
# Start the containers:
docker-compose build
docker-compose up -d
# Stop the containers and cleanup:
docker-compose down
docker-compose rm -vf
docker volume prune -f
./cleanup.sh
```
