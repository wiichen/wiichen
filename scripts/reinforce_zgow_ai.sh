#!/bin/bash

# 日志文件
LOGFILE="/tmp/reinforce_zgow.log"
exec >> "$LOGFILE" 2>&1
echo "Script started at $(date)"

# 定义变量
PASSWORD="atc4@ST202404"
GROUP="cetc"

# 备份配置文件
backup_file() {
    local file="$1"
    if [ -f "$file" ]; then
        cp "$file" "${file}.bak"
        echo "Backup created for $file: ${file}.bak"
    else
        echo "File $file does not exist. Skipping backup."
    fi
}

# 配置密码策略
configure_password_policy() {
    echo "Configuring password policy..."
    backup_file /etc/pam.d/system-auth
    sed -i '0,/^password/s/^password/password    requisite     pam_cracklib.so minlen=8 lcredit=-1 ucredit=-1 ocredit=-1 dcredit=-1\npassword/' /etc/pam.d/system-auth
    echo "Password policy configured."
}

# 配置登录失败锁定策略
configure_login_lock() {
    echo "Configuring login failure lock policy..."
    sed -i '0,/^auth/s/^auth/auth    required     pam_tally2.so deny=10 unlock_time=300 even_deny_root root_unlock_time=300\nauth/' /etc/pam.d/system-auth
    echo "Login failure lock policy configured."
}

# 配置会话超时
configure_session_timeout() {
    echo "Configuring session timeout..."
    if ! grep -q "export TMOUT=1800" /etc/profile; then
        echo "export TMOUT=1800" >> /etc/profile
    fi
    echo "Session timeout configured."
}

# 配置审计规则
configure_audit_rules() {
    echo "Configuring audit rules..."
    echo "-w /etc/passwd -p rwxa" >> /etc/audit/rules.d/audit.rules
    echo "-w /etc/shadow -p rwxa" >> /etc/audit/rules.d/audit.rules
    echo "Audit rules configured."
}

# 配置日志轮转
configure_log_rotation() {
    echo "Configuring log rotation..."
    sed -i "0,/^rotate/s/rotate 4/rotate 30/" /etc/logrotate.conf
    echo "Log rotation configured."
}

# 配置用户密码
configure_user_password() {
    local user="$1"
    echo "Configuring password for user $user..."
    echo "$PASSWORD" | passwd --stdin "$user"
    echo "Password configured for user $user."
}

# 创建用户并配置密码
create_user() {
    local user="$1"
    echo "Creating user $user..."
    if ! id "$user" &>/dev/null; then
        useradd "$user" -g "$GROUP"
        configure_user_password "$user"
        echo "User $user created and configured."
    else
        echo "User $user already exists. Skipping creation."
    fi
}

# 配置远程登录限制
configure_remote_login() {
    echo "Configuring remote login restrictions..."
    echo "exec X :0 -nolisten tcp" > /home/atc/.xserverrc
    if ! grep -q "auth required pam_wheel.so use_uid group=wheel" /etc/pam.d/su; then
        echo "auth required pam_wheel.so use_uid group=wheel" >> /etc/pam.d/su
    fi
    usermod -aG wheel atc
    echo "Remote login restrictions configured."
}

# 配置 FTP 匿名登录
configure_ftp() {
    echo "Configuring FTP anonymous login..."
    sed -i 's/anonymous_enable=YES/anonymous_enable=NO/' /etc/vsftpd/vsftpd.conf
    echo "FTP anonymous login disabled."
}

# 配置系统日志
configure_syslog() {
    echo "Configuring syslog..."
    echo "*.*    @195.28.4.233" >> /etc/rsyslog.conf
    echo "auth.info    /var/log/authlog" >> /etc/rsyslog.conf
    echo "*.info;auth.none    /var/log/syslog" >> /etc/rsyslog.conf
    touch /var/log/authlog /var/log/syslog
    chmod 600 /var/log/authlog
    chmod 640 /var/log/syslog
    systemctl restart rsyslog
    echo "Syslog configuration updated."
}

# 配置 SNMP
configure_snmp() {
    echo "Configuring SNMP..."
    sed -i '/com2sec notConfigUser/d' /etc/snmp/snmpd.conf
    echo "com2sec notConfigUser  default Les_Public_r" >> /etc/snmp/snmpd.conf
    echo "SNMP configuration updated."
}

# 配置 SSH 安全
configure_ssh() {
    echo "Configuring SSH security..."
    backup_file /etc/ssh/sshd_config
    echo "Banner none" >> /etc/ssh/sshd_config
    echo "Protocol 2" >> /etc/ssh/sshd_config
    echo "PermitRootLogin no" >> /etc/ssh/sshd_config
    echo "AllowUsers *@192.28.4.*" >> /etc/ssh/sshd_config
    echo "AllowUsers *@193.28.4.*" >> /etc/ssh/sshd_config
    echo "AllowUsers *@195.28.4.*" >> /etc/ssh/sshd_config
    systemctl restart sshd
    if systemctl is-active sshd > /dev/null; then
        echo "SSH service restarted successfully."
    else
        echo "Failed to restart SSH service."
        exit 1
    fi
}

# 主函数
main() {
    configure_password_policy
    configure_login_lock
    configure_session_timeout
    configure_audit_rules
    configure_log_rotation
    configure_user_password root
    create_user LESaudit
    create_user LESsafe
    create_user LESadmin
    create_user LESremote
    configure_remote_login
    configure_ftp
    configure_syslog
    configure_snmp
    configure_ssh
    echo "Script completed at $(date)"
}

main
