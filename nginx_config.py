import paramiko

host = "47.106.185.91"
user = "root"
password = "@Qq123456"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, 22, user, password, timeout=15)

nginx_conf = """server {
    listen 80;
    server_name depaido-xctx.store www.depaido-xctx.store;
    index index.html index.htm;
    root /www/wwwroot/depaido-xctx.store/;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \\.(gif|jpg|jpeg|png|bmp|swf)$ {
        expires 30d;
    }

    location ~* \\.(js|css)?$ {
        expires 12h;
    }

    access_log /www/wwwlogs/depaido-xctx.store.log;
    error_log /www/wwwlogs/depaido-xctx.store.error.log;
}"""

# Create domain directory and copy files
ssh.exec_command("mkdir -p /www/wwwroot/depaido-xctx.store")
ssh.exec_command("cp /www/wwwroot/index.html /www/wwwroot/depaido-xctx.store/index.html")
ssh.exec_command("cp -r /www/wwwroot/Pitch /www/wwwroot/depaido-xctx.store/")

# Write nginx config
transport = ssh.get_transport()
channel = transport.open_session()
channel.exec_command(f"cat > /www/server/panel/vhost/nginx/depaido-xctx.store.conf")
channel.send(nginx_conf.encode())
channel.shutdown_write()
output = channel.recv(1024).decode()
print("Config created")

# Test nginx
stdin, stdout, stderr = ssh.exec_command("nginx -t 2>&1")
print("Nginx test:", stdout.read().decode().strip())

# Reload
ssh.exec_command("nginx -s reload")
print("Nginx reloaded!")

ssh.close()
