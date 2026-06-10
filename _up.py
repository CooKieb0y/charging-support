import paramiko, os

host = "47.106.185.91"
user = "root"
password = "@Qq123456"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, 22, user, password, timeout=15)
sftp = ssh.open_sftp()

local_dir = r"D:\Xctx"
site_dirs = ["/www/wwwroot/47.106.185.91/", "/www/wwwroot/depaido-xctx.store/"]

for target_dir in site_dirs:
    print("Uploading to " + target_dir)
    ssh.exec_command("mkdir -p " + target_dir + "Pitch")
    
    # Upload key files
    for f in ["index.html", "logo.svg", "favicon.svg", "qrcode.png"]:
        local = os.path.join(local_dir, f)
        if os.path.exists(local):
            sftp.put(local, target_dir + f)
            print("  " + f + " ok")
    
    # Upload Pitch images
    for f in os.listdir(os.path.join(local_dir, "Pitch")):
        local = os.path.join(local_dir, "Pitch", f)
        if os.path.isfile(local) and os.path.getsize(local) < 30*1024*1024:
            try:
                sftp.put(local, target_dir + "Pitch/" + f)
            except:
                pass
    print("  Pitch/ ok")

sftp.close()

# Reload nginx
ssh.exec_command("nginx -s reload")

ssh.close()
print("\nDone! All files uploaded and nginx reloaded.")
