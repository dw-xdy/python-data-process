import random
from datetime import datetime, timedelta

# 生成日志
users = ['admin', 'root', 'john', 'alice', 'deploy', 'ubuntu', 'matt', 'guest', 'test', 'hacker']
ip_pool = ['188.166.237', '192.168.1', '10.0.0', '172.16.0', '203.0.113', '198.51.100']
logs = []

for i in range(100000):
    user = random.choice(users)
    ip_base = random.choice(ip_pool)
    ip = f"{ip_base}.{random.randint(1, 254)}"
    total_attempts = random.randint(1, 50)
    failed = random.randint(0, total_attempts)
    success = total_attempts - failed
    success_rate = (success / total_attempts * 100) if total_attempts > 0 else 0
    
    # 随机时间戳
    start_date = datetime(2024, 11, 1)
    end_date = datetime(2024, 11, 30)
    random_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
    timestamp = random_date.strftime("%b %d %H:%M:%S")
    
    log_line = f"{timestamp} thesquareplanet.com sshd[{random.randint(10000, 99999)}]: Last login summary for {user} from {ip}: Total attempts={total_attempts}, Success={success}, Failed={failed}, Success rate={success_rate:.1f}%"
    logs.append(log_line)

# 保存到文件
with open('ssh_login_summary.txt', 'w') as f:
    for log in logs:
        f.write(log + '\n')

print(f"已生成 {len(logs)} 条日志到 ssh_login_summary.txt")
