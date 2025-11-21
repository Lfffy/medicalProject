<template>
  <div id="header">
      <div id="header-left">
          <div class="title-content">
            <span class="title-icon">👶</span>
            <h1>孕产妇健康管理大屏可视化系统</h1>
          </div>
      </div>
      <div id="header-nav">
            <div  :class="['header-nav-item', isActive(item.path) ? 'active' : '']" @click="routerChange(item.path)" v-for="item in routerLink">
                    <router-link class="nav content" :to="item.path">
                        {{item.meta.name}}
                    </router-link>
            </div>
      </div>
      <div id="header-actions">
        <!-- 移动端菜单切换按钮 -->
        <div class="mobile-menu-toggle" @click="toggleMobileMenu" title="菜单">
          <i :class="['fas', mobileMenuOpen ? 'fa-times' : 'fa-bars']"></i>
        </div>
        
        <div class="user-info" @click="toggleUserMenu">
          <i class="fas fa-user-circle"></i>
          <span class="user-name">{{ currentUser.name || '管理员' }}</span>
          <div class="user-menu" v-show="showUserMenu">
            <div class="menu-item" @click="showProfile">
              <i class="fas fa-user"></i>
              <span>个人资料</span>
            </div>
            <div class="menu-item" @click="showSettings">
              <i class="fas fa-cog"></i>
              <span>系统设置</span>
            </div>
            <div class="menu-item" @click="logout">
              <i class="fas fa-sign-out-alt"></i>
              <span>退出登录</span>
            </div>
          </div>
        </div>
        <div class="quick-actions">
          <div class="quick-action" @click="showNotifications" title="通知">
            <i class="fas fa-bell"></i>
            <span class="badge" v-if="notificationCount > 0">{{ notificationCount }}</span>
          </div>
          <div class="quick-action" @click="showHelp" title="帮助">
            <i class="fas fa-question-circle"></i>
          </div>
          <!-- 临时测试按钮 -->
          <div class="quick-action" @click="testHelpDialog" title="测试帮助" style="background: red;">
            测试
          </div>
        </div>
        <div id="header-time">
          {{ currentDateTime }}
        </div>
      </div>
      <!-- 帮助文档对话框 -->
    <HelpDialog :visible.sync="helpDialogVisible" />
  </div>
</template>

<script>
import HelpDialog from './HelpDialog.vue'

export default {
    components: {
        HelpDialog
    },
    data(){
        return {
            activePath:"/",
            routerLink:[],
            currentDateTime: this.getCurrentDateTime(),
            showUserMenu: false,
            notificationCount: 3,
            currentUser: {
                name: '管理员',
                role: 'admin',
                avatar: ''
            },
            mobileMenuOpen: false,
            helpDialogVisible: false
        }
    },
    created(){
        // 优化后的导航结构 - 包含所有核心模块，添加数据管理页面
        this.routerLink = this.$router.options.routes.filter(route => 
            ['/auth', '/data-center', '/data-management', '/analysis-center', '/monitoring-center', '/dashboard-center'].includes(route.path)
        );
        this.activePath = this.$route.path
        
        // 监听路由变化，确保activePath正确更新
        this.$watch(
            () => this.$route.path,
            (newPath) => {
                this.activePath = newPath
            }
        )
        
        this.interval = setInterval(() => {
            this.currentDateTime = this.getCurrentDateTime();
        }, 1000);
    },
    methods:{
        getCurrentDateTime() {
            const now = new Date();
            const year = now.getFullYear();
            const month = (now.getMonth() + 1).toString().padStart(2, '0');
            const day = now.getDate().toString().padStart(2, '0');
            const hours = now.getHours().toString().padStart(2, '0');
            const minutes = now.getMinutes().toString().padStart(2, '0');
            const seconds = now.getSeconds().toString().padStart(2, '0');
            return `${year}年${month}月${day}日 ${hours}:${minutes}:${seconds}`;
        },
        routerChange(path){
            this.activePath = path
        },
        // 检查路径是否为激活状态
        isActive(path) {
            return this.activePath === path
        },
        
        // 用户菜单相关方法
        toggleUserMenu() {
            this.showUserMenu = !this.showUserMenu;
        },
        
        showProfile() {
            this.$message.info('个人资料功能开发中...');
            this.showUserMenu = false;
        },
        
        showSettings() {
            this.$message.info('系统设置功能开发中...');
            this.showUserMenu = false;
        },
        
        logout() {
            this.$confirm('确定要退出登录吗？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.$message.success('退出登录成功');
                this.$router.push('/auth');
            });
            this.showUserMenu = false;
        },
        
        // 快捷功能方法
        showNotifications() {
            this.$message.info('暂无新通知');
        },
        
        showHelp() {
            console.log('showHelp被调用，helpDialogVisible当前值:', this.helpDialogVisible);
            this.helpDialogVisible = true;
            console.log('showHelp执行后，helpDialogVisible新值:', this.helpDialogVisible);
        },
        
        testHelpDialog() {
            console.log('testHelpDialog被调用');
            alert('测试按钮被点击了！');
            this.helpDialogVisible = true;
            console.log('testHelpDialog设置helpDialogVisible为true');
        },
        
        // 移动端菜单切换方法
        toggleMobileMenu() {
            this.mobileMenuOpen = !this.mobileMenuOpen;
            // 通过事件总线通知UnifiedLayout组件
            this.$root.$emit('toggle-mobile-menu');
        }
    },
    
    mounted() {
        // 点击页面其他地方关闭用户菜单
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.user-info')) {
                this.showUserMenu = false;
            }
        });
    },
    
    beforeDestroy() {
        document.removeEventListener('click', this.closeUserMenu);
    }
}
</script>

<style lang="less" scoped>
    #header {
        width: 100%;
        height: 70px;
        background: linear-gradient(135deg, #ff7eb3 0%, #ff66a3 100%);
        box-shadow: 0 4px 20px rgba(255, 102, 163, 0.2);
        display: flex;
        padding: 0 30px;
        align-items: center;
        justify-content: space-between;
        position: relative;
        z-index: 10;
        
        &::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: 
                radial-gradient(rgba(255,255,255,0.2) 2px, transparent 2px),
                radial-gradient(rgba(255,255,255,0.2) 2px, transparent 2px);
            background-size: 30px 30px;
            background-position: 0 0, 15px 15px;
            opacity: 0.3;
            z-index: -1;
        }
        
        #header-left {
            .title-content {
                display: flex;
                align-items: center;
            }
            
            .title-icon {
                font-size: 32px;
                margin-right: 15px;
                animation: heartbeat 1.5s ease-in-out infinite;
            }
            
            h1 {
                color: #fff;
                font-size: 26px;
                margin: 0;
                font-weight: 600;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            }
        }
        
        #header-nav {
            display: flex !important;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
            
            .header-nav-item {
                display: flex !important;
                align-items: center !important;
                padding: 8px 16px;
                border-radius: 25px;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                cursor: pointer;
                transition: all 0.3s ease;
                white-space: nowrap;
                flex-shrink: 0;
                
                &:hover {
                    background: rgba(255, 255, 255, 0.2);
                    transform: translateY(-2px);
                }
                
                &.active {
                    background: rgba(255, 255, 255, 0.3);
                    box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
                }
            }
            
            .nav {
                display: flex !important;
                align-items: center !important;
                text-decoration: none;
                color: #fff;
                font-size: 14px;
                font-weight: 500;
            }
        }
        
        #header-actions {
            display: flex;
            align-items: center;
            gap: 20px;
            
            .mobile-menu-toggle {
                display: none; /* 默认隐藏，只在移动端显示 */
                align-items: center;
                justify-content: center;
                width: 40px;
                height: 40px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 50%;
                cursor: pointer;
                transition: all 0.3s ease;
                
                &:hover {
                    background: rgba(255, 255, 255, 0.2);
                    transform: scale(1.1);
                }
                
                i {
                    color: #fff;
                    font-size: 18px;
                    transition: transform 0.3s ease;
                }
                
                &:active i {
                    transform: scale(0.9);
                }
            }
            
            .user-info {
                position: relative;
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 8px 15px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.3s ease;
                
                &:hover {
                    background: rgba(255, 255, 255, 0.2);
                }
                
                i {
                    color: #fff;
                    font-size: 20px;
                }
                
                .user-name {
                    color: #fff;
                    font-size: 14px;
                    font-weight: 500;
                }
                
                .user-menu {
                    position: absolute;
                    top: 100%;
                    right: 0;
                    margin-top: 10px;
                    background: rgba(255, 255, 255, 0.95);
                    border-radius: 12px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
                    backdrop-filter: blur(10px);
                    min-width: 180px;
                    z-index: 1000;
                    
                    .menu-item {
                        display: flex;
                        align-items: center;
                        gap: 12px;
                        padding: 12px 16px;
                        color: #333;
                        cursor: pointer;
                        transition: all 0.3s ease;
                        
                        &:hover {
                            background: linear-gradient(135deg, #ff7eb3 0%, #ff66a3 100%);
                            color: white;
                        }
                        
                        &:first-child {
                            border-radius: 12px 12px 0 0;
                        }
                        
                        &:last-child {
                            border-radius: 0 0 12px 12px;
                        }
                        
                        i {
                            color: inherit;
                            font-size: 16px;
                            width: 20px;
                        }
                        
                        span {
                            font-weight: 500;
                            font-size: 14px;
                        }
                    }
                }
            }
            
            .quick-actions {
                display: flex;
                align-items: center;
                gap: 15px;
                
                .quick-action {
                    position: relative;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 40px;
                    height: 40px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 50%;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    
                    &:hover {
                        background: rgba(255, 255, 255, 0.2);
                        transform: scale(1.1);
                    }
                    
                    i {
                        color: #fff;
                        font-size: 18px;
                    }
                    
                    .badge {
                        position: absolute;
                        top: -5px;
                        right: -5px;
                        background: #ff4757;
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                        padding: 2px 6px;
                        border-radius: 10px;
                        min-width: 18px;
                        text-align: center;
                    }
                }
            }
        }
        
        #header-time {
            color: #fff;
            font-size: 17px;
            background: rgba(255, 255, 255, 0.1);
            padding: 8px 15px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            font-weight: 500;
        }
    }
    
    .content {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    @keyframes heartbeat {
        0% {
            transform: scale(1);
        }
        14% {
            transform: scale(1.1);
        }
        28% {
            transform: scale(1);
        }
        42% {
            transform: scale(1.1);
        }
        70% {
            transform: scale(1);
        }
    }
    
    /* 移动端响应式样式 */
    @media (max-width: 768px) {
        #header {
            padding: 0 15px;
            
            #header-left h1 {
                font-size: 18px;
            }
            
            #header-nav {
                display: none; /* 隐藏桌面端导航 */
            }
            
            #header-actions {
                gap: 10px;
                
                .mobile-menu-toggle {
                    display: flex; /* 在移动端显示菜单按钮 */
                }
                
                .user-info .user-name {
                    display: none; /* 隐藏用户名，只显示头像 */
                }
                
                .quick-actions {
                    gap: 8px;
                    
                    .quick-action {
                        width: 35px;
                        height: 35px;
                    }
                }
                
                #header-time {
                    display: none; /* 在移动端隐藏时间显示 */
                }
            }
        }
    }
    
    @media (max-width: 480px) {
        #header {
            padding: 0 10px;
            
            #header-left {
                .title-icon {
                    font-size: 24px;
                    margin-right: 10px;
                }
                
                h1 {
                    font-size: 16px;
                }
            }
        }
    }
</style>