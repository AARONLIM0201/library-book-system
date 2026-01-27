docker build -t library-system-repo .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 026527021140.dkr.ecr.us-east-1.amazonaws.com
docker tag library-system-repo:latest 026527021140.dkr.ecr.us-east-1.amazonaws.com/library-system-repo:latest
docker push 026527021140.dkr.ecr.us-east-1.amazonaws.com/library-system-repo:latest
aws ecs update-service --cluster library-system-cluster --service library-system-service --force-new-deployment
