docker build -t snapsavor_backend:2.0 .
docker run -p 5000:5000 snapsavor_backend:2.0
docker run -it --entrypoint /bin/bash snapsavor_backend:2.0

flyctl status -a snap-backend
flyctl deploy -a snap-backend
flyctl logs -a snap-backend
