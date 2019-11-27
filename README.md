# full-text-search
### Run services
```
docker-compose up
```
### Index building option
To avoid index rebuilding every time you start the services, change `COMMAND`
option in `.env` from `build` to `start`.
