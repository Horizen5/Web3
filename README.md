# aiOS CLI WSL 管理脚本

这是一个用于在WSL环境中安装、配置和管理aiOS CLI的脚本，基于 [aiOS CLI](https://github.com/hyperspaceai/aios-cli) 项目。

## 功能特性

- 🚀 一键安装 aiOS CLI
- 🖥️ 完整的节点部署（包含私钥导入和网络连接）
- 📊 积分查看和监控
- 📝 日志查看和监控
- 🔧 系统信息显示
- 🤖 模型管理和推理
- 🛡️ 自动错误检测和重启
- 🎨 彩色界面和用户友好菜单

## 安装和使用

### 1. 下载脚本

```bash
wget -O hyper.sh https://raw.githubusercontent.com/Horizen5/Web3/refs/heads/main/hyper.sh && sed -i 's/\r$//' hyper.sh && chmod +x hyper.sh && ./hyper.sh
```

### 2. 运行脚本

#### 交互式菜单模式（推荐）
```bash
./hyper.sh
```

#### 命令行模式
```bash
# 安装 aiOS CLI
./hyper.sh install

# 部署完整节点
./hyper.sh deploy

# 查看积分
./hyper.sh points

# 查看日志
./hyper.sh logs

# 启动守护进程
./hyper.sh start

# 停止守护进程
./hyper.sh stop
```

## 主要命令说明

### 基础命令
- `install` - 安装 aiOS CLI
- `start` - 启动守护进程
- `status` - 检查守护进程状态
- `stop` - 停止守护进程
- `system` - 显示系统信息

### 模型管理
- `models` - 显示可用模型
- `install-model` - 安装示例模型
- `local-models` - 显示本地模型
- `infer` - 运行示例推理

### 节点部署
- `deploy` - 部署完整节点（包含私钥导入和网络连接）
- `points` - 查看积分
- `logs` - 查看日志
- `whoami` - 查看私钥信息

### 监控功能
- `log-monitor` - 启动日志监控
- `points-monitor` - 启动积分监控

### 一键安装
- `full-setup` - 完整安装和配置
- `help` - 显示帮助信息

## 快速开始

1. **首次使用**：
   ```bash
   ./hyper.sh
   # 选择 "16. 完整安装和配置"
   ```

2. **部署节点**：
   ```bash
   ./hyper.sh deploy
   # 按提示输入私钥和选择等级
   ```

3. **查看状态**：
   ```bash
   ./hyper.sh points  # 查看积分
   ./hyper.sh logs    # 查看日志
   ```

## 监控功能

### 日志监控
自动检测连接问题并重启服务：
- 认证失败
- 连接断开
- 内部服务器错误
- 实例冲突

### 积分监控
每2小时检查一次积分变化，如果积分没有增加则自动重启服务。

## 文件位置

- 脚本文件：`~/hyper.sh`
- 日志文件：`~/aios-cli.log`
- 监控日志：`~/monitor.log`
- 积分监控日志：`~/points_monitor.log`

## 系统要求

- WSL (Windows Subsystem for Linux)
- Ubuntu/Debian 系统
- 网络连接
- 足够的磁盘空间（用于模型下载）

## 故障排除

### 常见问题

1. **aios-cli 命令未找到**
   ```bash
   source ~/.bashrc
   # 或重新运行安装
   ./hyper.sh install
   ```

2. **权限问题**
   ```bash
   sudo chmod +x hyper.sh
   ```

3. **网络连接问题**
   - 检查网络连接
   - 尝试使用VPN
   - 检查防火墙设置

### 日志查看

```bash
# 查看主日志
./hyper.sh logs

# 查看监控日志
tail -f ~/monitor.log

# 查看积分监控日志
tail -f ~/points_monitor.log
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目采用 MIT 许可证。

## 免责声明

- 本脚本仅供学习和研究使用
- 请确保遵守相关法律法规
- 使用本脚本产生的任何后果由用户自行承担

---

**脚本由大赌社区哈哈哈哈编写，免费开源，请勿相信收费** 
