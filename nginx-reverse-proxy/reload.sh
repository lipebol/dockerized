while true; do 
  sleep 10s; 
  nginx -s reload;
done &
exec nginx -g 'daemon off;'