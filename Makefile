load-test-1:
	hey -n 1 -c 1 -m POST -T "application/json" -d '{"message":"asdf"}' http://localhost:8080/

load-test-100:
	hey -z 5s -c 100 -m POST -T "application/json" -d '{"message":"asdf"}' http://localhost:8080/

consumer-batch:
	cd consumer && python3 batching-graceful-shutdown.py

consumer-loop:
	cd consumer && python3 loop-graceful-shutdown.py

producer:
	docker rm -f redpanda-1	 || true
	docker run --name=redpanda-1 -d \
        -p 9092:9092 \
        docker.vectorized.io/vectorized/redpanda:latest \
        redpanda start \
        --overprovisioned \
        --smp 1  \
        --memory 1G \
        --reserve-memory 0M \
        --node-id 0 \
        --check=false
	sleep 2
	docker exec -it redpanda-1 rpk topic create twitch_chat -p 2 || true
	cd producer && go run .

