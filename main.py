#!/bin/bash

# aiOS CLI WSL 安装和运行脚本
# 基于 https://github.com/hyperspaceai/aios-cli
# 改进版本，整合了更多实用功能

set -e

# 脚本保存路径
SCRIPT_PATH="$HOME/hyper.sh"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否为WSL环境
check_wsl() {
    if [[ ! -f /proc/version ]] || ! grep -q Microsoft /proc/version; then
        log_warning "这似乎不是WSL环境，但脚本仍将继续运行..."
    else
        log_info "检测到WSL环境"
    fi
}

# 检查并安装 screen
check_and_install_screen() {
    if ! command -v screen &> /dev/null; then
        log_info "screen 未安装，正在安装..."
        sudo apt update && sudo apt install -y screen
        log_success "screen 安装完成"
    else
        log_info "screen 已安装"
    fi
}

# 获取aios-cli路径
get_aios_path() {
    local aios_path=""
    
    # 检查多个可能的路径
    if command -v aios-cli &> /dev/null; then
        aios_path=$(which aios-cli)
    elif [ -f "/root/.aios/aios-cli" ]; then
        aios_path="/root/.aios/aios-cli"
    elif [ -f "$HOME/.aios/aios-cli" ]; then
        aios_path="$HOME/.aios/aios-cli"
    elif [ -f "$HOME/.local/bin/aios-cli" ]; then
        aios_path="$HOME/.local/bin/aios-cli"
    fi
    
    echo "$aios_path"
}

# 检查系统要求
check_requirements() {
    log_info "检查系统要求..."
    
    # 检查curl
    if ! command -v curl &> /dev/null; then
        log_error "curl 未安装，正在安装..."
        sudo apt update && sudo apt install -y curl
    fi
    
    # 检查wget
    if ! command -v wget &> /dev/null; then
        log_info "安装 wget..."
        sudo apt install -y wget
    fi
    
    log_success "系统要求检查完成"
}

# 安装aiOS CLI
install_aios() {
    log_info "开始安装 aiOS CLI..."
    
    # 使用官方安装脚本
    if curl -fsSL https://download.hyper.space/api/install | bash; then
        log_success "aiOS CLI 安装成功"
        
        # 更新PATH环境
        source ~/.bashrc 2>/dev/null || true
        
        # 获取安装后的aios-cli路径
        local aios_path=$(get_aios_path)
        if [ -n "$aios_path" ]; then
            log_info "aiOS CLI 安装路径: $aios_path"
        fi
    else
        log_error "安装失败，尝试备用方法..."
        
        # 备用安装方法
        log_info "尝试手动安装..."
        mkdir -p ~/.local/bin
        cd ~/.local/bin
        
        # 下载最新版本（这里需要根据实际发布版本调整）
        wget -O aios-cli "https://github.com/hyperspaceai/aios-cli/releases/latest/download/aios-cli-linux"
        chmod +x aios-cli
        
        # 添加到PATH
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
        export PATH="$HOME/.local/bin:$PATH"
        
        log_success "手动安装完成"
    fi
}

# 验证安装
verify_installation() {
    log_info "验证安装..."
    
    if command -v aios-cli &> /dev/null; then
        log_success "aiOS CLI 已正确安装"
        aios-cli version
    else
        log_error "aiOS CLI 安装验证失败"
        exit 1
    fi
}

# 显示系统信息
show_system_info() {
    log_info "显示系统信息..."
    local aios_path=$(get_aios_path)
    if [ -n "$aios_path" ]; then
        $aios_path system-info
    else
        log_error "未找到 aios-cli"
    fi
}

# 启动aiOS守护进程
start_daemon() {
    log_info "启动 aiOS 守护进程..."
    
    local aios_path=$(get_aios_path)
    if [ -z "$aios_path" ]; then
        log_error "未找到 aios-cli，请先安装"
        return 1
    fi
    
    # 检查是否已经在运行
    if $aios_path status &> /dev/null; then
        log_warning "aiOS 守护进程已在运行"
        return
    fi
    
    # 启动守护进程
    $aios_path start &
    sleep 3
    
    # 检查启动状态
    if $aios_path status &> /dev/null; then
        log_success "aiOS 守护进程启动成功"
    else
        log_error "aiOS 守护进程启动失败"
    fi
}

# 显示可用模型
show_available_models() {
    log_info "获取可用模型列表..."
    local aios_path=$(get_aios_path)
    if [ -n "$aios_path" ]; then
        $aios_path models available
    else
        log_error "未找到 aios-cli"
    fi
}

# 安装示例模型
install_sample_model() {
    log_info "安装示例模型 (Mistral 7B)..."
    
    local aios_path=$(get_aios_path)
    if [ -z "$aios_path" ]; then
        log_error "未找到 aios-cli，请先安装"
        return 1
    fi
    
    # 安装一个常用的模型
    $aios_path models add hf:TheBloke/Mistral-7B-Instruct-v0.1-GGUF:mistral-7b-instruct-v0.1.Q4_K_S.gguf
    
    log_success "示例模型安装完成"
}

# 显示本地模型
show_local_models() {
    log_info "显示本地已安装模型..."
    local aios_path=$(get_aios_path)
    if [ -n "$aios_path" ]; then
        $aios_path models list
    else
        log_error "未找到 aios-cli"
    fi
}

# 运行示例推理
run_sample_inference() {
    log_info "运行示例推理..."
    
    local aios_path=$(get_aios_path)
    if [ -z "$aios_path" ]; then
        log_error "未找到 aios-cli，请先安装"
        return 1
    fi
    
    # 检查是否有本地模型
    if $aios_path models list | grep -q "mistral"; then
        log_info "使用本地模型进行推理..."
        $aios_path infer --model hf:TheBloke/Mistral-7B-Instruct-v0.1-GGUF:mistral-7b-instruct-v0.1.Q4_K_S.gguf --prompt "你好，请介绍一下你自己"
    else
        log_warning "没有找到本地模型，跳过推理测试"
    fi
}

# 部署完整节点（包含私钥导入和网络连接）
deploy_full_node() {
    log_info "开始部署完整节点..."
    
    local aios_path=$(get_aios_path)
    if [ -z "$aios_path" ]; then
        log_error "未找到 aios-cli，请先安装"
        return 1
    fi
    
    # 检查并安装screen
    check_and_install_screen
    
    # 提示输入屏幕名称
    read -p "请输入屏幕名称 (默认值: hyper): " screen_name
    screen_name=${screen_name:-hyper}
    log_info "使用的屏幕名称是: $screen_name"
    
    # 清理已存在的屏幕会话
    log_info "检查并清理现有的 '$screen_name' 屏幕会话..."
    screen -ls | grep "$screen_name" &>/dev/null
    if [ $? -eq 0 ]; then
        log_info "找到现有的 '$screen_name' 屏幕会话，正在停止并删除..."
        screen -S "$screen_name" -X quit
        sleep 2
    fi
    
    # 创建新的屏幕会话
    log_info "创建一个名为 '$screen_name' 的屏幕会话..."
    screen -S "$screen_name" -dm
    
    # 启动aios守护进程
    log_info "在屏幕会话中启动 aiOS 守护进程..."
    screen -S "$screen_name" -X stuff "$aios_path start\n"
    sleep 5
    
    # 提示用户输入私钥
    log_info "请输入你的私钥（按 CTRL+D 结束）："
    cat > my.pem
    
    # 导入私钥
    log_info "正在导入私钥..."
    $aios_path hive import-keys ./my.pem
    sleep 3
    
    # 安装模型
    log_info "正在安装 phi-2 模型..."
    local model="hf:TheBloke/phi-2-GGUF:phi-2.Q4_K_M.gguf"
    while true; do
        if $aios_path models add "$model"; then
            log_success "模型添加成功！"
            break
        else
            log_warning "添加模型时发生错误，正在重试..."
            sleep 3
        fi
    done
    
    # 登录并选择等级
    log_info "正在登录并选择等级..."
    $aios_path hive login
    
    # 提示用户选择等级
    echo "请选择等级（1-5）："
    select tier in 1 2 3 4 5; do
        case $tier in
            1|2|3|4|5)
                log_info "你选择了等级 $tier"
                $aios_path hive select-tier $tier
                break
                ;;
            *)
                log_warning "无效的选择，请输入 1 到 5 之间的数字。"
                ;;
        esac
    done
    
    # 连接到网络
    log_info "正在连接到网络..."
    $aios_path hive connect
    sleep 5
    
    # 停止当前进程并在后台重新启动
    log_info "停止当前进程并在后台重新启动..."
    $aios_path kill
    
    # 在屏幕会话中运行带连接的启动命令
    log_info "在屏幕会话中运行 'aios-cli start --connect'..."
    screen -S "$screen_name" -X stuff "$aios_path start --connect >> $HOME/aios-cli.log 2>&1\n"
    
    log_success "完整节点部署完成！"
    log_info "日志文件位置: $HOME/aios-cli.log"
    log_info "使用 'screen -r $screen_name' 查看运行状态"
}

# 查看积分
view_points() {
    log_info "正在查看积分..."
    local aios_path=$(get_aios_path)
    if [ -n "$aios_path" ]; then
        $aios_path hive points
    else
        log_error "未找到 aios-cli"
    fi
    sleep 3
}

# 查看日志
view_logs() {
    log_info "正在查看日志..."
    local log_file="$HOME/aios-cli.log"
    
    if [ -f "$log_file" ]; then
        log_info "显示日志的最后 200 行:"
        tail -n 200 "$log_file"
    else
        log_warning "日志文件不存在: $log_file"
    fi
}

# 查看私钥信息
view_private_key() {
    log_info "正在查看使用的私钥..."
    local aios_path=$(get_aios_path)
    if [ -n "$aios_path" ]; then
        $aios_path hive whoami
    else
        log_error "未找到 aios-cli"
    fi
    sleep 3
}

# 启动日志监控
start_log_monitor() {
    log_info "启动日志监控..."
    
    local log_file="$HOME/aios-cli.log"
    local screen_name="hyper"
    local monitor_script="$HOME/monitor.sh"
    
    # 创建监控脚本
    cat > "$monitor_script" << 'EOL'
#!/bin/bash
LOG_FILE="$HOME/aios-cli.log"
SCREEN_NAME="hyper"
LAST_RESTART=$(date +%s)
MIN_RESTART_INTERVAL=300

while true; do
    current_time=$(date +%s)
    
    # 检测到以下几种情况，触发重启
    if (tail -n 4 "$LOG_FILE" | grep -q "Last pong received.*Sending reconnect signal" || \
        tail -n 4 "$LOG_FILE" | grep -q "Failed to authenticate" || \
        tail -n 4 "$LOG_FILE" | grep -q "Failed to connect to Hive" || \
        tail -n 4 "$LOG_FILE" | grep -q "Another instance is already running" || \
        tail -n 4 "$LOG_FILE" | grep -q "\"message\": \"Internal server error\"" || \
        tail -n 4 "$LOG_FILE" | grep -q "thread 'main' panicked") && \
       [ $((current_time - LAST_RESTART)) -gt $MIN_RESTART_INTERVAL ]; then
        echo "$(date): 检测到连接问题，正在重启服务..." >> "$HOME/monitor.log"
        
        # 先发送 Ctrl+C
        screen -S "$SCREEN_NAME" -X stuff $'\003'
        sleep 5
        
        # 执行 aios-cli kill
        screen -S "$SCREEN_NAME" -X stuff "aios-cli kill\n"
        sleep 5
        
        echo "$(date): 清理旧日志..." > "$LOG_FILE"
        
        # 重新启动服务
        screen -S "$SCREEN_NAME" -X stuff "aios-cli start --connect >> $LOG_FILE 2>&1\n"
        
        LAST_RESTART=$current_time
        echo "$(date): 服务已重启" >> "$HOME/monitor.log"
    fi
    sleep 30
done
EOL
    
    # 添加执行权限
    chmod +x "$monitor_script"
    
    # 在后台启动监控脚本
    nohup "$monitor_script" > "$HOME/monitor.log" 2>&1 &
    
    log_success "日志监控已启动，后台运行中。"
    log_info "监控日志位置: $HOME/monitor.log"
    sleep 2
}

# 启动积分监控
start_points_monitor() {
    log_info "启动积分监控..."
    
    local aios_path=$(get_aios_path)
    local log_file="$HOME/aios-cli.log"
    local screen_name="hyper"
    local monitor_script="$HOME/points_monitor.sh"
    
    if [ -z "$aios_path" ]; then
        log_error "未找到 aios-cli"
        return 1
    fi
    
    # 创建积分监控脚本
    cat > "$monitor_script" << EOL
#!/bin/bash
LOG_FILE="$log_file"
SCREEN_NAME="$screen_name"
AIOS_PATH="$aios_path"
LAST_POINTS=0
MIN_RESTART_INTERVAL=300

while true; do
    CURRENT_POINTS=\$($AIOS_PATH hive points | grep -o '[0-9]\+' | head -1)
    
    if [ "\$CURRENT_POINTS" -eq "\$LAST_POINTS" ] && [ "\$CURRENT_POINTS" -gt 0 ]; then
        echo "\$(date): 积分没有增加，正在重启服务..." >> "\$HOME/points_monitor.log"
        
        # 重启服务
        screen -S "\$SCREEN_NAME" -X stuff \$'\003'
        sleep 5
        screen -S "\$SCREEN_NAME" -X stuff "\$AIOS_PATH kill\n"
        sleep 5
        
        echo "\$(date): 清理旧日志..." > "\$LOG_FILE"
        screen -S "\$SCREEN_NAME" -X stuff "\$AIOS_PATH start --connect >> \$LOG_FILE 2>&1\n"
        
        LAST_POINTS=\$CURRENT_POINTS
    else
        LAST_POINTS=\$CURRENT_POINTS
    fi

    sleep 7200  # 每2小时检查一次积分变化
done
EOL
    
    # 添加执行权限
    chmod +x "$monitor_script"
    
    # 在后台启动积分监控脚本
    nohup "$monitor_script" > "$HOME/points_monitor.log" 2>&1 &
    
    log_success "积分监控已启动，后台运行中。"
    log_info "监控日志位置: $HOME/points_monitor.log"
    sleep 2
}

# 显示帮助信息
show_help() {
    echo -e "${BLUE}aiOS CLI WSL 脚本使用说明${NC}"
    echo ""
    echo -e "${CYAN}基础命令：${NC}"
    echo "  install        - 安装 aiOS CLI"
    echo "  start          - 启动守护进程"
    echo "  status         - 检查守护进程状态"
    echo "  stop           - 停止守护进程"
    echo "  system         - 显示系统信息"
    echo ""
    echo -e "${CYAN}模型管理：${NC}"
    echo "  models         - 显示可用模型"
    echo "  install-model  - 安装示例模型"
    echo "  local-models   - 显示本地模型"
    echo "  infer          - 运行示例推理"
    echo ""
    echo -e "${CYAN}节点部署：${NC}"
    echo "  deploy         - 部署完整节点（包含私钥导入和网络连接）"
    echo "  points         - 查看积分"
    echo "  logs           - 查看日志"
    echo "  whoami         - 查看私钥信息"
    echo ""
    echo -e "${CYAN}监控功能：${NC}"
    echo "  log-monitor    - 启动日志监控"
    echo "  points-monitor - 启动积分监控"
    echo ""
    echo -e "${CYAN}一键安装：${NC}"
    echo "  full-setup     - 完整安装和配置"
    echo "  help           - 显示此帮助信息"
    echo ""
    echo -e "${YELLOW}示例：${NC}"
    echo "  ./hyper.sh install"
    echo "  ./hyper.sh deploy"
    echo "  ./hyper.sh full-setup"
    echo "  ./hyper.sh points"
    echo ""
    echo -e "${PURPLE}脚本由大赌社区哈哈哈哈编写，免费开源，请勿相信收费${NC}"
}

# 完整安装和配置
full_setup() {
    log_info "开始完整安装和配置..."
    
    check_wsl
    check_requirements
    install_aios
    verify_installation
    show_system_info
    start_daemon
    show_available_models
    install_sample_model
    show_local_models
    
    log_success "完整安装和配置完成！"
    echo ""
    echo -e "${GREEN}下一步操作建议：${NC}"
    echo "1. 运行 './hyper.sh start' 启动守护进程"
    echo "2. 运行 './hyper.sh models' 查看可用模型"
    echo "3. 运行 './hyper.sh deploy' 部署完整节点"
    echo "4. 运行 './hyper.sh points' 查看积分"
    echo "5. 运行 './hyper.sh logs' 查看日志"
}

# 停止守护进程
stop_daemon() {
    log_info "停止 aiOS 守护进程..."
    local aios_path=$(get_aios_path)
    if [ -n "$aios_path" ]; then
        $aios_path kill
        log_success "守护进程已停止"
    else
        log_error "未找到 aios-cli"
    fi
}

# 主函数
main() {
    case "${1:-help}" in
        "install")
            check_wsl
            check_requirements
            install_aios
            verify_installation
            ;;
        "start")
            start_daemon
            ;;
        "stop")
            stop_daemon
            ;;
        "status")
            local aios_path=$(get_aios_path)
            if [ -n "$aios_path" ]; then
                $aios_path status
            else
                log_error "未找到 aios-cli"
            fi
            ;;
        "models")
            show_available_models
            ;;
        "install-model")
            install_sample_model
            ;;
        "local-models")
            show_local_models
            ;;
        "infer")
            run_sample_inference
            ;;
        "system")
            show_system_info
            ;;
        "deploy")
            deploy_full_node
            ;;
        "points")
            view_points
            ;;
        "logs")
            view_logs
            ;;
        "whoami")
            view_private_key
            ;;
        "log-monitor")
            start_log_monitor
            ;;
        "points-monitor")
            start_points_monitor
            ;;
        "full-setup")
            full_setup
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# 主菜单函数
main_menu() {
    while true; do
        clear
        echo -e "${BLUE}================================================================"
        echo -e "${PURPLE}aiOS CLI WSL 管理脚本"
        echo -e "${BLUE}================================================================"
        echo -e "${CYAN}脚本由大赌社区哈哈哈哈编写，免费开源，请勿相信收费${NC}"
        echo -e "${YELLOW}如有问题，可联系推特，仅此只有一个号${NC}"
        echo -e "${BLUE}================================================================"
        echo -e "${GREEN}退出脚本，请按键盘 ctrl + C 退出即可${NC}"
        echo -e "${BLUE}================================================================"
        echo ""
        echo -e "${CYAN}请选择要执行的操作:${NC}"
        echo "1. 安装 aiOS CLI"
        echo "2. 部署完整节点"
        echo "3. 启动守护进程"
        echo "4. 查看守护进程状态"
        echo "5. 停止守护进程"
        echo "6. 查看积分"
        echo "7. 查看日志"
        echo "8. 查看私钥信息"
        echo "9. 显示系统信息"
        echo "10. 显示可用模型"
        echo "11. 安装示例模型"
        echo "12. 显示本地模型"
        echo "13. 运行示例推理"
        echo "14. 启动日志监控"
        echo "15. 启动积分监控"
        echo "16. 完整安装和配置"
        echo "17. 退出脚本"
        echo -e "${BLUE}================================================================"
        read -p "请输入选择 (1-17): " choice

        case $choice in
            1)  check_wsl; check_requirements; install_aios; verify_installation; read -n 1 -s -r -p "按任意键返回主菜单...";;
            2)  deploy_full_node; read -n 1 -s -r -p "按任意键返回主菜单...";;
            3)  start_daemon; read -n 1 -s -r -p "按任意键返回主菜单...";;
            4)  local aios_path=$(get_aios_path); if [ -n "$aios_path" ]; then $aios_path status; else log_error "未找到 aios-cli"; fi; read -n 1 -s -r -p "按任意键返回主菜单...";;
            5)  stop_daemon; read -n 1 -s -r -p "按任意键返回主菜单...";;
            6)  view_points; read -n 1 -s -r -p "按任意键返回主菜单...";;
            7)  view_logs; read -n 1 -s -r -p "按任意键返回主菜单...";;
            8)  view_private_key; read -n 1 -s -r -p "按任意键返回主菜单...";;
            9)  show_system_info; read -n 1 -s -r -p "按任意键返回主菜单...";;
            10) show_available_models; read -n 1 -s -r -p "按任意键返回主菜单...";;
            11) install_sample_model; read -n 1 -s -r -p "按任意键返回主菜单...";;
            12) show_local_models; read -n 1 -s -r -p "按任意键返回主菜单...";;
            13) run_sample_inference; read -n 1 -s -r -p "按任意键返回主菜单...";;
            14) start_log_monitor; read -n 1 -s -r -p "按任意键返回主菜单...";;
            15) start_points_monitor; read -n 1 -s -r -p "按任意键返回主菜单...";;
            16) full_setup; read -n 1 -s -r -p "按任意键返回主菜单...";;
            17) echo -e "${GREEN}退出脚本...${NC}"; exit 0;;
            *)  echo -e "${RED}无效选择，请重新输入！${NC}"; sleep 2;;
        esac
    done
}

# 脚本入口
if [ $# -eq 0 ]; then
    # 如果没有参数，显示主菜单
    main_menu
else
    # 如果有参数，执行对应的命令
    main "$@"
fi 
