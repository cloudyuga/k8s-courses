while true; do
    curl -I http://go-app-example.app.svc.cluster.local/blue
    sleep 0.1
done